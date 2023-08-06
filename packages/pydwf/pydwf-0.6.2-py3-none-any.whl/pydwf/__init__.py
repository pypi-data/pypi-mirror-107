"""This package provides classes, types, and functions to control Digilent measurement and test devices."""

# The version number of the *pydwf* package.
__version__ = "0.6.2"

# The *DwfLibrary* type is the only type users need to access library functionality.
from pydwf.core.dwf_library import DwfLibrary

# Import the 24 enumeration types and make them available for import directly from the *pydwf* package.
from pydwf.core.auxiliary.enum_types import (
    DwfEnumFilter, DwfDeviceID, DwfDeviceVersion, DwfTriggerSource,
    DwfState, DwfEnumConfigInfo, DwfAcquisitionMode, DwfAnalogInFilter,
    DwfTriggerType, DwfTriggerSlope, DwfTriggerLength, DwfErrorCode,
    DwfAnalogOutFunction, DwfAnalogIO, DwfAnalogOutNode, DwfAnalogOutMode,
    DwfAnalogOutIdle, DwfDigitalInClockSource, DwfDigitalInSampleMode, DwfDigitalOutOutput,
    DwfDigitalOutType, DwfDigitalOutIdle, DwfAnalogImpedance, DwfParameter)

# Import the two exception classes and make them available for import directly from the *pydwf* package.
from pydwf.core.auxiliary.exceptions import PyDwfError, DwfLibraryError
