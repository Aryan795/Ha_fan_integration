# UDP Smart Fan (Atomberg)

A **local** Home Assistant integration for controlling **Atomberg smart fans** over your LAN using UDP.

> This is a custom integration (HACS-compatible). It is not part of Home Assistant Core.

## Features

- Fan entity
  - On/Off
  - Set speed (mapped to 6 speed steps)
- Light entity (fan LED)
- Switch entity (sleep mode)
- Select entity (timer)
- Local control (**no cloud**)

## Requirements

- Home Assistant **2024.6.0** or newer (per `hacs.json`)
- Fan reachable on your local network

## Installation

### Option A — HACS (recommended)

1. Open **HACS** in Home Assistant
2. Go to **Integrations** → **⋮** (top right) → **Custom repositories**
3. Add this repository URL and choose category **Integration**
4. Install **UDP Smart Fan**
5. Restart Home Assistant

### Option B — Manual

1. Copy `custom_components/udp_fan` into:

   `config/custom_components/udp_fan`

2. Restart Home Assistant

## Configuration

This integration uses the UI (Config Flow).

1. Go to **Settings → Devices & services → Add integration**
2. Search for **UDP Smart Fan**
3. Enter:
   - **Host**: Fan IP address
   - **Port**: UDP port (default in the form)
   - **Device ID**: Your fan's device id
   - **Name** (optional)

## Entities created

Depending on your fan/model and integration setup, you may see:

- `fan.<name>` — main fan control
- `light.<name>_light` — LED control
- `switch.<name>_sleep_mode` — sleep mode
- `select.<name>_timer` — timer
- `sensor.<name>_fan_speed` — speed (if enabled)
- `sensor.<name>_signal_strength` — RSSI (disabled by default)

## Troubleshooting

- Ensure your Home Assistant host can reach the fan IP on your LAN.
- If setup fails with *cannot_connect*, double-check **Host**, **Port**, and **Device ID**.
- If you use DHCP, consider reserving an IP for the fan in your router.

## Roadmap / ideas

- Auto-discovery of fans on the network
- Better device info (model, firmware, etc.)
- Translations and proper `strings.json`

## Credits

- Community inspiration from other local fan integrations

## Disclaimer

This project is not affiliated with Atomberg or Home Assistant.