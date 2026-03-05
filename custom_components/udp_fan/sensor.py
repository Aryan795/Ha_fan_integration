"""Sensor platform for the UDP Fan integration."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_DEVICE_ID,
    CONF_NAME,
    DEFAULT_NAME,
    DOMAIN,
    STATUS_RSSI,
    STATUS_SPEED,
)
from .coordinator import UDPFanCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class UDPFanSensorEntityDescription(SensorEntityDescription):
    """Description for a UDP fan sensor entity."""

    status_key: str


SENSOR_DESCRIPTIONS: tuple[UDPFanSensorEntityDescription, ...] = (
    UDPFanSensorEntityDescription(
        key="speed",
        name="Fan Speed",
        icon="mdi:fan",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
        status_key=STATUS_SPEED,
    ),
    UDPFanSensorEntityDescription(
        key="rssi",
        name="Signal Strength",
        icon="mdi:wifi",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        status_key=STATUS_RSSI,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up UDP fan sensor entities."""
    coordinator: UDPFanCoordinator = hass.data[DOMAIN][entry.entry_id]
    name = entry.data.get(CONF_NAME, DEFAULT_NAME)
    device_id = entry.data[CONF_DEVICE_ID]

    async_add_entities(
        UDPFanSensor(coordinator, name, device_id, entry.entry_id, description)
        for description in SENSOR_DESCRIPTIONS
    )


class UDPFanSensor(CoordinatorEntity[UDPFanCoordinator], SensorEntity):
    """Representation of a UDP fan sensor."""

    entity_description: UDPFanSensorEntityDescription

    def __init__(
        self,
        coordinator: UDPFanCoordinator,
        fan_name: str,
        device_id: str,
        entry_id: str,
        description: UDPFanSensorEntityDescription,
    ) -> None:
        """Initialize the sensor entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = f"{fan_name} {description.name}"
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._device_id = device_id

    @property
    def native_value(self) -> int | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.status_key)
