from homeassistant.components.switch import SwitchEntity

from .udp import send_udp


class SleepModeSwitch(SwitchEntity):

    def __init__(self, ip):

        self._ip = ip
        self._state = False

    async def async_turn_on(self):

        send_udp(self._ip, {"sleep": True})

        self._state = True

    async def async_turn_off(self):

        send_udp(self._ip, {"sleep": False})

        self._state = False
