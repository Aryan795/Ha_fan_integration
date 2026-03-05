from homeassistant.components.select import SelectEntity

from .udp import send_udp
from .const import TIMER_OPTIONS


class TimerSelect(SelectEntity):

    _attr_options = list(TIMER_OPTIONS.keys())

    def __init__(self, ip):

        self._ip = ip
        self._current = "Off"

    async def async_select_option(self, option):

        send_udp(self._ip, {"timer": TIMER_OPTIONS[option]})

        self._current = option
