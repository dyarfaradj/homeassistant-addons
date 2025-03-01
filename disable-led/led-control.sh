#!/usr/bin/with-contenv bash
# ==============================================================================
# Home Assistant Add-on: Raspberry Pi LED Control
# Main script to control Raspberry Pi LEDs
# Based on https://github.com/home-assistant/operating-system/pull/2854
# ==============================================================================
set -e

# Get parameters
POWER_LED=$1
ACTIVITY_LED=$2

# Define LED paths based on Raspberry Pi model
if [ -d "/sys/class/leds/PWR" ]; then
    # Newer Raspberry Pi models
    POWER_LED_PATH="/sys/class/leds/PWR"
elif [ -d "/sys/class/leds/led0" ]; then
    # Older Raspberry Pi models (led0 is typically power)
    POWER_LED_PATH="/sys/class/leds/led0"
else
    echo "Power LED path not found"
    POWER_LED_PATH=""
fi

if [ -d "/sys/class/leds/ACT" ]; then
    # Newer Raspberry Pi models
    ACTIVITY_LED_PATH="/sys/class/leds/ACT"
elif [ -d "/sys/class/leds/led1" ]; then
    # Older Raspberry Pi models (led1 is typically activity)
    ACTIVITY_LED_PATH="/sys/class/leds/led1"
else
    echo "Activity LED path not found"
    ACTIVITY_LED_PATH=""
fi

# Function to control LED
control_led() {
    LED_PATH=$1
    LED_STATE=$2
    
    if [ -z "$LED_PATH" ]; then
        echo "LED path not available, skipping"
        return
    fi
    
    # Save original trigger to restore if needed
    if [ ! -f "/tmp/original_$(basename $LED_PATH)_trigger" ]; then
        cat "$LED_PATH/trigger" | grep -o "\[[a-z]*\]" | tr -d "[]" > "/tmp/original_$(basename $LED_PATH)_trigger"
    fi
    
    case $LED_STATE in
        "off")
            echo "none" > "$LED_PATH/trigger"
            echo "0" > "$LED_PATH/brightness"
            ;;
        "on")
            echo "none" > "$LED_PATH/trigger"
            echo "1" > "$LED_PATH/brightness"
            ;;
        "heartbeat")
            echo "heartbeat" > "$LED_PATH/trigger"
            ;;
        "mmc")
            echo "mmc0" > "$LED_PATH/trigger"
            ;;
        "timer")
            echo "timer" > "$LED_PATH/trigger"
            ;;
        *)
            echo "Invalid LED state: $LED_STATE"
            ;;
    esac
}

# Control LEDs
if [ -n "$POWER_LED_PATH" ]; then
    echo "Setting power LED to $POWER_LED"
    control_led "$POWER_LED_PATH" "$POWER_LED"
fi

if [ -n "$ACTIVITY_LED_PATH" ]; then
    echo "Setting activity LED to $ACTIVITY_LED"
    control_led "$ACTIVITY_LED_PATH" "$ACTIVITY_LED"
fi

echo "LED settings applied successfully"