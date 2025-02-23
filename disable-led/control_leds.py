import os
import signal
import time

# LED paths
LED_PWR = "/sys/class/leds/led1/brightness"
LED_ACT = "/sys/class/leds/led0/brightness"

def disable_leds():
    """Turn off the LEDs"""
    print("Disabling LEDs...")
    try:
        with open(LED_PWR, "w") as f:
            f.write("0")
        with open(LED_ACT, "w") as f:
            f.write("0")
    except PermissionError:
        print("Permission denied. Ensure the add-on runs with privileged access.")

def enable_leds():
    """Turn LEDs back on"""
    print("Restoring LEDs...")
    try:
        with open(LED_PWR, "w") as f:
            f.write("1")
        with open(LED_ACT, "w") as f:
            f.write("1")
    except PermissionError:
        print("Permission denied. Ensure the add-on runs with privileged access.")

def signal_handler(sig, frame):
    """Handle shutdown signals (so LEDs turn back on when add-on stops)"""
    enable_leds()
    print("Add-on stopped, LEDs restored.")
    exit(0)

# Trap exit signals
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Disable LEDs when the add-on starts
disable_leds()

# Keep running indefinitely
while True:
    time.sleep(1)
