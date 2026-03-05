from homeassistant.components.light import LightEntity

from .udp import send_udp
from .coordinator import devices


async def async_setup_entry(hass, entry, async_add_entities):
    mac = entry.data["mac"]
    async_add_entities([FanLight(mac)])


class FanLight(LightEntity):

    def __init__(self, mac):

        self._mac = mac
        self._is_on = False

    @property
    def unique_id(self):
        return f"{self._mac}_light"

    async def async_turn_on(self, **kwargs):

        dev = devices.get(self._mac)
        if not dev:
            return

        ip = dev["ip"]

        await send_udp(ip, {"led": True})

        self._is_on = True

    async def async_turn_off(self, **kwargs):

        dev = devices.get(self._mac)
        if not dev:
            return

        ip = dev["ip"]

        await send_udp(ip, {"led": False})

        self._is_on = False
