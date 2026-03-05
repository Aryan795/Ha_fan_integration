import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN


class UDPFanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):

        if user_input is not None:

            mac = user_input["mac"]
            ip = user_input["ip"]

            await self.async_set_unique_id(mac)

            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"UDP Fan {mac}",
                data={"mac": mac, "ip": ip},
            )

        schema = vol.Schema(
            {
                vol.Required("mac"): str,
                vol.Required("ip"): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_discovery(self, discovery_info):

        mac = discovery_info["mac"]
        ip = discovery_info["ip"]

        await self.async_set_unique_id(mac)

        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"UDP Fan {mac}",
            data={"mac": mac, "ip": ip},
        )
