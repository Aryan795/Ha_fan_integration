from homeassistant.components.light import LightEntity

from .udp import send_udp


class FanLight(LightEntity):

    def __init__(self, ip):

        self._ip = ip
        self._is_on = False

    async def async_turn_on(self, **kwargs):

        send_udp(self._ip, {"led": True})

        self._is_on = True

    async def async_turn_off(self, **kwargs):

        send_udp(self._ip, {"led": False})

        self._is_on = False
