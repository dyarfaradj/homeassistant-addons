# Raspberry Pi LED Control

This Home Assistant add-on allows you to control the power and activity LEDs on your Raspberry Pi.

## Features

- Control power LED (PWR/led0)
- Control activity LED (ACT/led1)
- Multiple modes available:
  - on: LED continuously on
  - off: LED completely off
  - heartbeat: LED pulses like a heartbeat
  - mmc: LED blinks on SD card activity
  - timer: LED blinks at a fixed rate

## Installation

1. Add this repository to your Home Assistant instance.
2. Install the "Raspberry Pi LED Control" add-on.
3. Configure the add-on with your preferred LED settings.
4. Start the add-on.

## Configuration

Example configuration:

```yaml
power_led: off
activity_led: heartbeat
```

### Options

| Option       | Description                       | Possible values                |
| ------------ | --------------------------------- | ------------------------------ |
| power_led    | Control mode for the power LED    | on, off, heartbeat, mmc, timer |
| activity_led | Control mode for the activity LED | on, off, heartbeat, mmc, timer |

## Support

If you have any issues or questions, please open an issue in the GitHub repository.

## Credits

This add-on is based on the Home Assistant Operating System PR [#2854](https://github.com/home-assistant/operating-system/pull/2854).
