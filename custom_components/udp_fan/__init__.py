from .const import DOMAIN
from .coordinator import start_listener


async def async_setup_entry(hass, entry):

    start_listener(hass)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(
            entry,
            ["fan", "light", "switch", "select"],
        )
    )

    return True
