"""Config flow for Sporza Calendar integration."""

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN


class SporzaCalendarConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sporza Calendar."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title="Sporza Calendar",
                data={},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={},
        )
