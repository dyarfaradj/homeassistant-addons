import os
import signal
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# LED paths
LED_PWR = "/sys/class/leds/led1/brightness"
LED_ACT = "/sys/class/leds/led0/brightness"

# Track LED state
LED_STATE = {"power": False, "activity": False, "auto_mode": True}

def disable_leds():
    """Turn off the LEDs"""
    print("Disabling LEDs...")
    try:
        with open(LED_PWR, "w") as f:
            f.write("0")
        LED_STATE["power"] = False
        with open(LED_ACT, "w") as f:
            f.write("0")
        LED_STATE["activity"] = False
    except PermissionError:
        print("Permission denied. Ensure the add-on runs with privileged access.")

def enable_leds():
    """Turn LEDs back on"""
    print("Restoring LEDs...")
    try:
        with open(LED_PWR, "w") as f:
            f.write("1")
        LED_STATE["power"] = True
        with open(LED_ACT, "w") as f:
            f.write("1")
        LED_STATE["activity"] = True
    except PermissionError:
        print("Permission denied. Ensure the add-on runs with privileged access.")

def toggle_power_led():
    """Toggle power LED"""
    try:
        new_state = "0" if LED_STATE["power"] else "1"
        with open(LED_PWR, "w") as f:
            f.write(new_state)
        LED_STATE["power"] = not LED_STATE["power"]
    except PermissionError:
        print("Permission denied when toggling power LED")

def toggle_activity_led():
    """Toggle activity LED"""
    try:
        new_state = "0" if LED_STATE["activity"] else "1"
        with open(LED_ACT, "w") as f:
            f.write(new_state)
        LED_STATE["activity"] = not LED_STATE["activity"]
    except PermissionError:
        print("Permission denied when toggling activity LED")

def signal_handler(sig, frame):
    """Handle shutdown signals (so LEDs turn back on when add-on stops)"""
    if LED_STATE["auto_mode"]:
        enable_leds()
        print("Add-on stopped, LEDs restored.")
    exit(0)

# Simple web UI handler
class LEDControlHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Raspberry Pi LED Control</title>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                        padding: 20px;
                        max-width: 600px;
                        margin: 0 auto;
                    }}
                    h1 {{ color: #03a9f4; }}
                    .button {{
                        background-color: #03a9f4;
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border-radius: 4px;
                    }}
                    .button.red {{ background-color: #f44336; }}
                    .button.green {{ background-color: #4CAF50; }}
                    .active {{ background-color: #4CAF50; }}
                    .inactive {{ background-color: #f44336; }}
                    .controls {{ 
                        display: flex;
                        flex-direction: column;
                        gap: 15px;
                        margin-top: 20px;
                    }}
                    .control-row {{
                        display: flex;
                        align-items: center;
                    }}
                    .control-row span {{
                        width: 120px;
                        display: inline-block;
                    }}
                    .status-dot {{
                        display: inline-block;
                        height: 12px;
                        width: 12px;
                        border-radius: 50%;
                        margin-right: 8px;
                    }}
                </style>
            </head>
            <body>
                <h1>Raspberry Pi LED Control</h1>
                <p>Control your Raspberry Pi's onboard LEDs</p>
                
                <div class="controls">
                    <div class="control-row">
                        <span>Auto Mode:</span> 
                        <span class="status-dot {'active' if LED_STATE['auto_mode'] else 'inactive'}"></span>
                        <button class="button {'green' if LED_STATE['auto_mode'] else 'red'}" onclick="toggleAutoMode()">
                            {'ON' if LED_STATE['auto_mode'] else 'OFF'}
                        </button>
                        <span style="margin-left: 10px;">
                            (LEDs off when add-on runs, on when stopped)
                        </span>
                    </div>
                    
                    <div class="control-row">
                        <span>Power LED:</span>
                        <span class="status-dot {'inactive' if LED_STATE['power'] else 'active'}"></span>
                        <button class="button" onclick="toggleLed('power')">
                            Toggle
                        </button>
                        <span style="margin-left: 10px;">
                            Currently: {'OFF' if not LED_STATE['power'] else 'ON'}
                        </span>
                    </div>
                    
                    <div class="control-row">
                        <span>Activity LED:</span>
                        <span class="status-dot {'inactive' if LED_STATE['activity'] else 'active'}"></span>
                        <button class="button" onclick="toggleLed('activity')">
                            Toggle
                        </button>
                        <span style="margin-left: 10px;">
                            Currently: {'OFF' if not LED_STATE['activity'] else 'ON'}
                        </span>
                    </div>
                    
                    <div class="control-row" style="margin-top: 15px;">
                        <button class="button green" onclick="enableAll()">Enable All LEDs</button>
                        <button class="button red" style="margin-left: 10px;" onclick="disableAll()">Disable All LEDs</button>
                    </div>
                </div>
                
                <script>
                    function toggleAutoMode() {{
                        fetch('/toggle/auto', {{ method: 'POST' }})
                            .then(response => response.json())
                            .then(data => {{
                                if (data.success) location.reload();
                            }});
                    }}
                    
                    function toggleLed(led) {{
                        fetch('/toggle/' + led, {{ method: 'POST' }})
                            .then(response => response.json())
                            .then(data => {{
                                if (data.success) location.reload();
                            }});
                    }}
                    
                    function enableAll() {{
                        fetch('/enable_all', {{ method: 'POST' }})
                            .then(response => response.json())
                            .then(data => {{
                                if (data.success) location.reload();
                            }});
                    }}
                    
                    function disableAll() {{
                        fetch('/disable_all', {{ method: 'POST' }})
                            .then(response => response.json())
                            .then(data => {{
                                if (data.success) location.reload();
                            }});
                    }}
                </script>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/toggle/power':
            toggle_power_led()
            self._respond_ok()
        elif self.path == '/toggle/activity':
            toggle_activity_led()
            self._respond_ok()
        elif self.path == '/toggle/auto':
            LED_STATE["auto_mode"] = not LED_STATE["auto_mode"]
            self._respond_ok()
        elif self.path == '/disable_all':
            disable_leds()
            self._respond_ok()
        elif self.path == '/enable_all':
            enable_leds()
            self._respond_ok()
        else:
            self.send_response(404)
            self.end_headers()
    
    def _respond_ok(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "state": LED_STATE}).encode())

# Trap exit signals
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Auto mode - disable LEDs when the add-on starts
if LED_STATE["auto_mode"]:
    disable_leds()

# Start web server (will be available via ingress)
def run_server():
    server_address = ('', 8099)
    httpd = HTTPServer(server_address, LEDControlHandler)
    print("Starting LED control server on port 8099")
    httpd.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Keep running indefinitely
while True:
    time.sleep(1)