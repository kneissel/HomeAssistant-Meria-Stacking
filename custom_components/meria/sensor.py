from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity import Entity
from homeassistant import config_entries

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    staking_entities = []

    api_client = hass.data[DOMAIN][entry.entry_id]

    # Utilisez api_client pour créer des entités ou effectuer d'autres opérations.
    stakings_data = await api_client.stakings()

    for staking_data in stakings_data:
        staking_entity = MeriaStakingSensor(entry.entry_id, staking_data)
        staking_entities.append(staking_entity)

    async_add_entities(staking_entities, True)


class MeriaStakingSensor(SensorEntity):
    def __init__(self, entry_id, staking_data) -> None:
        self._entry_id = entry_id
        self._staking_data = staking_data
        self._state = STATE_UNKNOWN

    @property
    def name(self):
        return f"Staking {self._staking_data['currencyCode']}"

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"staking_{self._staking_data['currencyCode']}"

    @property
    def device_class(self):
        return SensorDeviceClass.MONETARY

    @property
    def state_class(self):
        return SensorStateClass.MEASUREMENT

    @property
    def unit_of_measurement(self):
        return self._staking_data["currencyCode"]

    async def async_update(self):
        api_client = self.hass.data[DOMAIN][self._entry_id]

        try:
            # Appelez la méthode pour obtenir les dernières données du staking
            new_data = await api_client.staking(self._staking_data["currencyCode"])

            # Mettez à jour l'état de l'entité en fonction des nouvelles données
            self._state = new_data["amount"]

        except Exception as e:  # pylint: disable=broad-except
            # Gérer les erreurs de mise à jour ici (par exemple, journaliser l'erreur)
            self._state = STATE_UNKNOWN
