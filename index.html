# 

# <!DOCTYPE html>

# <html lang="en">

# <head>

# <meta charset="UTF-8">

# <meta name="viewport" content="width=device-width, initial-scale=1">

# <title>AgroNexon Dashboard</title>

# <style>

# body{margin:0;background:#101a13;color:#eef5ed;font-family:Arial;padding:25px}

# header{display:flex;justify-content:space-between;align-items:center}

# h1{color:#a8dc8d}

# .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin-top:25px}

# .card{background:#1b2b20;padding:22px;border-radius:14px;border:1px solid #36523b}

# .value{font-size:30px;color:#a8dc8d;font-weight:bold}

# button{padding:12px 18px;margin:5px;background:#477c4b;color:white;border:0;border-radius:8px;cursor:pointer}

# .status{color:#f2c66d}

# </style>

# </head>

# <body>

# <header>

# &#x20;<div><h1>🌱 AgroNexon</h1>

# &#x20;<p>Precision Agriculture Rover System</p></div>

# &#x20;<div class="status" id="status">● Awaiting rover connection</div>

# </header>

# 

# <div class="grid">

# &#x20;<div class="card"><h3>Soil Moisture</h3>

# &#x20;<div class="value" id="soil">-- %</div></div>

# &#x20;<div class="card"><h3>Obstacle Distance</h3>

# &#x20;<div class="value" id="distance">-- cm</div></div>

# &#x20;<div class="card"><h3>Obstacle Status</h3>

# &#x20;<div class="value" id="obstacle">--</div></div>

# &#x20;<div class="card"><h3>Rover Control</h3>

# &#x20;<button onclick="send('forward')">Forward</button>

# &#x20;<button onclick="send('left')">Left</button>

# &#x20;<button onclick="send('stop')">STOP</button>

# &#x20;<button onclick="send('right')">Right</button>

# &#x20;<button onclick="send('backward')">Reverse</button>

# &#x20;</div>

# &#x20;<div class="card"><h3>Pump Control</h3>

# &#x20;<button onclick="pump(1)">Pump ON</button>

# &#x20;<button onclick="pump(0)">Pump OFF</button>

# &#x20;<p id="pump">Unknown</p></div>

# &#x20;<div class="card"><h3>Camera Monitoring</h3>

# &#x20;<p>ESP32-CAM stream connection pending</p>

# &#x20;</div>

# </div>

# 

# <script>

# const API = ""; // Add your secure rover API URL here

# 

# async function getData(){

# &#x20;if(!API) return;

# &#x20;try{

# &#x20; const r=await fetch(API+"/api/status");

# &#x20; const d=await r.json();

# &#x20; document.getElementById("soil").textContent=d.soil\_percent+" %";

# &#x20; document.getElementById("distance").textContent=d.distance\_cm+" cm";

# &#x20; document.getElementById("obstacle").textContent=d.obstacle?"Detected":"Clear";

# &#x20; document.getElementById("pump").textContent=d.pump?"ON":"OFF";

# &#x20; document.getElementById("status").textContent="● Connected";

# &#x20;}catch(e){

# &#x20; document.getElementById("status").textContent="● Connection unavailable";

# &#x20;}

# }

# async function send(direction){

# &#x20;if(!API){alert("Rover API not configured");return;}

# &#x20;try{await fetch(API+"/api/move?dir="+direction);}

# &#x20;catch(e){alert("Command failed");}

# }

# async function pump(value){

# &#x20;if(!API){alert("Rover API not configured");return;}

# &#x20;try{await fetch(API+"/api/pump?v="+value);}

# &#x20;catch(e){alert("Pump command failed");}

# }

# setInterval(getData,2000);

# getData();

# </script>

# </body>

# </html>



