"""Device update listener."""

import logging
from ipaddress import IPv4Address
from typing import Any, Mapping, Optional

from async_upnp_client import UpnpAdvertisementListener, UpnpDevice, UpnpFactory

_LOGGER = logging.getLogger(__name__)


class DeviceUpdater:
    """
    Device updater.

    Listens for SSDP advertisements and updates device inline when needed.
    Inline meaning that it keeps the original UpnpDevice instance.
    So be sure to keep only references to the UpnpDevice,
    as a device might decide to remove a service after an update!
    """

    def __init__(
        self,
        device: UpnpDevice,
        factory: UpnpFactory,
        source_ip: Optional[IPv4Address] = None,
    ) -> None:
        """Initialize."""
        self._device = device
        self._factory = factory
        self._listener = UpnpAdvertisementListener(
            on_alive=self._on_alive,
            on_byebye=self._on_byebye,
            on_update=self._on_update,
            source_ip=source_ip,
        )

    async def async_start(self) -> None:
        """Start listening for notifications."""
        _LOGGER.debug("Start listening for notifications.")
        await self._listener.async_start()

    async def async_stop(self) -> None:
        """Stop listening for notifications."""
        _LOGGER.debug("Stop listening for notifications.")
        await self._listener.async_stop()

    async def _on_alive(self, data: Mapping[str, str]) -> None:
        """Handle on alive."""
        # Ensure for root devices only.
        if data.get("nt") != "upnp:rootdevice":
            return

        # Ensure for our device.
        if data.get("_udn") != self._device.udn:
            return

        _LOGGER.debug("Handling alive: %s", data)
        await self._async_handle_alive_update(data)

    async def _on_byebye(self, data: Mapping[str, Any]) -> None:
        """Handle on byebye."""
        _LOGGER.debug("Handling on_byebye: %s", data)
        self._device.available = False

    async def _on_update(self, data: Mapping[str, Any]) -> None:
        """Handle on update."""
        # Ensure for root devices only.
        if data.get("nt") != "upnp:rootdevice":
            return

        # Ensure for our device.
        if data.get("_udn") != self._device.udn:
            return

        _LOGGER.debug("Handling update: %s", data)
        await self._async_handle_alive_update(data)

    async def _async_handle_alive_update(self, data: Mapping[str, str]) -> None:
        """Handle on_alive or on_update."""
        do_reinit = False

        # Handle BOOTID.UPNP.ORG.
        boot_id = data.get("BOOTID.UPNP.ORG")
        if boot_id and boot_id != self._device.boot_id:
            _LOGGER.debug(
                "New boot_id: %s, old boot_id: %s", boot_id, self._device.boot_id
            )
            do_reinit = True

        # Handle CONFIGID.UPNP.ORG.
        config_id = data.get("CONFIGID.UPNP.ORG")
        if config_id and config_id != self._device.config_id:
            _LOGGER.debug(
                "New config_id: %s, old config_id: %s",
                config_id,
                self._device.config_id,
            )
            do_reinit = True

        # Handle LOCATION.
        location = data.get("LOCATION")
        if location and self._device.device_url != location:
            _LOGGER.debug(
                "New location: %s, old location: %s", location, self._device.device_url
            )
            do_reinit = True

        if location and do_reinit:
            await self._reinit_device(location, boot_id, config_id)

        # We heard from it, so mark it available.
        self._device.available = True

    async def _reinit_device(
        self, location: str, boot_id: Optional[str], config_id: Optional[str]
    ) -> None:
        """Reinitialize device."""
        # pylint: disable=protected-access
        _LOGGER.debug("Reinitializing device")

        new_device = await self._factory.async_create_device(location)

        self._device._device_info = new_device._device_info

        # Copy new services and update the binding between the original device and new services.
        self._device.services = new_device.services
        for service in self._device.services.values():
            service.device = self._device

        self._device.boot_id = boot_id
        self._device.config_id = config_id
