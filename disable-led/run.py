import sys
import logging
import os
import signal
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    stream=sys.stdout
)

# LED paths - these may vary by Pi model
LED_PATHS = {
    "power": [
        "/sys/class/leds/led1/brightness",  # Standard Pi 4
        "/sys/class/leds/PWR/brightness",   # Alternative path on some Pis
        "/sys/class/leds/pwr/brightness"    # Another alternative
    ],
    "activity": [
        "/sys/class/leds/led0/brightness",  # Standard Pi 4
        "/sys/class/leds/ACT/brightness",   # Alternative path
        "/sys/class/leds/act/brightness"    # Another alternative
    ]
}

# Find valid LED paths
ACTIVE_PATHS = {"power": None, "activity": None}

# State tracking
LED_STATE = {"power": None, "activity": None, "auto_mode": True, "has_leds": False}

def find_led_paths():
    """Detect available LED paths on this system"""
    for led_type, paths in LED_PATHS.items():
        for path in paths:
            if os.path.exists(path):
                ACTIVE_PATHS[led_type] = path
                try:
                    # Read current state
                    with open(path, "r") as f:
                        state = int(f.read().strip())
                    LED_STATE[led_type] = bool(state)
                    LED_STATE["has_leds"] = True
                    logging.info(f"Found {led_type} LED at {path}, current state: {state}")
                except Exception as e:
                    logging.warning(f"Found {led_type} LED at {path} but couldn't read state: {str(e)}")
                break
    
    if not LED_STATE["has_leds"]:
        logging.warning("No LED paths found. This might not be a Raspberry Pi or we lack permissions.")
        logging.info("Will continue in simulation mode.")

def toggle_led(led_type):
    """Toggle an LED state"""
    if not ACTIVE_PATHS[led_type]:
        logging.warning(f"No path found for {led_type} LED, can't toggle")
        # Still update our simulated state
        LED_STATE[led_type] = not LED_STATE[led_type]
        return

    try:
        new_state = "0" if LED_STATE[led_type] else "1"
        with open(ACTIVE_PATHS[led_type], "w") as f:
            f.write(new_state)
        LED_STATE[led_type] = not LED_STATE[led_type]
        logging.info(f"{led_type.capitalize()} LED toggled: {'OFF' if not LED_STATE[led_type] else 'ON'}")
    except Exception as e:
        logging.error(f"Error toggling {led_type} LED: {str(e)}")

def set_led(led_type, state):
    """Set LED to specific state (True=on, False=off)"""
    if not ACTIVE_PATHS[led_type]:
        logging.warning(f"No path found for {led_type} LED, can't set state")
        # Still update our simulated state
        LED_STATE[led_type] = state
        return

    try:
        with open(ACTIVE_PATHS[led_type], "w") as f:
            f.write("1" if state else "0")
        LED_STATE[led_type] = state
        logging.info(f"{led_type.capitalize()} LED set to: {'ON' if state else 'OFF'}")
    except Exception as e:
        logging.error(f"Error setting {led_type} LED: {str(e)}")

def disable_leds():
    """Turn off all LEDs"""
    logging.info("Disabling all LEDs...")
    for led_type in ["power", "activity"]:
        set_led(led_type, False)

def enable_leds():
    """Turn on all LEDs"""
    logging.info("Enabling all LEDs...")
    for led_type in ["power", "activity"]:
        set_led(led_type, True)

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    logging.info("Shutdown signal received")
    if LED_STATE["auto_mode"] and LED_STATE["has_leds"]:
        enable_leds()
        logging.info("Add-on stopped, LEDs restored")
    sys.exit(0)

