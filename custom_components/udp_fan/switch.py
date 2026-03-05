from homeassistant.components.switch import SwitchEntity

from .udp import send_udp
from .coordinator import devices


async def async_setup_entry(hass, entry, async_add_entities):
    mac = entry.data["mac"]
    async_add_entities([SleepSwitch(mac)])


class SleepSwitch(SwitchEntity):

    def __init__(self, mac):

        self._mac = mac
        self._state = False

    @property
    def unique_id(self):
        return f"{self._mac}_sleep"

    async def async_turn_on(self):

        dev = devices.get(self._mac)
        if not dev:
            return

        ip = dev["ip"]

        await send_udp(ip, {"sleep": True})

        self._state = True

    async def async_turn_off(self):

        dev = devices.get(self._mac)
        if not dev:
            return

        ip = dev["ip"]

        await send_udp(ip, {"sleep": False})

        self._state = False
