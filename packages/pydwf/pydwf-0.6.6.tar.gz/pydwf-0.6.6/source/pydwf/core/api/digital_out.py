"""The |pydwf.core.api.digital_out| module implements a single class: |DigitalOut|."""

from typing import Tuple, List

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.enum_types import (DwfTriggerSource, DwfTriggerSlope, DwfDigitalOutOutput, DwfDigitalOutType,
                                             DwfState, DwfDigitalOutIdle)
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.auxiliary.exceptions import PyDwfError
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class DigitalOut(DwfDevice_SubAPI):
    """The |DigitalOut| class provides access to the DigitalOut (pattern generator) instrument of a |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its
        public |digitalOut:link| attribute for access by the user.
    """

    # pylint: disable=too-many-public-methods

    def reset(self) -> None:
        """Reset the digital-out instrument."""
        result = self.lib.FDwfDigitalOutReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def configure(self, start: bool) -> None:
        """Start or stop the digital-out instrument."""
        result = self.lib.FDwfDigitalOutConfigure(self.hdwf, start)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def status(self) -> DwfState:
        """Return the status of the digital-out instrument."""
        c_status = typespec_ctypes.DwfState()
        result = self.lib.FDwfDigitalOutStatus(self.hdwf, c_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        status_ = DwfState(c_status.value)
        return status_

    def internalClockInfo(self) -> float:
        """Get digital-out clock frequency.

        Returns:
            float: The digital-out clock frequency, in Hz.
        """
        c_internal_clock_frequency = typespec_ctypes.c_double()
        result = self.lib.FDwfDigitalOutInternalClockInfo(self.hdwf, c_internal_clock_frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        internal_clock_frequency = c_internal_clock_frequency.value
        return internal_clock_frequency

    def triggerSourceInfo(self) -> List[DwfTriggerSource]:
        """Get digital-out trigger source info.

        Note:
            This function is OBSOLETE. Use the generic DeviceControl.triggerInfo() method instead.

        Returns:
            List[DwfTriggerSource]: a list of possible choices for the trigger source.
        """
        c_trigger_source_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalOutTriggerSourceInfo(self.hdwf, c_trigger_source_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source_bitset = c_trigger_source_bitset.value
        trigger_source_list = [trigger_source for trigger_source in DwfTriggerSource
                               if trigger_source_bitset & (1 << trigger_source.value)]
        return trigger_source_list

    def triggerSourceSet(self, trigger_source: DwfTriggerSource) -> None:
        """Set the trigger source."""
        result = self.lib.FDwfDigitalOutTriggerSourceSet(self.hdwf, trigger_source.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSourceGet(self) -> DwfTriggerSource:
        """Get the currently active trigger source."""
        c_trigger_source = typespec_ctypes.TRIGSRC()
        result = self.lib.FDwfDigitalOutTriggerSourceGet(self.hdwf, c_trigger_source)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source = DwfTriggerSource(c_trigger_source.value)
        return trigger_source

    def runInfo(self) -> Tuple[float, float]:
        """Get minimal and maximal duration for a single digital-out pulse sequence run, in seconds.

        Returns:
            Tuple[float, float]: A tuple containing the minimal and maximal digital-out run duration, in seconds.
        """
        c_run_duration_min = typespec_ctypes.c_double()
        c_run_duration_max = typespec_ctypes.c_double()
        result = self.lib.FDwfDigitalOutRunInfo(self.hdwf, c_run_duration_min, c_run_duration_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        run_duration_min = c_run_duration_min.value
        run_duration_max = c_run_duration_max.value
        return (run_duration_min, run_duration_max)

    def runSet(self, run_duration: float) -> None:
        """Set duration for a single digital-out pulse sequence run, in seconds.

        Parameters:
            run_duration (float): Digital-out runtime, in seconds.

                The value 0 is special; it means *forever*.
        """
        result = self.lib.FDwfDigitalOutRunSet(self.hdwf, run_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def runGet(self) -> float:
        """Get duration for a single digital-out pulse sequence run, in seconds.

        Returns:
            float: digital-out run-time, in seconds.
        """
        c_run_duration = typespec_ctypes.c_double()
        result = self.lib.FDwfDigitalOutRunGet(self.hdwf, c_run_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        run_duration = c_run_duration.value
        return run_duration

    def runStatus(self) -> int:
        """Get run-time for the currently active digital-out pulse sequence run.

        This value is internally expressed as an integer with 48-bit resolution,
        and is measured in integer clock cycles. The C API returns it as a
        double-precision floating point number, to avoid using 64-bit integers.

        Use the :py:meth:`internalClockInfo` method to retrieve the clock frequency.

        Returns:
            int: The number of clock cycles until the nest state transition of the
                     DigitalOut instrument's state machine.
        """
        c_run_status = typespec_ctypes.c_double()
        result = self.lib.FDwfDigitalOutRunStatus(self.hdwf, c_run_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        if not c_run_status.value.is_integer():
            raise PyDwfError("FDwfDigitalOutRunStatus returned {}; an integer was expected.".format(c_run_status.value))
        run_status = int(c_run_status.value)
        return run_status

    def waitInfo(self) -> Tuple[float, float]:
        """Get minimal and maximal wait-time preceding digital-out pulse-sequence runs, in seconds.

        Returns:
            Tuple[float, float]: A tuple containing the minimal and maximal configurable wait durations that should
            precede a pulse-train output, expressed in seconds.
        """
        c_wait_duration_min = typespec_ctypes.c_double()
        c_wait_duration_max = typespec_ctypes.c_double()
        result = self.lib.FDwfDigitalOutWaitInfo(self.hdwf, c_wait_duration_min, c_wait_duration_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        wait_duration_min = c_wait_duration_min.value
        wait_duration_max = c_wait_duration_max.value
        return (wait_duration_min, wait_duration_max)

    def waitSet(self, wait_duration: float) -> None:
        """Set wait duration before digital-out pulse-sequence runs, in seconds.

        Parameters:
            wait_duration (float): Digital-out wait duration, in seconds.
        """
        result = self.lib.FDwfDigitalOutWaitSet(self.hdwf, wait_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def waitGet(self) -> float:
        """Get wait duration before digital-out pulse-sequence runs, in seconds.

        Returns:
            float: Digital-out wait duration, in seconds.
        """
        c_wait_duration = typespec_ctypes.c_double()
        result = self.lib.FDwfDigitalOutWaitGet(self.hdwf, c_wait_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        wait_duration = c_wait_duration.value
        return wait_duration

    def repeatInfo(self) -> Tuple[int, int]:
        """Get minimal and maximal repeat count for digital-out pulse-sequence runs.

        Returns:
            Tuple[int, int]: A tuple containing the minimal and maximal repeat count for
                digital-out pulse-sequence runs.
        """
        c_repeat_min = typespec_ctypes.c_unsigned_int()
        c_repeat_max = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalOutRepeatInfo(self.hdwf, c_repeat_min, c_repeat_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        repeat_min = c_repeat_min.value
        repeat_max = c_repeat_max.value
        return (repeat_min, repeat_max)

    def repeatSet(self, repeat: int) -> None:
        """Set repeat count for digital-out pulse-sequence runs.

        Parameters:
            repeat: Repeat count.
                The value 0 is special; it means *forever*.
        """
        result = self.lib.FDwfDigitalOutRepeatSet(self.hdwf, repeat)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def repeatGet(self) -> int:
        """Set repeat count for digital-out pulse-sequence runs.

        Returns:
            int: Repeat count.
                The value 0 is special; it means *forever*.
        """
        c_repeat = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalOutRepeatGet(self.hdwf, c_repeat)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        repeat = c_repeat.value
        return repeat

    def repeatStatus(self) -> int:
        """Get repeat status for the currently active digital-out train of pulse-sequence runs.

        This number counts down as a digital output sequence is active.

        Returns:
            int: Repeat count status.
        """
        c_repeat_status = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalOutRepeatStatus(self.hdwf, c_repeat_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        repeat_status = c_repeat_status.value
        return repeat_status

    def triggerSlopeSet(self, trigger_slope: DwfTriggerSlope) -> None:
        """Set the slope for the digital-out trigger.

        Parameters:
            trigger_slope (DwfTriggerSlope): The trigger slope to be configured.
        """
        result = self.lib.FDwfDigitalOutTriggerSlopeSet(self.hdwf, trigger_slope.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSlopeGet(self) -> DwfTriggerSlope:
        """Get the slope for the digital-out trigger.

        Returns:
            DwfTriggerSlope: The currently configured trigger slope.
        """
        c_trigger_slope = typespec_ctypes.DwfTriggerSlope()
        result = self.lib.FDwfDigitalOutTriggerSlopeGet(self.hdwf, c_trigger_slope)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_slope = DwfTriggerSlope(c_trigger_slope.value)
        return trigger_slope

    def repeatTriggerSet(self, repeat_trigger_flag: bool) -> None:
        """Specify if each pulse sequence run should wait for its own trigger.

        Parameters:
            repeat_trigger_flag (bool): If True, not only the first, both also every successive run of the
                pulse output sequence will wait until it receives a trigger.
        """
        result = self.lib.FDwfDigitalOutRepeatTriggerSet(self.hdwf, repeat_trigger_flag)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def repeatTriggerGet(self) -> bool:
        """Get if each pulse sequence run should wait for its own trigger.

        Returns:
            bool: If True, not only the first, both also every successive run of the pulse output sequence
                will wait until it receives a trigger.
        """
        c_repeat_trigger = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalOutRepeatTriggerGet(self.hdwf, c_repeat_trigger)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        repeat_trigger_flag = bool(c_repeat_trigger.value)
        return repeat_trigger_flag

    def count(self) -> int:
        """Get digital-out channel count.

        Returns:
            int: The number of digital output channels.
        """
        c_channel_count = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalOutCount(self.hdwf, c_channel_count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        channel_count = c_channel_count.value
        return channel_count

    def enableSet(self, channel_index: int, enable_flag: bool) -> None:
        """Enable or disable a digital-out channel."""
        result = self.lib.FDwfDigitalOutEnableSet(self.hdwf, channel_index, enable_flag)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def enableGet(self, channel_index: int) -> bool:
        """Check if a specific digital-out channel is enabled."""
        c_enable_flag = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalOutEnableGet(self.hdwf, channel_index, c_enable_flag)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        enable_flag = bool(c_enable_flag.value)
        return enable_flag

    def outputInfo(self, channel_index: int) -> List[DwfDigitalOutOutput]:
        """Get output info."""
        c_output_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalOutOutputInfo(self.hdwf, channel_index, c_output_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_bitset = c_output_bitset.value
        output_list = [output for output in DwfDigitalOutOutput if output_bitset & (1 << output.value)]
        return output_list

    def outputSet(self, channel_index: int, output_value: DwfDigitalOutOutput) -> None:
        """Set output."""
        result = self.lib.FDwfDigitalOutOutputSet(self.hdwf, channel_index, output_value.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputGet(self, channel_index: int) -> DwfDigitalOutOutput:
        """Get output."""
        c_output_value = typespec_ctypes.DwfDigitalOutOutput()
        result = self.lib.FDwfDigitalOutOutputGet(self.hdwf, channel_index, c_output_value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_value = DwfDigitalOutOutput(c_output_value.value)
        return output_value

    def typeInfo(self, channel_index: int) -> List[DwfDigitalOutType]:
        """Get a list of possible output signal type values."""
        c_type_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalOutTypeInfo(self.hdwf, channel_index, c_type_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        type_bitset = c_type_bitset.value
        type_list = [type_ for type_ in DwfDigitalOutType if type_bitset & (1 << type_.value)]
        return type_list

    def typeSet(self, channel_index: int, output_type: DwfDigitalOutType) -> None:
        """Set output signal type."""
        result = self.lib.FDwfDigitalOutTypeSet(self.hdwf, channel_index, output_type.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def typeGet(self, channel_index: int) -> DwfDigitalOutType:
        """Get currently configured output signal type."""
        c_output_type = typespec_ctypes.DwfDigitalOutType()
        result = self.lib.FDwfDigitalOutTypeGet(self.hdwf, channel_index, c_output_type)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_type = DwfDigitalOutType(c_output_type.value)
        return output_type

    def idleInfo(self, channel_index: int) -> List[DwfDigitalOutIdle]:
        """Get a list of possible idle behavior setting values."""
        c_idle_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalOutIdleInfo(self.hdwf, channel_index, c_idle_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        idle_bitset = c_idle_bitset.value
        idle_list = [idle for idle in DwfDigitalOutIdle if idle_bitset & (1 << idle.value)]
        return idle_list

    def idleSet(self, channel_index: int, idle_mode: DwfDigitalOutIdle) -> None:
        """Set idle behavior setting."""
        result = self.lib.FDwfDigitalOutIdleSet(self.hdwf, channel_index, idle_mode.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def idleGet(self, channel_index: int) -> DwfDigitalOutIdle:
        """Get currently active idle behavior setting."""
        c_idle_mode = typespec_ctypes.DwfDigitalOutIdle()
        result = self.lib.FDwfDigitalOutIdleGet(self.hdwf, channel_index, c_idle_mode)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        idle_mode = DwfDigitalOutIdle(c_idle_mode.value)
        return idle_mode

    def dividerInfo(self, channel_index: int) -> Tuple[int, int]:
        """Get divider value range."""
        c_divider_init_min = typespec_ctypes.c_unsigned_int()
        c_divider_init_max = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalOutDividerInfo(
            self.hdwf,
            channel_index,
            c_divider_init_min,
            c_divider_init_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        divider_init_min = c_divider_init_min.value
        divider_init_max = c_divider_init_max.value
        return (divider_init_min, divider_init_max)

    def dividerInitSet(self, channel_index: int, divider_init: int) -> None:
        """Set initial divider value."""
        result = self.lib.FDwfDigitalOutDividerInitSet(self.hdwf, channel_index, divider_init)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def dividerInitGet(self, channel_index: int) -> int:
        """Get currently configured initial divider value."""
        c_divider_init = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalOutDividerInitGet(self.hdwf, channel_index, c_divider_init)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        divider_init = c_divider_init.value
        return divider_init

    def dividerSet(self, channel_index: int, divider: int) -> None:
        """Set divider value."""
        result = self.lib.FDwfDigitalOutDividerSet(self.hdwf, channel_index, divider)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def dividerGet(self, channel_index: int) -> int:
        """Get currently configured divider value."""
        c_divider = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalOutDividerGet(self.hdwf, channel_index, c_divider)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        divider = c_divider.value
        return divider

    def counterInfo(self, channel_index: int) -> Tuple[int, int]:
        """Get counter value range."""
        c_counter_min = typespec_ctypes.c_unsigned_int()
        c_counter_max = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalOutCounterInfo(
            self.hdwf,
            channel_index,
            c_counter_min,
            c_counter_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        counter_min = c_counter_min.value
        counter_max = c_counter_max.value
        return (counter_min, counter_max)

    def counterInitSet(self, channel_index: int, high: bool, counter_init: int) -> None:
        """Set initial signal value and initial counter value."""
        result = self.lib.FDwfDigitalOutCounterInitSet(
            self.hdwf,
            channel_index,
            high, counter_init)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def counterInitGet(self, channel_index: int) -> Tuple[bool, int]:
        """Get initial signal value and initial counter value."""
        c_high = typespec_ctypes.c_int()
        c_counter_init = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalOutCounterInitGet(
            self.hdwf,
            channel_index, c_high,
            c_counter_init)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        high = bool(c_high.value)
        counter_init = c_counter_init.value
        return (high, counter_init)

    def counterSet(self, channel_index: int, low_count: int, high_count: int) -> None:
        """Set counter durations for both the low and high signal output levels."""
        result = self.lib.FDwfDigitalOutCounterSet(self.hdwf, channel_index, low_count, high_count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def counterGet(self, channel_index: int) -> Tuple[int, int]:
        """Get counter durations for both the low and high signal output levels."""
        c_low_count = typespec_ctypes.c_unsigned_int()
        c_high_count = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalOutCounterGet(self.hdwf, channel_index, c_low_count, c_high_count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        low_count = c_low_count.value
        high_count = c_high_count.value
        return (low_count, high_count)

    def dataInfo(self, channel_index: int) -> int:
        """Return the maximum buffer size for the specified DigitalOut channel,
        i.e., the number of custom data bits.

        Parameters:
            channel_index (int): the channel for which to obtain the data bits count.
        Returns:
            int: The number of custom data bits that can be specified for the channel.
        """
        c_max_data_bits = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalOutDataInfo(self.hdwf, channel_index, c_max_data_bits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        max_data_bits = c_max_data_bits.value
        return max_data_bits

    def dataSet(self, channel_index: int, bits: str, tristate: bool = False) -> None:
        """Set digital-out arbitrary channel data."""

        if tristate:
            bits = bits.replace('1', '11').replace('0', '01').replace('Z', '00')

        countOfBits = len(bits)

        octets = []
        while len(bits) > 0:
            octet_str = bits[:8]
            octet = int(octet_str[::-1], 2)
            octets.append(octet)
            bits = bits[8:]

        octets_as_bytes = bytes(octets)

        result = self.lib.FDwfDigitalOutDataSet(self.hdwf, channel_index, octets_as_bytes, countOfBits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def playDataSet(self, rg_bits: int, bits_per_sample: int, count_of_samples: int) -> None:
        """Set playback data."""
        result = self.lib.FDwfDigitalOutPlayDataSet(
            self.hdwf,
            rg_bits,
            bits_per_sample,
            count_of_samples)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def playRateSet(self, rate_hz: float) -> None:
        """Set playback rate."""
        result = self.lib.FDwfDigitalOutPlayRateSet(self.hdwf, rate_hz)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
