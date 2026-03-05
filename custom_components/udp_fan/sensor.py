from homeassistant.components.sensor import SensorEntity

from .coordinator import devices


async def async_setup_entry(hass, entry, async_add_entities):
    mac = entry.data["mac"]
    async_add_entities([FanStatusSensor(mac)])


class FanStatusSensor(SensorEntity):

    def __init__(self, mac):
        self._mac = mac

    @property
    def unique_id(self):
        return f"{self._mac}_status"

    @property
    def name(self):
        return "Fan Status"

    @property
    def state(self):

        dev = devices.get(self._mac)

        if not dev:
            return "offline"

        return "online" if dev["available"] else "offline"
