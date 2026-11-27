# AgroNexon Installation & Test Guide

## 1. Arduino IDE setup

1. Install Arduino IDE 2.x.
2. In Preferences, add Espressif ESP32 Boards Manager URL:
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
3. Boards Manager -> install `esp32` by Espressif Systems.
4. Install ArduinoJson library by Benoit Blanchon.
5. For the main controller, select `ESP32 Dev Module`.
6. Select a suitable upload speed (115200 initially) and the correct COM port.
7. Open `ESP32_Controller/AgroNexon_Controller.ino`.
8. Edit Wi-Fi SSID/password and camera stream URL.
9. Upload and open Serial Monitor at 115200 baud.

The main sketch uses the ESP32 Arduino Core 3.x LEDC API (`ledcAttach`,
`ledcWrite(pin, duty)`). If using Core 2.x, update PWM calls as noted in code.

## 2. ESP32-CAM setup

1. Open `ESP32_CAM/AgroNexon_Camera.ino`.
2. Set the same Wi-Fi SSID/password as the main controller.
3. Select the correct ESP32-CAM board profile (commonly AI Thinker ESP32-CAM).
4. Select PSRAM enabled where supported.
5. Upload using your ESP32-CAM-MB programmer or USB-to-TTL adapter.
6. Open Serial Monitor at 115200.
7. Note the camera IP. Test `http://CAMERA_IP/` and `http://CAMERA_IP:81/stream`.
8. Set the camera stream URL in the main controller firmware and re-upload.

Both devices must be on the same Wi-Fi network for the dashboard to show the stream.
If the main ESP32 falls back to its own AP, connect to AgroNexon-Rover and use
http://192.168.4.1. In that fallback arrangement the camera will not automatically
join the rover AP unless its Wi-Fi configuration is changed to that AP.

## 3. Python AI server

Use Python 3.10 or 3.11 in a virtual environment (recommended).

Windows:
```powershell
cd AI_Disease_Detection
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy labels.txt.example labels.txt
```

Linux/macOS:
```bash
cd AI_Disease_Detection
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp labels.txt.example labels.txt
```

Copy your trained ONNX model into this folder as `disease_model.onnx`.
Replace `labels.txt` with exact class names in exact model output order.
Set camera capture URL:
- Windows PowerShell: `$env:CAMERA_CAPTURE_URL="http://CAMERA_IP/capture"`
- Linux/macOS: `export CAMERA_CAPTURE_URL="http://CAMERA_IP/capture"`

Run:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
Open `http://127.0.0.1:8000/docs`, then test POST `/predict`.
Open `/health` to verify model loading.

IMPORTANT: Default preprocessing is RGB, 224x224, ImageNet mean/std, NCHW.
If the model was trained with different transforms, update `preprocess()` accordingly.
Some ONNX models output probabilities already; if so, remove softmax in `predict()`.
Check the model input dimensions and output tensor before field use.

## 4. First power-up checklist

- Lift all four wheels clear of the ground.
- Disconnect pump power initially.
- Confirm battery polarity and fuse.
- Confirm common ground.
- Confirm motor driver voltage and current ratings are adequate.
- Power the ESP32 from a regulated supply, not from motor outputs.
- Verify relay defaults OFF on boot.
- Keep a physical battery disconnect / emergency stop accessible.

## 5. Test sequence

1. Upload main firmware with motor power disconnected; verify dashboard loads.
2. Test `/api/status`; soil and distance values should update.
3. Test ultrasonic readings with a flat object at 20, 40 and 80 cm.
4. Calibrate soil dry/wet raw values and update constants in firmware.
5. With wheels lifted, test forward, backward, left and right at low speed.
6. If a side runs backward, swap that side's direction wiring or correct direction logic.
7. Put rover on floor in a clear area; test manual stop and emergency stop.
8. Test obstacle stop with a box in front; verify rover stops before contact.
9. Test auto mode at low speed in a clear, supervised area.
10. Test pump relay with pump disconnected; confirm relay ON/OFF polarity.
11. Connect pump and water only after electrical checks. Check leaks and current draw.
12. Test camera `/capture` and `/stream`.
13. Test AI `/health`, then `/predict` with a known plant image.
14. Validate model predictions on held-out images before treating any plant.

## 6. Known limitations of Version 1

- Autonomous mode is reactive obstacle avoidance, not true farm-row navigation.
- No GPS, wheel encoders, odometry, mapping or row detection is implemented.
- Soil percentage is a calibrated sensor estimate, not a laboratory soil nutrient analysis.
- Disease classification requires a compatible trained ONNX model and matching labels/preprocessing.
- Spraying is manually controlled; no chemical dosing or disease-triggered spraying is enabled.
- A browser stop button is not a certified emergency stop. Use a physical power cutoff.
