#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Raspberry Pi LED Control
# Runs the LED control script
# ==============================================================================
set -e

CONFIG_PATH=/data/options.json

# Get settings from configuration
POWER_LED=$(jq --raw-output ".power_led" $CONFIG_PATH)
ACTIVITY_LED=$(jq --raw-output ".activity_led" $CONFIG_PATH)

bashio::log.info "Starting Raspberry Pi LED Control add-on"
bashio::log.info "Power LED set to: ${POWER_LED}"
bashio::log.info "Activity LED set to: ${ACTIVITY_LED}"

# Run the LED control script with the provided settings
/usr/bin/led-control.sh "${POWER_LED}" "${ACTIVITY_LED}"

# Keep the add-on running
tail -f /dev/null