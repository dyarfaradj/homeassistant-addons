#!/usr/bin/with-contenv bashio

bashio::log.info "Setting up LED permissions..."

# Try to remount /sys as read-write
mount -o remount,rw /sys || bashio::log.warning "Could not remount /sys as read-write"

# Set permissions for LED controls
for led in PWR ACT pwr act led0 led1; do
    if [ -e "/sys/class/leds/$led/brightness" ]; then
        chmod 666 "/sys/class/leds/$led/brightness" || bashio::log.warning "Could not set permissions for $led"
    fi
done

# Start the Python script
python3 /run.py