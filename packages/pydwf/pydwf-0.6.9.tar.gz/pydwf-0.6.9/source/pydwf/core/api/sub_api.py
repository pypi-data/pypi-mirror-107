"""This module implements the :py:class:`DwfLibrary_SubAPI` and :py:class:`DwfDevice_SubAPI` classes."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydwf.core.dwf_library import DwfLibrary
    from pydwf.core.dwf_device import DwfDevice


class DwfLibrary_SubAPI:
    """Abstract base class for the sub-API class members of a |DwfLibrary.short|."""
    def __init__(self, dwf: 'DwfLibrary'):
        self._dwf = dwf

    @property
    def dwf(self):
        """Return the library."""
        return self._dwf

    @property
    def lib(self):
        """Return the ctypes library."""
        return self.dwf.lib


class DwfDevice_SubAPI:
    """Abstract base class for the sub-API class members of a |DwfDevice.short|."""

    def __init__(self, device: 'DwfDevice'):
        self._device = device

    @property
    def device(self):
        """Return the device."""
        return self._device

    @property
    def hdwf(self):
        """Return the HDWF device handle."""
        return self.device.hdwf

    @property
    def dwf(self):
        """Return the library."""
        return self.device.dwf

    @property
    def lib(self):
        """Return the *ctypes* library."""
        return self.dwf.lib
