# LG Dev Session Auto Renew

![Supports aarch64 Architecture][aarch64-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports armhf Architecture][armhf-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports i386 Architecture][i386-shield]

This Home Assistant add-on automatically calls an LG Developer URL to renew Developer Mode sessions on your LG webOS TV.

## Features

- 🔄 Automatically renews LG webOS Developer Mode sessions
- ⏰ Configurable renewal interval (1-168 hours)
- 📊 Detailed logging of all renewal attempts
- 🚀 Easy setup through Home Assistant UI
- 🔧 No manual configuration files needed

## Installation

1. Navigate in your Home Assistant frontend to **Settings** → **Add-ons** → **Add-on Store**.
2. Click the 3-dots menu at upper right → **Repositories** and add this repository URL: `https://github.com/dyarfaradj/homeassistant-addons`
3. Click **Add** → **Close** and wait for the add-ons to load.
4. Find "LG Dev Session Auto Renew" and click **Install**.

## Configuration

Example configuration:

```yaml
url: "https://developer.lge.com/secure/ResetDevModeSession.dev?sessionToken=YOUR_TOKEN"
interval_hours: 48
```

### Options

| Option           | Description                          | Required | Default |
| ---------------- | ------------------------------------ | -------- | ------- |
| `url`            | The LG Developer session URL to call | Yes      | -       |
| `interval_hours` | Renewal interval in hours (1-168)    | No       | 48      |

### Getting your Session URL

1. Go to [LG Developer](https://developer.lge.com/) and sign in
2. Navigate to your Developer Mode management page
3. Find the session renewal URL (usually contains a sessionToken parameter)
4. Copy the complete URL and paste it into the add-on configuration

## Usage

1. After installation, go to **Settings** → **Add-ons** → **LG Dev Session Auto Renew**
2. Click **Configuration**
3. Enter your LG Developer session URL
4. Set your preferred renewal interval (default: 48 hours)
5. Click **Save** and then **Start**

The add-on will immediately attempt an initial renewal and then continue to renew your session at the specified interval.

## Logs

You can monitor the add-on's activity in the **Log** tab. The add-on logs:

- Successful session renewals
- Failed renewal attempts with error details
- Configuration changes
- Scheduled renewal times

## Troubleshooting

### Common Issues

**Invalid URL Error**: Make sure your URL starts with `http://` or `https://` and includes the complete session token.

**Network Errors**: Check your Home Assistant's internet connection and ensure the LG Developer website is accessible.

**Session Token Expired**: If renewals consistently fail, you may need to get a new session URL from the LG Developer website.

## Support

If you have any issues or questions, please open an issue in the [GitHub repository](https://github.com/dyarfaradj/homeassistant-addons).

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
