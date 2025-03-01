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

echo "LED Control Script started"
echo "Checking available LED paths..."

# List available LED paths for debugging
echo "Available LED paths:"
ls -la /sys/class/leds/ || echo "Failed to list LED paths"

# Define LED paths based on Raspberry Pi model
if [ -d "/sys/class/leds/PWR" ]; then
    # Newer Raspberry Pi models
    POWER_LED_PATH="/sys/class/leds/PWR"
    echo "Found Power LED path: $POWER_LED_PATH"
elif [ -d "/sys/class/leds/led0" ]; then
    # Older Raspberry Pi models (led0 is typically power)
    POWER_LED_PATH="/sys/class/leds/led0"
    echo "Found Power LED path: $POWER_LED_PATH"
else
    echo "Power LED path not found"
    POWER_LED_PATH=""
fi

if [ -d "/sys/class/leds/ACT" ]; then
    # Newer Raspberry Pi models
    ACTIVITY_LED_PATH="/sys/class/leds/ACT"
    echo "Found Activity LED path: $ACTIVITY_LED_PATH"
elif [ -d "/sys/class/leds/led1" ]; then
    # Older Raspberry Pi models (led1 is typically activity)
    ACTIVITY_LED_PATH="/sys/class/leds/led1"
    echo "Found Activity LED path: $ACTIVITY_LED_PATH"
else
    echo "Activity LED path not found"
    ACTIVITY_LED_PATH=""
fi

# Function to control LED with verbose output
control_led() {
    LED_PATH=$1
    LED_STATE=$2
    
    if [ -z "$LED_PATH" ]; then
        echo "LED path not available, skipping"
        return
    fi
    
    echo "Controlling LED at $LED_PATH to state: $LED_STATE"
    
    # Check if LED path is writable
    if [ ! -w "$LED_PATH/trigger" ]; then
        echo "ERROR: Cannot write to $LED_PATH/trigger - check permissions"
        return 1
    fi
    
    # Save original trigger to restore if needed
    if [ ! -f "/tmp/original_$(basename $LED_PATH)_trigger" ]; then
        echo "Saving original trigger state"
        cat "$LED_PATH/trigger" | grep -o "\[[a-z0-9]*\]" | tr -d "[]" > "/tmp/original_$(basename $LED_PATH)_trigger" || echo "Failed to save original trigger"
    fi
    
    echo "Setting LED to $LED_STATE mode"
    case $LED_STATE in
        "off")
            echo "Setting to OFF - writing 'none' to trigger and '0' to brightness"
            echo "none" > "$LED_PATH/trigger" || echo "Failed to write to trigger"
            echo "0" > "$LED_PATH/brightness" || echo "Failed to write to brightness"
            ;;
        "on")
            echo "Setting to ON - writing 'none' to trigger and '1' to brightness"
            echo "none" > "$LED_PATH/trigger" || echo "Failed to write to trigger"
            echo "1" > "$LED_PATH/brightness" || echo "Failed to write to brightness"
            ;;
        "heartbeat")
            echo "Setting to HEARTBEAT mode"
            echo "heartbeat" > "$LED_PATH/trigger" || echo "Failed to write to trigger"
            ;;
        "mmc")
            echo "Setting to MMC mode"
            echo "mmc0" > "$LED_PATH/trigger" || echo "Failed to write to trigger"
            ;;
        "timer")
            echo "Setting to TIMER mode"
            echo "timer" > "$LED_PATH/trigger" || echo "Failed to write to trigger"
            ;;
        *)
            echo "Invalid LED state: $LED_STATE"
            ;;
    esac
    
    echo "Current LED status:"
    echo "- Trigger: $(cat $LED_PATH/trigger)"
    echo "- Brightness: $(cat $LED_PATH/brightness)"
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