from homeassistant.components.select import SelectEntity

from .udp import send_udp
from .const import TIMER_OPTIONS
from .coordinator import devices


async def async_setup_entry(hass, entry, async_add_entities):
    mac = entry.data["mac"]
    async_add_entities([TimerSelect(mac)])


class TimerSelect(SelectEntity):

    _attr_options = list(TIMER_OPTIONS.keys())

    def __init__(self, mac):

        self._mac = mac
        self._current = "Off"

    @property
    def unique_id(self):
        return f"{self._mac}_timer"

    async def async_select_option(self, option):

        dev = devices.get(self._mac)
        if not dev:
            return

        ip = dev["ip"]

        await send_udp(ip, {"timer": TIMER_OPTIONS[option]})

        self._current = option
