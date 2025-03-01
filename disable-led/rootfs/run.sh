#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Raspberry Pi LED Control
# Runs the LED control script
# ==============================================================================
set -e

bashio::log.info "Starting Raspberry Pi LED Control add-on"

# Check if we're running on a supported platform
if [ ! -d "/sys/class/leds" ]; then
    bashio::log.error "LED control paths not found. This add-on may only work on Raspberry Pi hardware."
    bashio::log.warning "Will continue execution for debug purposes."
fi

bashio::log.info "Loading configuration options..."
CONFIG_PATH=/data/options.json

# Log contents of the config file for debugging
bashio::log.debug "Config file contents:"
cat $CONFIG_PATH

# Get settings from configuration with error handling
if jq -e . "$CONFIG_PATH" >/dev/null 2>&1; then
    POWER_LED=$(jq --raw-output ".power_led" $CONFIG_PATH)
    ACTIVITY_LED=$(jq --raw-output ".activity_led" $CONFIG_PATH)
    
    bashio::log.info "Configuration loaded successfully"
    bashio::log.info "Power LED set to: ${POWER_LED}"
    bashio::log.info "Activity LED set to: ${ACTIVITY_LED}"
else
    bashio::log.error "Failed to parse JSON configuration"
    POWER_LED="on"
    ACTIVITY_LED="on"
    bashio::log.warning "Using default settings: Power LED=on, Activity LED=on"
fi

# Check if led-control.sh exists and is executable
if [ ! -f "/usr/bin/led-control.sh" ]; then
    bashio::log.error "LED control script not found at /usr/bin/led-control.sh"
    exit 1
fi

if [ ! -x "/usr/bin/led-control.sh" ]; then
    bashio::log.warning "LED control script not executable, fixing permissions"
    chmod +x /usr/bin/led-control.sh
fi

# Run the LED control script with the provided settings
bashio::log.info "Executing LED control script..."
/usr/bin/led-control.sh "${POWER_LED}" "${ACTIVITY_LED}" || bashio::log.error "LED control script failed"

bashio::log.info "LED control script completed"
bashio::log.info "Add-on will remain running to maintain LED settings"

# Keep the add-on running
bashio::log.info "Entering maintenance mode"
while true; do
    sleep 3600 & wait $!
done