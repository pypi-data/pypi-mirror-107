"""The |pydwf.core.api.analog_io| module implements a single class: |AnalogIO|."""

import ctypes

from typing import Tuple

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.auxiliary.enum_types import DwfAnalogIO
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class AnalogIO(DwfDevice_SubAPI):
    """The |AnalogIO| class provides access to the analog I/O functionality of a |DwfDevice:link|.

    The |AnalogIO| functions are used to control the power supplies, reference voltage supplies, voltmeters, ammeters,
    thermometers, and any other sensors on the device. These are organized into channels which contain a number of
    nodes. For instance, a power supply channel might have three nodes: an enable setting, a voltage level
    setting/reading, and current limitation setting/reading.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its public
        |analogIO:link| attribute for access by the user.
    """

    def reset(self) -> None:
        """Reset and configure all AnalogIO instrument parameters to default values.

        If auto-configure is enabled, the changes take immediate effect.
        """
        result = self.lib.FDwfAnalogIOReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def configure(self) -> None:
        """Configure the AnalogIO instrument."""
        result = self.lib.FDwfAnalogIOConfigure(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def status(self) -> None:
        """Read the status of the device and stores it internally.

        The following status functions will return the information that was read from the device
        when this function was last called.
        """
        result = self.lib.FDwfAnalogIOStatus(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def enableInfo(self) -> Tuple[bool, bool]:
        """Verify if Master Enable Setting and/or Master Enable Status are supported for the AnalogIO instrument.

        The Master Enable setting is essentially a software switch that "enables" or "turns on" the AnalogIO channels.
        If supported, the status of this Master Enable switch (Enabled/Disabled) can be queried by calling the
        :py:meth:`enableStatus` method.
        """
        c_set_supported = typespec_ctypes.c_int()
        c_status_supported = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogIOEnableInfo(self.hdwf, c_set_supported, c_set_supported)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        set_supported = bool(c_set_supported.value)
        status_supported = bool(c_status_supported.value)
        return (set_supported, status_supported)

    def enableSet(self, master_enable: bool) -> None:
        """Set the master enable switch."""
        result = self.lib.FDwfAnalogIOEnableSet(self.hdwf, master_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def enableGet(self) -> bool:
        """Return the current state of the master enable switch. This is not obtained from the device."""
        c_master_enable = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogIOEnableGet(self.hdwf, c_master_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        master_enable = bool(c_master_enable.value)
        return master_enable

    def enableStatus(self) -> bool:
        """Return the master enable status (if the device supports it).

        This can be a switch on the board or an over-current protection circuit state."""
        c_master_enable_status = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogIOEnableStatus(self.hdwf, c_master_enable_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        master_enable_status = bool(c_master_enable_status.value)
        return master_enable_status

    def channelCount(self) -> int:
        """Return the number of AnalogIO channels available on the device."""
        c_channel_count = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogIOChannelCount(self.hdwf, c_channel_count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        channel_count = c_channel_count.value
        return channel_count

    def channelName(self, channel_index: int) -> Tuple[str, str]:
        """Return the name (long text) and label (short text, printed on the device) for a channel."""
        c_channel_name = ctypes.create_string_buffer(32)
        c_channel_label = ctypes.create_string_buffer(16)
        result = self.lib.FDwfAnalogIOChannelName(
            self.hdwf,
            channel_index,
            c_channel_name,
            c_channel_label)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        channel_name = c_channel_name.value.decode()
        channel_label = c_channel_label.value.decode()
        return (channel_name, channel_label)

    def channelInfo(self, channel_index: int) -> int:
        """Return the number of nodes associated with the specified channel."""
        c_node_count = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogIOChannelInfo(self.hdwf, channel_index, c_node_count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        return c_node_count.value

    def channelNodeName(self, channel_index: int, node_index: int) -> Tuple[str, str]:
        """Return the node name ("Voltage", "Current", ...) and units ("V", "A") for an Analog I/O node."""
        c_node_name = ctypes.create_string_buffer(32)
        c_node_units = ctypes.create_string_buffer(16)
        result = self.lib.FDwfAnalogIOChannelNodeName(
            self.hdwf,
            channel_index,
            node_index,
            c_node_name,
            c_node_units)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        node_name = c_node_name.value.decode()
        node_units = c_node_units.value.decode()
        return (node_name, node_units)

    def channelNodeInfo(self, channel_index: int, node_index: int) -> DwfAnalogIO:
        """Return the supported channel node modes."""
        c_analog_io = typespec_ctypes.ANALOGIO()
        result = self.lib.FDwfAnalogIOChannelNodeInfo(
            self.hdwf,
            channel_index,
            node_index,
            c_analog_io)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        analog_io = DwfAnalogIO(c_analog_io.value)
        return analog_io

    def channelNodeSetInfo(self, channel_index: int, node_index: int) -> Tuple[float, float, int]:
        """Return node value limits.

        Since a Node can represent many things (Power supply, Temperature sensor, etc.),
        the Minimum, Maximum, and Steps parameters also represent different types of values.

        The (Maximum - Minimum) / Steps is the step size.

        *FDwfAnalogIOChannelNodeInfo* returns the type of values to expect and *FDwfAnalogIOChannelNodeName*
        returns the units of these values.
        """
        c_min_value = typespec_ctypes.c_double()
        c_max_value = typespec_ctypes.c_double()
        c_num_steps = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogIOChannelNodeSetInfo(
            self.hdwf,
            channel_index,
            node_index,
            c_min_value,
            c_max_value,
            c_num_steps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        min_value = c_min_value.value
        max_value = c_max_value.value
        num_steps = c_num_steps.value
        return (min_value, max_value, num_steps)

    def channelNodeSet(self, channel_index: int, node_index: int, node_value: float) -> None:
        """Set the node value for the specified node on the specified channel."""
        result = self.lib.FDwfAnalogIOChannelNodeSet(
            self.hdwf,
            channel_index,
            node_index,
            node_value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def channelNodeGet(self, channel_index: int, node_index: int) -> float:
        """Return the currently set value of the node on the specified channel."""
        c_node_value = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogIOChannelNodeGet(
            self.hdwf,
            channel_index,
            node_index,
            c_node_value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        node_value = c_node_value.value
        return node_value

    def channelNodeStatusInfo(self, channel_index: int, node_index: int) -> Tuple[float, float, int]:
        """Return the range of reading values available for the specified node on the specified channel."""
        c_min_value = typespec_ctypes.c_double()
        c_max_value = typespec_ctypes.c_double()
        c_num_steps = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogIOChannelNodeStatusInfo(
            self.hdwf,
            channel_index,
            node_index,
            c_min_value,
            c_max_value,
            c_num_steps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        min_value = c_min_value.value
        max_value = c_max_value.value
        num_steps = c_num_steps.value
        return (min_value, max_value, num_steps)

    def channelNodeStatus(self, channel_index: int, node_index: int) -> float:
        """Return the value reading of the node."""
        c_node_status = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogIOChannelNodeStatus(
            self.hdwf,
            channel_index,
            node_index,
            c_node_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        node_status = c_node_status.value
        return node_status
