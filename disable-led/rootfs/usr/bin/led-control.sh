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

# Function to control LED with permission verification
control_led() {
    LED_PATH=$1
    LED_STATE=$2
    
    if [ -z "$LED_PATH" ]; then
        echo "LED path not available, skipping"
        return
    fi
    
    echo "Controlling LED at $LED_PATH to state: $LED_STATE"
    
    # Check if LED path exists
    if [ ! -d "$LED_PATH" ]; then
        echo "ERROR: LED path $LED_PATH does not exist"
        return 1
    fi
    
    # Display permissions for debugging
    echo "Permissions on LED files:"
    ls -la $LED_PATH/ || echo "Failed to list LED files"
    
    # Try using a direct approach with privileged access
    echo "Trying to control LED..."
    case $LED_STATE in
        "off")
            echo "Setting to OFF"
            {
                # Try different methods to set the LED
                echo none > $LED_PATH/trigger 2>/dev/null || true
                echo 0 > $LED_PATH/brightness 2>/dev/null || true
                
                # Alternative approach using sysfs files directly
                if [ -e "/sys/class/leds/$(basename $LED_PATH)/trigger" ]; then
                    echo none > /sys/class/leds/$(basename $LED_PATH)/trigger 2>/dev/null || true
                    echo 0 > /sys/class/leds/$(basename $LED_PATH)/brightness 2>/dev/null || true
                fi
            }
            ;;
        "on")
            echo "Setting to ON"
            {
                echo none > $LED_PATH/trigger 2>/dev/null || true
                echo 1 > $LED_PATH/brightness 2>/dev/null || true
                
                # Alternative approach
                if [ -e "/sys/class/leds/$(basename $LED_PATH)/trigger" ]; then
                    echo none > /sys/class/leds/$(basename $LED_PATH)/trigger 2>/dev/null || true
                    echo 1 > /sys/class/leds/$(basename $LED_PATH)/brightness 2>/dev/null || true
                fi
            }
            ;;
        "heartbeat")
            echo "Setting to HEARTBEAT mode"
            echo heartbeat > $LED_PATH/trigger 2>/dev/null || echo "Failed - trying alternative approach" 
            [ $? -ne 0 ] && echo heartbeat > /sys/class/leds/$(basename $LED_PATH)/trigger 2>/dev/null || true
            ;;
        "mmc")
            echo "Setting to MMC mode"
            echo mmc0 > $LED_PATH/trigger 2>/dev/null || echo "Failed - trying alternative approach"
            [ $? -ne 0 ] && echo mmc0 > /sys/class/leds/$(basename $LED_PATH)/trigger 2>/dev/null || true
            ;;
        "timer")
            echo "Setting to TIMER mode"
            echo timer > $LED_PATH/trigger 2>/dev/null || echo "Failed - trying alternative approach"
            [ $? -ne 0 ] && echo timer > /sys/class/leds/$(basename $LED_PATH)/trigger 2>/dev/null || true
            ;;
        *)
            echo "Invalid LED state: $LED_STATE"
            ;;
    esac
    
    # Check the current state
    echo "Current LED status (if readable):"
    cat $LED_PATH/trigger 2>/dev/null || echo "Can't read trigger"
    cat $LED_PATH/brightness 2>/dev/null || echo "Can't read brightness"
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

echo "LED control attempt completed"