#!/usr/bin/with-contenv bashio

bashio::log.info "Setting up LED permissions..."

# Try to remount /sys as read-write
mount -o remount,rw /sys || bashio::log.warning "Could not remount /sys as read-write"

# Try different LED path patterns and set permissions
for pattern in /sys/class/leds/{PWR,ACT,pwr,act,led0,led1}/brightness; do
    if [ -e "$pattern" ]; then
        bashio::log.info "Setting permissions for $pattern"
        chmod 666 "$pattern" || bashio::log.warning "Could not set permissions for $pattern"
        chown root:gpio "$pattern" 2>/dev/null || true
    fi
done

# Create gpio group if it doesn't exist and add our user
if ! getent group gpio >/dev/null; then
    groupadd gpio
fi
usermod -a -G gpio $(whoami)

# Start the Python script
python3 /run.py