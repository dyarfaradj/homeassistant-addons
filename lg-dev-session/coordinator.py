from datetime import timedelta
import logging
import aiohttp
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class LgDevSessionCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry
        self.url = entry.data[CONF_URL]
        self.interval_hours = entry.data.get("interval_hours", 48)

        super().__init__(
            hass,
            _LOGGER,
            name="LG Dev Session Coordinator",
            update_interval=timedelta(hours=self.interval_hours)
        )

    async def _async_update_data(self):
        _LOGGER.info("[LG Dev Session] Starting auto-renew call to %s", self.url)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as resp:
                    data = await resp.text()
                    _LOGGER.info("[LG Dev Session] Response: %s", data)
        except Exception as e:
            _LOGGER.error("[LG Dev Session] Error while calling URL: %s", e)
        return {}