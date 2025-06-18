import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_URL
from .const import DOMAIN, DEFAULT_INTERVAL_HOURS

CONF_INTERVAL_HOURS = "interval_hours"

class LgDevSessionConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="LG Dev Session Auto Renew", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_URL): str,
                vol.Optional(CONF_INTERVAL_HOURS, default=DEFAULT_INTERVAL_HOURS): int
            }),
            errors=errors
        )
