"""The |pydwf.core.api.digital_in| module implements a single class: |DigitalIn|."""

from typing import List, Tuple

import numpy as np

from pydwf.core.auxiliary.enum_types import (DwfDigitalInSampleMode, DwfDigitalInClockSource,
                                             DwfAcquisitionMode, DwfTriggerSlope, DwfState, DwfTriggerSource)
from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class DigitalIn(DwfDevice_SubAPI):
    """The |DigitalIn| class provides access to the DigitalIn (logic analyzer) instrument of a |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its public
        |digitalIn:link| attribute for access by the user.
    """

    # pylint: disable=too-many-public-methods

    def reset(self) -> None:
        """Reset the DigitalIn instrument parameters to default values.

        If auto-configure is enabled, the reset values will be used immediately.
        """
        result = self.lib.FDwfDigitalInReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def configure(self, reconfigure: bool, start: bool) -> None:
        """Configure the DigitalIn instrument."""
        result = self.lib.FDwfDigitalInConfigure(self.hdwf, reconfigure, start)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def status(self, read_data_flag: bool) -> DwfState:
        """Get instrument status."""
        c_status = typespec_ctypes.DwfState()
        result = self.lib.FDwfDigitalInStatus(self.hdwf, read_data_flag, c_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        status = DwfState(c_status.value)
        return status

    def statusSamplesLeft(self) -> int:
        """Retrieve the number of samples left in the acquisition."""
        c_samplesLeft = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInStatusSamplesLeft(self.hdwf, c_samplesLeft)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        samplesLeft = c_samplesLeft.value
        return samplesLeft

    def statusSamplesValid(self) -> int:
        """Retrieve the number of valid/acquired data samples."""
        c_samplesValid = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInStatusSamplesValid(self.hdwf, c_samplesValid)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        samplesValid = c_samplesValid.value
        return samplesValid

    def statusIndexWrite(self) -> int:
        """Retrieve the buffer write pointer.

        This is needed in ScanScreen acquisition mode to display the scan bar.
        """
        c_idxWrite = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInStatusIndexWrite(self.hdwf, c_idxWrite)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        idxWrite = c_idxWrite.value
        return idxWrite

    def statusAutoTriggered(self) -> bool:
        """Verify if the acquisition is auto triggered."""
        c_auto = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInStatusAutoTriggered(self.hdwf, c_auto)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        auto = bool(c_auto.value)
        return auto

    def statusData(self, count_bytes: int) -> np.ndarray:
        """Retrieve the acquired data samples from the DigitalIn instrument.
        It copies the data samples to the provided buffer.
        """
        samples = np.empty(count_bytes, dtype='B')
        result = self.lib.FDwfDigitalInStatusData(
            self.hdwf,
            samples.ctypes.data_as(typespec_ctypes.c_unsigned_char_ptr),
            count_bytes)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        return samples

    def statusData2(self, first_sample: int, count_bytes: int) -> np.ndarray:
        """Retrieve the acquired data samples from the DigitalIn instrument.
        """

        samples = np.empty(count_bytes, dtype='B')
        result = self.lib.FDwfDigitalInStatusData2(
            self.hdwf,
            samples.ctypes.data_as(typespec_ctypes.c_unsigned_char_ptr),
            first_sample,
            count_bytes)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        return samples

    def statusNoise2(self, first_sample: int, count_bytes: int) -> np.ndarray:
        """Get noise."""
        noise = np.empty(count_bytes, dtype='B')
        result = self.lib.FDwfDigitalInStatusNoise2(
            self.hdwf,
            noise.ctypes.data_as(typespec_ctypes.c_unsigned_char_ptr),
            first_sample,
            count_bytes)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        return noise

    def statusRecord(self) -> Tuple[int, int, int]:
        """Get recording status."""
        c_data_available = typespec_ctypes.c_int()
        c_data_lost = typespec_ctypes.c_int()
        c_data_corrupt = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInStatusRecord(
            self.hdwf,
            c_data_available,
            c_data_lost,
            c_data_corrupt)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        data_free = c_data_available.value
        data_lost = c_data_lost.value
        data_corrupt = c_data_corrupt.value
        return (data_free, data_lost, data_corrupt)

    def statusTime(self) -> Tuple[int, int, int]:
        """Get status timestamp."""
        c_sec_utc = typespec_ctypes.c_unsigned_int()
        c_tick = typespec_ctypes.c_unsigned_int()
        c_ticks_per_second = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalInStatusTime(
            self.hdwf,
            c_sec_utc,
            c_tick,
            c_ticks_per_second)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        sec_utc = c_sec_utc.value
        tick = c_tick.value
        ticks_per_second = c_ticks_per_second.value
        return (sec_utc, tick, ticks_per_second)

    def internalClockInfo(self) -> float:
        """Get internal clock info."""
        c_hzFreq = typespec_ctypes.c_double()
        result = self.lib.FDwfDigitalInInternalClockInfo(self.hdwf, c_hzFreq)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        hzFreq = c_hzFreq.value
        return hzFreq

    def clockSourceInfo(self) -> List[DwfDigitalInClockSource]:
        """Get digital-in clock source info."""
        c_clock_source_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInClockSourceInfo(self.hdwf, c_clock_source_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        clock_source_bitset = c_clock_source_bitset.value
        clock_source_list = [clock_source for clock_source in DwfDigitalInClockSource
                             if clock_source_bitset & (1 << clock_source.value)]
        return clock_source_list

    def clockSourceSet(self, clock_source: DwfDigitalInClockSource) -> None:
        """Set clock source."""
        result = self.lib.FDwfDigitalInClockSourceSet(self.hdwf, clock_source.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def clockSourceGet(self) -> DwfDigitalInClockSource:
        """Get clock source."""
        c_clock_source = typespec_ctypes.DwfDigitalInClockSource()
        result = self.lib.FDwfDigitalInClockSourceGet(self.hdwf, c_clock_source)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        clock_source = DwfDigitalInClockSource(c_clock_source.value)
        return clock_source

    def dividerInfo(self) -> int:
        """Get divider info."""
        c_divMax = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalInDividerInfo(self.hdwf, c_divMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        divMax = c_divMax.value
        return divMax

    def dividerSet(self, div: int) -> None:
        """Set divider value."""
        result = self.lib.FDwfDigitalInDividerSet(self.hdwf, div)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def dividerGet(self) -> int:
        """Get divider value."""
        c_div = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalInDividerGet(self.hdwf, c_div)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        div = c_div.value
        return div

    def bitsInfo(self) -> int:
        """Get bits info."""
        c_nBits = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInBitsInfo(self.hdwf, c_nBits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        nBits = c_nBits.value
        return nBits

    def sampleFormatSet(self, num_bits: int) -> None:
        """Set sample format."""
        result = self.lib.FDwfDigitalInSampleFormatSet(self.hdwf, num_bits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def sampleFormatGet(self) -> int:
        """Set sample format."""
        c_num_bits = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInSampleFormatGet(self.hdwf, c_num_bits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        num_bits = c_num_bits.value
        return num_bits

    def inputOrderSet(self, dio_first: bool) -> None:
        """Configure the order of values stored in the sampling array.

        If dio_first is True, DIO 24..39 are placed at the beginning of the array followed by DIN 0..23.
        If dio_first is False, DIN 0..23 are placed at the beginning followed by DIO 24..31.
        Valid only for Digital Discovery device.
        """
        result = self.lib.FDwfDigitalInInputOrderSet(self.hdwf, dio_first)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def bufferSizeInfo(self) -> int:
        """Get buffer size info."""
        c_nSizeMax = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInBufferSizeInfo(self.hdwf, c_nSizeMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        nSizeMax = c_nSizeMax.value
        return nSizeMax

    def bufferSizeSet(self, buffer_size: int) -> None:
        """Set buffer size."""
        result = self.lib.FDwfDigitalInBufferSizeSet(self.hdwf, buffer_size)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def bufferSizeGet(self) -> int:
        """Get buffer size."""
        c_buffer_size = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInBufferSizeGet(self.hdwf, c_buffer_size)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        buffer_size = c_buffer_size.value
        return buffer_size

    def sampleModeInfo(self) -> List[DwfDigitalInSampleMode]:
        """Get digital-in sample mode info."""
        c_sample_mode_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInSampleModeInfo(self.hdwf, c_sample_mode_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        sample_mode_bitset = c_sample_mode_bitset.value
        sample_mode_list = [sample_mode for sample_mode in DwfDigitalInSampleMode
                            if sample_mode_bitset & (1 << sample_mode.value)]
        return sample_mode_list

    def sampleModeSet(self, sample_mode: DwfDigitalInSampleMode) -> None:
        """Set sample mode."""
        result = self.lib.FDwfDigitalInSampleModeSet(self.hdwf, sample_mode.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def sampleModeGet(self) -> DwfDigitalInSampleMode:
        """Get sample mode."""
        c_sample_mode = typespec_ctypes.DwfDigitalInSampleMode()
        result = self.lib.FDwfDigitalInSampleModeGet(self.hdwf, c_sample_mode)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        sample_mode = DwfDigitalInSampleMode(c_sample_mode.value)
        return sample_mode

    def sampleSensibleSet(self, compression_bits: int) -> None:
        """Set sample sensible (?)."""
        result = self.lib.FDwfDigitalInSampleSensibleSet(self.hdwf, compression_bits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def sampleSensibleGet(self) -> int:
        """Get sample sensible (?)."""
        c_compression_bits = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalInSampleSensibleGet(self.hdwf, c_compression_bits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        compression_bits = c_compression_bits.value
        return compression_bits

    def acquisitionModeInfo(self) -> List[DwfAcquisitionMode]:
        """Get digital-in acquisition mode info."""
        c_acquisition_mode_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInAcquisitionModeInfo(self.hdwf, c_acquisition_mode_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        acquisition_mode_bitset = c_acquisition_mode_bitset.value
        acquisition_mode_list = [acquisition_mode for acquisition_mode in DwfAcquisitionMode
                                 if acquisition_mode_bitset & (1 << acquisition_mode.value)]
        return acquisition_mode_list

    def acquisitionModeSet(self, acquisition_mode: DwfAcquisitionMode) -> None:
        """Set acquisition mode."""
        result = self.lib.FDwfDigitalInAcquisitionModeSet(self.hdwf, acquisition_mode.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def acquisitionModeGet(self) -> DwfAcquisitionMode:
        """Get acquisition mode."""
        c_acquisition_mode = typespec_ctypes.ACQMODE()
        result = self.lib.FDwfDigitalInAcquisitionModeGet(self.hdwf, c_acquisition_mode)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        acquisition_mode = DwfAcquisitionMode(c_acquisition_mode.value)
        return acquisition_mode

    # Trigger functions:

    def triggerSourceSet(self, trigger_source: DwfTriggerSource) -> None:
        """Set trigger source."""
        result = self.lib.FDwfDigitalInTriggerSourceSet(self.hdwf, trigger_source.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSourceGet(self) -> DwfTriggerSource:
        """Get trigger source."""
        c_trigger_source = typespec_ctypes.TRIGSRC()
        result = self.lib.FDwfDigitalInTriggerSourceGet(self.hdwf, c_trigger_source)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source = DwfTriggerSource(c_trigger_source.value)
        return trigger_source

    def triggerSlopeSet(self, trigger_slope: DwfTriggerSlope) -> None:
        """Set trigger slope."""
        result = self.lib.FDwfDigitalInTriggerSlopeSet(self.hdwf, trigger_slope.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSlopeGet(self) -> DwfTriggerSlope:
        """Get trigger slope."""
        c_trigger_slope = typespec_ctypes.DwfTriggerSlope()
        result = self.lib.FDwfDigitalInTriggerSlopeGet(self.hdwf, c_trigger_slope)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_slope = DwfTriggerSlope(c_trigger_slope.value)
        return trigger_slope

    def triggerPositionInfo(self) -> int:
        """Get trigger position info."""
        c_max_samples_after_trigger = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalInTriggerPositionInfo(
            self.hdwf,
            c_max_samples_after_trigger)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        max_samples_after_trigger = c_max_samples_after_trigger.value
        return max_samples_after_trigger

    def triggerPositionSet(self, samples_after_trigger: int) -> None:
        """Set trigger desired position."""
        result = self.lib.FDwfDigitalInTriggerPositionSet(self.hdwf, samples_after_trigger)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerPositionGet(self) -> int:
        """Get trigger desired position."""
        c_samples_after_trigger = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalInTriggerPositionGet(self.hdwf, c_samples_after_trigger)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        samples_after_trigger = c_samples_after_trigger.value
        return samples_after_trigger

    def triggerPrefillSet(self, samples_before_trigger: int) -> None:
        """Set trigger prefill."""
        result = self.lib.FDwfDigitalInTriggerPrefillSet(self.hdwf, samples_before_trigger)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerPrefillGet(self) -> int:
        """Get trigger prefill."""
        c_samples_before_trigger = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalInTriggerPrefillGet(self.hdwf, c_samples_before_trigger)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        samples_before_trigger = c_samples_before_trigger.value
        return samples_before_trigger

    def triggerAutoTimeoutInfo(self) -> Tuple[float, float, float]:
        """Get trigger auto-timeout info."""
        c_secMin = typespec_ctypes.c_double()
        c_secMax = typespec_ctypes.c_double()
        c_nSteps = typespec_ctypes.c_double()
        result = self.lib.FDwfDigitalInTriggerAutoTimeoutInfo(self.hdwf, c_secMin, c_secMax, c_nSteps)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        secMin = c_secMin.value
        secMax = c_secMax.value
        nSteps = c_nSteps.value
        return (secMin, secMax, nSteps)

    def triggerAutoTimeoutSet(self, auto_timeout: float) -> None:
        """Set trigger auto-timeout value."""
        result = self.lib.FDwfDigitalInTriggerAutoTimeoutSet(self.hdwf, auto_timeout)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerAutoTimeoutGet(self) -> float:
        """Get trigger auto-timeout value."""
        c_auto_timeout = typespec_ctypes.c_double()
        result = self.lib.FDwfDigitalInTriggerAutoTimeoutGet(self.hdwf, c_auto_timeout)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        auto_timeout = c_auto_timeout.value
        return auto_timeout

    def triggerInfo(self) -> Tuple[int, int, int, int]:
        """Get trigger info."""
        c_fsLevelLow  = typespec_ctypes.c_unsigned_int()
        c_fsLevelHigh = typespec_ctypes.c_unsigned_int()
        c_fsEdgeRise  = typespec_ctypes.c_unsigned_int()
        c_fsEdgeFall  = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalInTriggerInfo(
            self.hdwf,
            c_fsLevelLow,
            c_fsLevelHigh,
            c_fsEdgeRise,
            c_fsEdgeFall)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        fsLevelLow  = c_fsLevelLow.value
        fsLevelHigh = c_fsLevelHigh.value
        fsEdgeRise  = c_fsEdgeRise.value
        fsEdgeFall  = c_fsEdgeFall.value
        return (fsLevelLow, fsLevelHigh, fsEdgeRise, fsEdgeFall)

    def triggerSet(self, fsLevelLow: int, fsLevelHigh: int, fsEdgeRise: int, fsEdgeFall: int) -> None:
        """Set trigger."""
        result = self.lib.FDwfDigitalInTriggerSet(
            self.hdwf,
            fsLevelLow,
            fsLevelHigh,
            fsEdgeRise,
            fsEdgeFall)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerGet(self) -> Tuple[int, int, int, int]:
        """Get trigger."""
        c_fsLevelLow  = typespec_ctypes.c_unsigned_int()
        c_fsLevelHigh = typespec_ctypes.c_unsigned_int()
        c_fsEdgeRise  = typespec_ctypes.c_unsigned_int()
        c_fsEdgeFall  = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalInTriggerGet(
            self.hdwf,
            c_fsLevelLow,
            c_fsLevelHigh,
            c_fsEdgeRise,
            c_fsEdgeFall)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        fsLevelLow  = c_fsLevelLow.value
        fsLevelHigh = c_fsLevelHigh.value
        fsEdgeRise  = c_fsEdgeRise.value
        fsEdgeFall  = c_fsEdgeFall.value
        return (fsLevelLow, fsLevelHigh, fsEdgeRise, fsEdgeFall)

    def triggerResetSet(self, fsLevelLow: int, fsLevelHigh: int, fsEdgeRise: int, fsEdgeFall: int) -> None:
        """Configure trigger reset settings."""
        result = self.lib.FDwfDigitalInTriggerResetSet(
            self.hdwf,
            fsLevelLow,
            fsLevelHigh,
            fsEdgeRise,
            fsEdgeFall)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerCountSet(self, count: int, restart: int) -> None:
        """Set trigger count."""
        result = self.lib.FDwfDigitalInTriggerCountSet(self.hdwf, count, restart)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerLengthSet(self, trigger_length_min: float, trigger_length_max: float, idxSync: int) -> None:
        """Set trigger length."""
        result = self.lib.FDwfDigitalInTriggerLengthSet(self.hdwf, trigger_length_min, trigger_length_max, idxSync)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerMatchSet(self, pin: int, mask: int, value: int, bit_stuffing: int) -> None:
        """Set trigger match."""
        result = self.lib.FDwfDigitalInTriggerMatchSet(self.hdwf, pin, mask, value, bit_stuffing)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    # Obsolete functions:

    def mixedSet(self, enable: bool) -> None:
        """Set mixed state.

        Note:
            This function is OBSOLETE.
        """
        result = self.lib.FDwfDigitalInMixedSet(self.hdwf, enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSourceInfo(self) -> List[DwfTriggerSource]:
        """Get trigger source info.

        Note:
            This function is OBSOLETE. Use the generic :py:meth:`DeviceControl.triggerInfo()` method instead.
        """
        c_trigger_source_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalInTriggerSourceInfo(self.hdwf, c_trigger_source_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source_bitset = c_trigger_source_bitset.value
        trigger_source_list = [trigger_source for trigger_source in DwfTriggerSource
                               if trigger_source_bitset & (1 << trigger_source.value)]
        return trigger_source_list
