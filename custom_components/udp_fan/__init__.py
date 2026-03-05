import asyncio
import time

from .const import DEVICE_TIMEOUT
from .coordinator import devices, start_discovery


async def async_setup(hass, config):

    await start_discovery(hass)

    hass.async_create_task(monitor_devices())

    return True


async def async_setup_entry(hass, entry):

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(
            entry,
            ["fan", "light", "switch", "select", "button", "sensor"],
        )
    )

    return True


async def monitor_devices():

    while True:

        now = time.time()

        for mac in devices:

            if now - devices[mac]["last_seen"] > DEVICE_TIMEOUT:
                devices[mac]["available"] = False

        await asyncio.sleep(5)
