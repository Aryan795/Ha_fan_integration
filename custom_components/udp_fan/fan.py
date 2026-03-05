from homeassistant.components.fan import FanEntity, FanEntityFeature

from .udp import send_udp


class UDPFan(FanEntity):

    _attr_supported_features = FanEntityFeature.SET_SPEED

    def __init__(self, ip):

        self._ip = ip
        self._is_on = False
        self._speed = 0

    @property
    def name(self):
        return "Smart UDP Fan"

    @property
    def percentage(self):
        return self._speed

    async def async_turn_on(self, percentage=None, **kwargs):

        send_udp(self._ip, {"power": True})

        self._is_on = True

        if percentage:
            await self.async_set_percentage(percentage)

    async def async_turn_off(self, **kwargs):

        send_udp(self._ip, {"power": False})

        self._is_on = False

    async def async_set_percentage(self, percentage):

        speed = round((percentage / 100) * 6)

        if speed == 0:
            speed = 1

        send_udp(self._ip, {"speed": speed})

        self._speed = percentage