def load_html_template():
    """Load the HTML template from file or use default if not found"""
    try:
        if os.path.exists('/templates/index.html'):
            with open('/templates/index.html', 'r') as f:
                return f.read()
    except Exception as e:
        logging.error(f"Error loading template: {str(e)}")
    
    # Fallback to default template
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Raspberry Pi LED Control</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                padding: 20px;
                max-width: 600px;
                margin: 0 auto;
                background-color: #f5f5f5;
                color: #333;
            }
            h1 { 
                color: #03a9f4; 
                margin-bottom: 10px;
            }
            .card {
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 20px;
                margin-bottom: 20px;
            }
            .system-info {
                font-size: 14px;
                margin-bottom: 20px;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 6px;
                border-left: 4px solid #03a9f4;
            }
            .button {
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
                transition: background-color 0.3s;
            }
            .button:hover {
                background-color: #0288d1;
            }
            .button.red { background-color: #f44336; }
            .button.red:hover { background-color: #d32f2f; }
            .button.green { background-color: #4CAF50; }
            .button.green:hover { background-color: #388e3c; }
            .active { background-color: #4CAF50; }
            .inactive { background-color: #f44336; }
            .controls { 
                display: flex;
                flex-direction: column;
                gap: 15px;
                margin-top: 20px;
            }
            .control-row {
                display: flex;
                align-items: center;
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }
            .control-row:last-child {
                border-bottom: none;
            }
            .control-row span {
                width: 120px;
                display: inline-block;
            }
            .status-dot {
                display: inline-block;
                height: 12px;
                width: 12px;
                border-radius: 50%;
                margin-right: 8px;
            }
            .led-warning {
                background-color: #fff3cd;
                color: #856404;
                padding: 10px;
                border-radius: 4px;
                margin-bottom: 20px;
                border-left: 4px solid #ffc107;
            }
            footer {
                margin-top: 20px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Raspberry Pi LED Control</h1>
            <p>Control your Raspberry Pi's onboard LEDs</p>
            
            <div id="led-warning" class="led-warning" style="display: none;">
                No LED controls were found. Running in simulation mode.
            </div>
            
            <div class="system-info">
                <div><strong>Status:</strong> <span id="status-text">Operational</span></div>
                <div><strong>LEDs Detected:</strong> <span id="leds-detected">Checking...</span></div>
            </div>
            
            <div class="controls">
                <div class="control-row">
                    <span>Auto Mode:</span> 
                    <span id="auto-dot" class="status-dot"></span>
                    <button id="auto-btn" class="button" onclick="toggleAutoMode()">
                        Loading...
                    </button>
                    <span style="margin-left: 10px;" id="auto-text">
                        (LEDs off when add-on runs, on when stopped)
                    </span>
                </div>
                
                <div class="control-row">
                    <span>Power LED:</span>
                    <span id="power-dot" class="status-dot"></span>
                    <button class="button" onclick="toggleLed('power')">
                        Toggle
                    </button>
                    <span style="margin-left: 10px;" id="power-text">
                        Loading...
                    </span>
                </div>
                
                <div class="control-row">
                    <span>Activity LED:</span>
                    <span id="activity-dot" class="status-dot"></span>
                    <button class="button" onclick="toggleLed('activity')">
                        Toggle
                    </button>
                    <span style="margin-left: 10px;" id="activity-text">
                        Loading...
                    </span>
                </div>
                
                <div class="control-row" style="margin-top: 15px;">
                    <button class="button green" onclick="enableAll()">Enable All LEDs</button>
                    <button class="button red" style="margin-left: 10px;" onclick="disableAll()">Disable All LEDs</button>
                </div>
            </div>
        </div>
        
        <footer>
            Raspberry Pi LED Control Add-on for Home Assistant
        </footer>
        
        <script>
            // Initial state load
            window.onload = function() {
                updateStatus();
            };
            
            function updateStatus() {
                fetch('/api/status')
                    .then(response => response.json())
                    .then(data => {
                        // Update UI based on state
                        document.getElementById('auto-dot').className = 'status-dot ' + (data.state.auto_mode ? 'active' : 'inactive');
                        document.getElementById('auto-btn').className = 'button ' + (data.state.auto_mode ? 'green' : 'red');
                        document.getElementById('auto-btn').innerText = data.state.auto_mode ? 'ON' : 'OFF';
                        
                        document.getElementById('power-dot').className = 'status-dot ' + (data.state.power ? 'active' : 'inactive');
                        document.getElementById('power-text').innerText = 'Currently: ' + (data.state.power ? 'ON' : 'OFF');
                        
                        document.getElementById('activity-dot').className = 'status-dot ' + (data.state.activity ? 'active' : 'inactive');
                        document.getElementById('activity-text').innerText = 'Currently: ' + (data.state.activity ? 'ON' : 'OFF');
                        
                        // Show simulation warning if needed
                        if (!data.state.has_leds) {
                            document.getElementById('led-warning').style.display = 'block';
                            document.getElementById('leds-detected').innerText = 'No';
                        } else {
                            document.getElementById('led-warning').style.display = 'none';
                            document.getElementById('leds-detected').innerText = 'Yes';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('status-text').innerText = 'Error connecting to server';
                    });
            }
            
            function toggleAutoMode() {
                fetch('/api/toggle/auto', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) updateStatus();
                    });
            }
            
            function toggleLed(led) {
                fetch('/api/toggle/' + led, { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) updateStatus();
                    });
            }
            
            function enableAll() {
                fetch('/api/enable_all', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) updateStatus();
                    });
            }
            
            function disableAll() {
                fetch('/api/disable_all', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) updateStatus();
                    });
            }
        </script>
    </body>
    </html>
    """

# Web UI handler
class LEDControlHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = load_html_template()
            self.wfile.write(html.encode())
        elif self.path == '/api/status':
            self._serve_status()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/toggle/power':
            toggle_led('power')
            self._serve_status()
        elif self.path == '/api/toggle/activity':
            toggle_led('activity')
            self._serve_status()
        elif self.path == '/api/toggle/auto':
            LED_STATE["auto_mode"] = not LED_STATE["auto_mode"]
            logging.info(f"Auto mode toggled: {'ON' if LED_STATE['auto_mode'] else 'OFF'}")
            self._serve_status()
        elif self.path == '/api/disable_all':
            disable_leds()
            self._serve_status()
        elif self.path == '/api/enable_all':
            enable_leds()
            self._serve_status()
        else:
            self.send_response(404)
            self.end_headers()
    
    def _serve_status(self):
        """Send current status as JSON"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "success": True, 
            "state": LED_STATE
        }).encode())

def main():
    # Find LED paths
    find_led_paths()
    
    # Trap exit signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Auto mode - disable LEDs when the add-on starts
    if LED_STATE["auto_mode"] and LED_STATE["has_leds"]:
        disable_leds()
    
    # Start web server
    server_address = ('', 8099)
    httpd = HTTPServer(server_address, LEDControlHandler)
    logging.info("Starting LED control server on port 8099")
    
    try:
        httpd.serve_forever()
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        # Make sure LEDs are restored if there's an error
        if LED_STATE["auto_mode"] and LED_STATE["has_leds"]:
            enable_leds()

if __name__ == "__main__":
    main()