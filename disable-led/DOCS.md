# Raspberry Pi LED Control

## Installation

1. Install the add-on
2. Start the add-on
3. Click "OPEN WEB UI" to access the controls

## How to use

### Auto Mode

When enabled (default), the LEDs will:

- Turn OFF when the add-on starts
- Turn ON when the add-on stops

### Manual Control

Use the web interface buttons to:

- Toggle individual LEDs
- Enable/disable all LEDs at once
- Toggle auto mode

## Troubleshooting

### Add-on fails to start

- Ensure the add-on has the required privileges
- Check that you're running on a Raspberry Pi
- Verify LED control files exist at `/sys/class/leds/`

### LEDs don't respond

- Check Home Assistant logs for permission errors
- Ensure the add-on is running with privileged access
- Verify your Raspberry Pi model is supported
