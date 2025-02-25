# Raspberry Pi LED Control

A Home Assistant add-on to control the Raspberry Pi's onboard LEDs through a simple web interface.

## Features

- Turn off and on the Power and Activity LEDs individually
- Enable "Auto Mode" to automatically disable LEDs when add-on starts and restore when it stops
- Simple web UI accessible through Home Assistant

## Installation

1. Add this repository to your Home Assistant instance
2. Install the "Raspberry Pi LED Control" add-on
3. Start the add-on
4. Open the web UI through the ingress link

## Usage

- **Auto Mode**: When enabled, LEDs turn off when the add-on starts and turn back on when it stops
- **Power LED**: Toggle the red power LED (LED1)
- **Activity LED**: Toggle the green activity LED (LED0)
- **Enable/Disable All**: Quick buttons to control both LEDs simultaneously

## Permissions

This add-on requires privileged access to control the Raspberry Pi hardware. The required permissions are automatically configured in the `config.json` file.

## Support

If you encounter any issues or have questions, please open an issue in the GitHub repository.
