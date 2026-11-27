"""
AgroNexon Plant Disease Inference API
- Reads a JPEG frame from ESP32-CAM /capture.
- Runs an ONNX image classifier.
- Returns top prediction and confidence.
IMPORTANT: model preprocessing and class order MUST match your training pipeline.
"""
import os, time
from pathlib import Path
from typing import Optional
import cv2
import numpy as np
import requests
import onnxruntime as ort
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

BASE = Path(__file__).resolve().parent
MODEL_PATH = Path(os.getenv("MODEL_PATH", BASE / "disease_model.onnx"))
LABELS_PATH = Path(os.getenv("LABELS_PATH", BASE / "labels.txt"))
CAMERA_CAPTURE_URL = os.getenv("CAMERA_CAPTURE_URL", "http://192.168.1.50/capture")
INPUT_SIZE = int(os.getenv("INPUT_SIZE", "224"))
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.60"))

app = FastAPI(title="AgroNexon Plant Disease API", version="1.0")
session: Optional[ort.InferenceSession] = None
labels = []

class PredictRequest(BaseModel):
    image_url: Optional[str] = None

def load_model():
    global session, labels
    if not MODEL_PATH.exists():
        raise RuntimeError(f"ONNX model not found: {MODEL_PATH}")
    if not LABELS_PATH.exists():
        raise RuntimeError(f"labels.txt not found: {LABELS_PATH}")
    labels = [x.strip() for x in LABELS_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]
    session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])

@app.on_event("startup")
def startup():
    try:
        load_model()
    except Exception as exc:
        # API remains available so /health explains the missing model.
        print("Model not loaded:", exc)

def fetch_image(url: str):
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        arr = np.frombuffer(r.content, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode camera JPEG")
        return img
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Camera fetch failed: {exc}")

def preprocess(bgr):
    # Default ImageNet-style preprocessing. Change if your ONNX model expects
    # different normalization, RGB/BGR order, dimensions, or input layout.
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (INPUT_SIZE, INPUT_SIZE))
    x = resized.astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    x = (x - mean) / std
    x = np.transpose(x, (2, 0, 1))[None, ...]
    return x.astype(np.float32)

def softmax(x):
    x = x - np.max(x)
    e = np.exp(x)
    return e / np.sum(e)

@app.get("/")
def root():
    return {"project": "AgroNexon", "service": "Plant disease detection", "docs": "/docs"}

@app.get("/health")
def health():
    return {
        "ok": session is not None,
        "model_path": str(MODEL_PATH),
        "camera_capture_url": CAMERA_CAPTURE_URL,
        "labels": len(labels),
    }

@app.post("/predict")
def predict(req: PredictRequest = PredictRequest()):
    if session is None:
        raise HTTPException(status_code=503, detail="Model unavailable. Add disease_model.onnx and labels.txt.")
    url = req.image_url or CAMERA_CAPTURE_URL
    img = fetch_image(url)
    x = preprocess(img)
    input_meta = session.get_inputs()[0]
    output = session.run(None, {input_meta.name: x})[0]
    scores = np.asarray(output).squeeze()
    probs = softmax(scores)
    idx = int(np.argmax(probs))
    confidence = float(probs[idx])
    label = labels[idx] if idx < len(labels) else f"class_{idx}"
    return {
        "timestamp": int(time.time()),
        "prediction": label if confidence >= CONFIDENCE_THRESHOLD else "Uncertain - retake image",
        "raw_class": label,
        "confidence": round(confidence, 4),
        "accepted": confidence >= CONFIDENCE_THRESHOLD,
        "note": "AI output is advisory; confirm visually before spraying or treatment."
    }

@app.get("/capture-and-predict")
def capture_and_predict():
    return predict(PredictRequest())
