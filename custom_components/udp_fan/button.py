from homeassistant.components.button import ButtonEntity

from .udp import send_udp
from .coordinator import devices


async def async_setup_entry(hass, entry, async_add_entities):
    mac = entry.data["mac"]
    async_add_entities([SpeedUpButton(mac), SpeedDownButton(mac)])


class SpeedUpButton(ButtonEntity):

    def __init__(self, mac):
        self._mac = mac

    @property
    def unique_id(self):
        return f"{self._mac}_speed_up"

    async def async_press(self):

        dev = devices.get(self._mac)
        if not dev:
            return

        ip = dev["ip"]

        await send_udp(ip, {"speedDelta": 1})


class SpeedDownButton(ButtonEntity):

    def __init__(self, mac):
        self._mac = mac

    @property
    def unique_id(self):
        return f"{self._mac}_speed_down"

    async def async_press(self):

        dev = devices.get(self._mac)
        if not dev:
            return

        ip = dev["ip"]

        await send_udp(ip, {"speedDelta": -1})
