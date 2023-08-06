"""Implementation of the |pydwf.utilities.open_dwf_device| function."""

from typing import Optional, Callable

from pydwf.core.dwf_library import DwfLibrary
from pydwf.core.dwf_device import DwfDevice
from pydwf.core.auxiliary.enum_types import DwfEnumConfigInfo, DwfEnumFilter
from pydwf.core.auxiliary.exceptions import PyDwfError


def open_dwf_device(dwf: DwfLibrary, serial_number: Optional[str] = None,
                    configuration_fitness_func: Optional[Callable] = None,
                    enum_filter: Optional[DwfEnumFilter] = None) -> DwfDevice:
    """Open a device identified by its serial number, optionally selecting a preferred configuration.

    Note:
        This method takes several seconds to complete.

    Parameters:
        dwf (DwfLibrary): The |DwfLibrary:link| used to open the device.
        serial_number (str): The serial number of the device to be opened.
            Digilent Waveforms device serial numbers consist of 12 hexadecimal digits.
        configuration_fitness_func (Callable):
            A function to select the preferred configuration of the selected device.
        enum_filter (Optional[DwfEnumFilter]):
            An optional filter to limit the device enumeration to certain device types.
            In None, enumerate all devices.

    Returns:
        DwfDevice: The |DwfDevice:link| created as a result of this call.

    Raises:
        PyDwfError: could not select a unique candidate device.
    """

    if enum_filter is None:
        enum_filter = DwfEnumFilter.All

    # The dwf.deviceEnum.enumerateDevices() function builds an internal table of connected devices
    # that can be queried using other dwf.deviceEnum methods.
    num_devices = dwf.deviceEnum.enumerateDevices(enum_filter)

    # We do the explicit conversion to list to make sure the variable is a list of integers, not a range.
    candidate_devices = list(range(num_devices))

    if serial_number is not None:

        candidate_devices = [device_index for device_index in candidate_devices
                             if dwf.deviceEnum.serialNumber(device_index) == serial_number]

        if len(candidate_devices) == 0:
            raise PyDwfError("No Digilent Waveforms device found in device class '{}' with serial number '{}'.".format(
                enum_filter.name, serial_number))

        if len(candidate_devices) > 1:
            # Multiple devices found with a matching serial number; this should not happen!
            raise PyDwfError("Multiple Digilent Waveforms devices found with serial number '{}'.".format(
                serial_number))

    else:

        if len(candidate_devices) == 0:
            raise PyDwfError("No Digilent Waveforms devices found in device class '{}'.".format(enum_filter.name))

        if len(candidate_devices) > 1:
            raise PyDwfError(
                "Multiple Digilent Waveforms devices found (serial numbers: {});"
                " specify a serial number to select one.".format(
                    ", ".join(dwf.deviceEnum.serialNumber(device_index) for device_index in candidate_devices)))

    # We now have a single candidate device left.

    assert len(candidate_devices) == 1

    device_index = candidate_devices[0]

    if configuration_fitness_func is None:
        # If no 'configuration_fitness_func' was specified, just return the first one.
        return dwf.deviceControl.open(device_index)

    # The caller specified a 'configuration_fitness_func'.
    # We will examine all configuration and pick the one that has the highest fitness.

    num_config = dwf.deviceEnum.enumerateConfigurations(device_index)

    best_configuration_index = None
    best_configuration_fitness = None

    for configuration_index in range(num_config):

        configuration_info = {
            configuration_parameter.name:
                dwf.deviceEnum.configInfo(configuration_index, configuration_parameter)
            for configuration_parameter in DwfEnumConfigInfo}

        configuration_fitness = configuration_fitness_func(configuration_info)

        if best_configuration_index is None or configuration_fitness > best_configuration_fitness:
            best_configuration_index = configuration_index
            best_configuration_fitness = configuration_fitness

    return dwf.deviceControl.open(device_index, best_configuration_index)
