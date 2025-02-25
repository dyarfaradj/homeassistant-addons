#!/usr/bin/with-contenv bashio

bashio::log.info "Setting up LED permissions..."

# Try to remount /sys as read-write
sudo mount -o remount,rw /sys || bashio::log.warning "Could not remount /sys as read-write"

# Create gpio group if it doesn't exist and add our user
if ! getent group gpio >/dev/null; then
    sudo groupadd gpio
fi
sudo usermod -a -G gpio $(whoami)

# Start the Python script
sudo python3 /run.py