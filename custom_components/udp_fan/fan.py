from homeassistant.components.fan import FanEntity, FanEntityFeature

from .udp import send_udp
from .coordinator import devices


async def async_setup_entry(hass, entry, async_add_entities):
    mac = entry.data["mac"]
    async_add_entities([UDPFan(mac)])


class UDPFan(FanEntity):

    _attr_supported_features = FanEntityFeature.SET_SPEED

    def __init__(self, mac):

        self._mac = mac
        self._speed = 0
        self._is_on = False

    @property
    def unique_id(self):
        return f"{self._mac}_fan"

    @property
    def device_info(self):

        return {
            "identifiers": {("udp_fan", self._mac)},
            "name": "UDP Smart Fan",
            "manufacturer": "UDP",
        }

    @property
    def available(self):

        dev = devices.get(self._mac)

        if not dev:
            return False

        return dev["available"]

    async def async_turn_on(self, percentage=None, **kwargs):

        dev = devices.get(self._mac)
        if not dev:
            return

        ip = dev["ip"]

        await send_udp(ip, {"power": True})

        self._is_on = True

        if percentage:
            await self.async_set_percentage(percentage)

    async def async_turn_off(self, **kwargs):

        dev = devices.get(self._mac)
        if not dev:
            return

        ip = dev["ip"]

        await send_udp(ip, {"power": False})

        self._is_on = False

    async def async_set_percentage(self, percentage):

        dev = devices.get(self._mac)
        if not dev:
            return

        ip = dev["ip"]

        speed = round((percentage / 100) * 6)

        if speed == 0:
            speed = 1

        await send_udp(ip, {"speed": speed})

        self._speed = percentage
