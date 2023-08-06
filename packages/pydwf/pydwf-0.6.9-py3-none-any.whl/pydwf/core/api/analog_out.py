"""The |pydwf.core.api.analog_out| module implements a single class: |AnalogOut|."""

from typing import Tuple, List

import numpy as np

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.enum_types import (DwfTriggerSource, DwfAnalogOutFunction, DwfState,
                                             DwfAnalogOutNode, DwfTriggerSlope, DwfAnalogOutMode, DwfAnalogOutIdle)
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class AnalogOut(DwfDevice_SubAPI):
    """The |AnalogOut| class provides access to the AnalogOut (signal generator) instrument of a |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its
        public |analogOut:link| attribute for access by the user.
    """

    # pylint: disable=too-many-public-methods

    def count(self) -> int:
        """Count number of analog output channels."""
        c_cChannel = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutCount(self.hdwf, c_cChannel)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        cChannel = c_cChannel.value
        return cChannel

    def masterSet(self, channel_index: int, master_index: int) -> None:
        """Set master status."""
        result = self.lib.FDwfAnalogOutMasterSet(self.hdwf, channel_index, master_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def masterGet(self, channel_index: int) -> int:
        """Get master status."""
        c_master_index = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutMasterGet(self.hdwf, channel_index, c_master_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        master_index = c_master_index.value
        return master_index

    def triggerSourceSet(self, channel_index: int, trigger_source: DwfTriggerSource) -> None:
        """Set trigger source."""
        result = self.lib.FDwfAnalogOutTriggerSourceSet(
            self.hdwf,
            channel_index,
            trigger_source.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSourceGet(self, channel_index: int) -> DwfTriggerSource:
        """Get trigger source."""
        c_trigger_source = typespec_ctypes.TRIGSRC()
        result = self.lib.FDwfAnalogOutTriggerSourceGet(self.hdwf, channel_index, c_trigger_source)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source = DwfTriggerSource(c_trigger_source.value)
        return trigger_source

    def triggerSlopeSet(self, channel_index: int, trigger_slope: DwfTriggerSlope) -> None:
        """Set trigger slope."""
        result = self.lib.FDwfAnalogOutTriggerSlopeSet(
            self.hdwf,
            channel_index,
            trigger_slope.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def triggerSlopeGet(self, channel_index: int) -> DwfTriggerSlope:
        """Get trigger slope."""
        c_trigger_slope = typespec_ctypes.DwfTriggerSlope()
        result = self.lib.FDwfAnalogOutTriggerSlopeGet(self.hdwf, channel_index, c_trigger_slope)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_slope = DwfTriggerSlope(c_trigger_slope.value)
        return trigger_slope

    def runInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get run info."""
        c_secMin = typespec_ctypes.c_double()
        c_secMax = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutRunInfo(self.hdwf, channel_index, c_secMin, c_secMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        secMin = c_secMin.value
        secMax = c_secMax.value
        return (secMin, secMax)

    def runSet(self, channel_index: int, run_duration: float) -> None:
        """Set run duration, in seconds."""
        result = self.lib.FDwfAnalogOutRunSet(self.hdwf, channel_index, run_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def runGet(self, channel_index: int) -> float:
        """Get run-time."""
        c_run_duration = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutRunGet(self.hdwf, channel_index, c_run_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        run_duration = c_run_duration.value
        return run_duration

    def runStatus(self, channel_index: int) -> float:
        """Get run status."""
        c_secRun = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutRunStatus(self.hdwf, channel_index, c_secRun)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        secRun = c_secRun.value
        return secRun

    def waitInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get wait info."""
        c_secMin = typespec_ctypes.c_double()
        c_secMax = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutWaitInfo(self.hdwf, channel_index, c_secMin, c_secMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        secMin = c_secMin.value
        secMax = c_secMax.value
        return (secMin, secMax)

    def waitSet(self, channel_index: int, wait_duration: float) -> None:
        """Set wait state duration, in seconds."""
        result = self.lib.FDwfAnalogOutWaitSet(self.hdwf, channel_index, wait_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def waitGet(self, channel_index: int) -> float:
        """Get wait state duration in seconds."""
        c_wait_duration = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutWaitGet(self.hdwf, channel_index, c_wait_duration)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        wait_duration = c_wait_duration.value
        return wait_duration

    def repeatInfo(self, channel_index: int) -> Tuple[int, int]:
        """Get repeat info."""
        c_nMin = typespec_ctypes.c_int()
        c_nMax = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutRepeatInfo(self.hdwf, channel_index, c_nMin, c_nMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        nMin = c_nMin.value
        nMax = c_nMax.value
        return (nMin, nMax)

    def repeatSet(self, channel_index: int, repeat: int) -> None:
        """Set repeat setting."""
        result = self.lib.FDwfAnalogOutRepeatSet(self.hdwf, channel_index, repeat)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def repeatGet(self, channel_index: int) -> int:
        """Get repeat setting."""
        c_repeat = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutRepeatGet(self.hdwf, channel_index, c_repeat)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        repeat = c_repeat.value
        return repeat

    def repeatStatus(self, channel_index: int) -> int:
        """Get repeat status."""
        c_repeat_status = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutRepeatStatus(self.hdwf, channel_index, c_repeat_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        repeat_status = c_repeat_status.value
        return repeat_status

    def repeatTriggerSet(self, channel_index: int, repeat_trigger_flag: bool) -> None:
        """Set repeat trigger setting."""
        result = self.lib.FDwfAnalogOutRepeatTriggerSet(self.hdwf, channel_index, repeat_trigger_flag)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def repeatTriggerGet(self, channel_index: int) -> bool:
        """Get repeat trigger setting."""
        c_repeat_trigger_flag = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutRepeatTriggerGet(
            self.hdwf,
            channel_index,
            c_repeat_trigger_flag)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        repeat_trigger_flag = bool(c_repeat_trigger_flag.value)
        return repeat_trigger_flag

    def limitationInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get limitation info."""
        c_min = typespec_ctypes.c_double()
        c_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutLimitationInfo(self.hdwf, channel_index, c_min, c_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        min_ = c_min.value
        max_ = c_max.value
        return (min_, max_)

    def limitationSet(self, channel_index: int, limit: float) -> None:
        """Set limitation value."""
        result = self.lib.FDwfAnalogOutLimitationSet(self.hdwf, channel_index, limit)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def limitationGet(self, channel_index: int) -> float:
        """Get limitation value."""
        c_limit = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutLimitationGet(self.hdwf, channel_index, c_limit)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        limit = c_limit.value
        return limit

    def modeSet(self, channel_index: int, mode: DwfAnalogOutMode) -> None:
        """Set analog output mode."""
        result = self.lib.FDwfAnalogOutModeSet(self.hdwf, channel_index, mode.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def modeGet(self, channel_index: int) -> DwfAnalogOutMode:
        """Get analog output mode."""
        c_mode = typespec_ctypes.DwfAnalogOutMode()
        result = self.lib.FDwfAnalogOutModeGet(self.hdwf, channel_index, c_mode)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        mode = DwfAnalogOutMode(c_mode.value)
        return mode

    def idleInfo(self, channel_index: int) -> List[DwfAnalogOutIdle]:
        """Get idle info."""
        c_idle_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutIdleInfo(self.hdwf, channel_index, c_idle_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        idle_bitset = c_idle_bitset.value
        idle_list = [idle for idle in DwfAnalogOutIdle if idle_bitset & (1 << idle.value)]
        return idle_list

    def idleSet(self, channel_index: int, idle: DwfAnalogOutIdle) -> None:
        """Set idle behavior."""
        result = self.lib.FDwfAnalogOutIdleSet(self.hdwf, channel_index, idle.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def idleGet(self, channel_index: int) -> DwfAnalogOutIdle:
        """Get idle behavior."""
        c_idle = typespec_ctypes.DwfAnalogOutIdle()
        result = self.lib.FDwfAnalogOutIdleGet(self.hdwf, channel_index, c_idle)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        idle = DwfAnalogOutIdle(c_idle.value)
        return idle

    def nodeInfo(self, channel_index: int) -> List[DwfAnalogOutNode]:
        """Get node info."""
        c_node_info_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutNodeInfo(self.hdwf, channel_index, c_node_info_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        node_info_bitset = c_node_info_bitset.value
        node_info_list = [node for node in DwfAnalogOutNode if node_info_bitset & (1 << node.value)]
        return node_info_list

    def nodeEnableSet(self, channel_index: int, node: DwfAnalogOutNode, enable: bool) -> None:
        """Set node enabled state."""
        result = self.lib.FDwfAnalogOutNodeEnableSet(self.hdwf, channel_index, node.value, enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeEnableGet(self, channel_index: int, node: DwfAnalogOutNode) -> bool:
        """"Get node enabled state."""
        c_enable = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutNodeEnableGet(self.hdwf, channel_index, node.value, c_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        enable = bool(c_enable.value)
        return enable

    def nodeFunctionInfo(self, channel_index: int, node: DwfAnalogOutNode) -> List[DwfAnalogOutFunction]:
        """Get node function info."""
        c_func_bitset = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfAnalogOutNodeFunctionInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_func_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        func_bitset = c_func_bitset.value
        func_list = [func for func in DwfAnalogOutFunction if func_bitset & (1 << func.value)]
        return func_list

    def nodeFunctionSet(self, channel_index: int, node: DwfAnalogOutNode, func: DwfAnalogOutFunction) -> None:
        """Set node function."""
        result = self.lib.FDwfAnalogOutNodeFunctionSet(self.hdwf, channel_index, node.value, func.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeFunctionGet(self, channel_index: int, node: DwfAnalogOutNode) -> DwfAnalogOutFunction:
        """Get node function."""
        c_func = typespec_ctypes.FUNC()
        result = self.lib.FDwfAnalogOutNodeFunctionGet(self.hdwf, channel_index, node.value, c_func)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        func = DwfAnalogOutFunction(c_func.value)
        return func

    def nodeFrequencyInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get node frequency info, in Hz."""
        c_frequency_min = typespec_ctypes.c_double()
        c_frequency_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeFrequencyInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_frequency_min,
            c_frequency_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        frequency_min = c_frequency_min.value
        frequency_max = c_frequency_max.value
        return (frequency_min, frequency_max)

    def nodeFrequencySet(self, channel_index: int, node: DwfAnalogOutNode, frequency: float) -> None:
        """Set node frequency, in Hz."""
        result = self.lib.FDwfAnalogOutNodeFrequencySet(
            self.hdwf,
            channel_index,
            node.value,
            frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeFrequencyGet(self, channel_index: int, node: DwfAnalogOutNode) -> float:
        """Get node frequency, in Hz."""
        c_frequency = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeFrequencyGet(
            self.hdwf,
            channel_index,
            node.value,
            c_frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        frequency = c_frequency.value
        return frequency

    def nodeAmplitudeInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get node amplitude info, in Volts."""
        c_amplitude_min = typespec_ctypes.c_double()
        c_amplitude_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeAmplitudeInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_amplitude_min,
            c_amplitude_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        amplitude_min = c_amplitude_min.value
        amplitude_max = c_amplitude_max.value
        return (amplitude_min, amplitude_max)

    def nodeAmplitudeSet(self, channel_index: int, node: DwfAnalogOutNode, amplitude: float) -> None:
        """Set node amplitude, in Volts."""
        result = self.lib.FDwfAnalogOutNodeAmplitudeSet(
            self.hdwf,
            channel_index,
            node.value,
            amplitude)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeAmplitudeGet(self, channel_index: int, node: DwfAnalogOutNode) -> float:
        """Get node amplitude, in Volts."""
        c_amplitude = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeAmplitudeGet(
            self.hdwf,
            channel_index,
            node.value,
            c_amplitude)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        amplitude = c_amplitude.value
        return amplitude

    def nodeOffsetInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get node offset info, in Volts."""
        c_offset_min = typespec_ctypes.c_double()
        c_offset_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeOffsetInfo(self.hdwf, channel_index, node.value, c_offset_min, c_offset_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        offset_min = c_offset_min.value
        offset_max = c_offset_max.value
        return (offset_min, offset_max)

    def nodeOffsetSet(self, channel_index: int, node: DwfAnalogOutNode, offset: float) -> None:
        """Set node offset, in Volts."""
        result = self.lib.FDwfAnalogOutNodeOffsetSet(self.hdwf, channel_index, node.value, offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeOffsetGet(self, channel_index: int, node: DwfAnalogOutNode) -> float:
        """Get node offset, in Volts."""
        c_offset = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeOffsetGet(self.hdwf, channel_index, node.value, c_offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        offset = c_offset.value
        return offset

    def nodeSymmetryInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get node symmetry info."""
        c_symmetry_min = typespec_ctypes.c_double()
        c_symmetry_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeSymmetryInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_symmetry_min,
            c_symmetry_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        symmetry_min = c_symmetry_min.value
        symmetry_max = c_symmetry_max.value
        return (symmetry_min, symmetry_max)

    def nodeSymmetrySet(self, channel_index: int, node: DwfAnalogOutNode, symmetry: float) -> None:
        """Set node symmetry."""
        result = self.lib.FDwfAnalogOutNodeSymmetrySet(
            self.hdwf,
            channel_index,
            node.value,
            symmetry)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodeSymmetryGet(self, channel_index: int, node: DwfAnalogOutNode) -> float:
        """Get node symmetry."""
        c_symmetry = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodeSymmetryGet(
            self.hdwf,
            channel_index,
            node.value,
            c_symmetry)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        symmetry = c_symmetry.value
        return symmetry

    def nodePhaseInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get node phase info, in degrees."""
        c_phase_min = typespec_ctypes.c_double()
        c_phase_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodePhaseInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_phase_min,
            c_phase_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        phase_min = c_phase_min.value
        phase_max = c_phase_max.value
        return (phase_min, phase_max)

    def nodePhaseSet(self, channel_index: int, node: DwfAnalogOutNode, phase: float) -> None:
        """Set node phase, in degrees."""
        result = self.lib.FDwfAnalogOutNodePhaseSet(
            self.hdwf,
            channel_index,
            node.value,
            phase)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def nodePhaseGet(self, channel_index: int, node: DwfAnalogOutNode) -> float:
        """Get node phase, in degrees."""
        c_phase = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutNodePhaseGet(
            self.hdwf,
            channel_index,
            node.value,
            c_phase)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        phase = c_phase.value
        return phase

    def nodeDataInfo(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[float, float]:
        """Get node data info, in samples."""
        c_samples_min = typespec_ctypes.c_int()
        c_samples_max = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutNodeDataInfo(
            self.hdwf,
            channel_index,
            node.value,
            c_samples_min,
            c_samples_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        samples_min = c_samples_min.value
        samples_max = c_samples_max.value
        return (samples_min, samples_max)

    def nodeDataSet(self, channel_index: int, node: DwfAnalogOutNode, data: np.ndarray) -> None:
        """Set node data."""

        double_data = data.astype(np.float64)

        result = self.lib.FDwfAnalogOutNodeDataSet(
            self.hdwf,
            channel_index,
            node.value,
            double_data.ctypes.data_as(typespec_ctypes.c_double_ptr),
            len(double_data))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def customAMFMEnableSet(self, channel_index: int, enable: bool) -> None:
        """Set custom AM/FM enable status."""
        result = self.lib.FDwfAnalogOutCustomAMFMEnableSet(self.hdwf, channel_index, int(enable))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def customAMFMEnableGet(self, channel_index: int) -> bool:
        """Get custom AM/FM enable status."""
        c_enable = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutCustomAMFMEnableGet(self.hdwf, channel_index, c_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        enable = bool(c_enable.value)
        return enable

    def reset(self, channel_index: int) -> None:
        """Reset the AnalogOut instrument."""
        result = self.lib.FDwfAnalogOutReset(self.hdwf, channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def configure(self, channel_index: int, start: bool) -> None:
        """Configure the AnalogOut instrument."""
        result = self.lib.FDwfAnalogOutConfigure(self.hdwf, channel_index, start)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def status(self, channel_index: int) -> DwfState:
        """Get AnalogOut instrument state."""
        c_status = typespec_ctypes.DwfState()
        result = self.lib.FDwfAnalogOutStatus(self.hdwf, channel_index, c_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        status = DwfState(c_status.value)
        return status

    def nodePlayStatus(self, channel_index: int, node: DwfAnalogOutNode) -> Tuple[int, int, int]:
        """Get node play status."""
        c_data_free = typespec_ctypes.c_int()
        c_data_lost = typespec_ctypes.c_int()
        c_data_corrupted = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutNodePlayStatus(
            self.hdwf,
            channel_index,
            node.value,
            c_data_free,
            c_data_lost,
            c_data_corrupted)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        data_free = c_data_free.value
        data_lost = c_data_lost.value
        data_corrupted = c_data_corrupted.value
        return (data_free, data_lost, data_corrupted)

    def nodePlayData(self, channel_index: int, node: DwfAnalogOutNode, data: np.ndarray) -> None:
        """Configure node play data."""
        result = self.lib.FDwfAnalogOutNodePlayData(
            self.hdwf,
            channel_index,
            node.value,
            data.ctypes.data_as(typespec_ctypes.c_double_ptr),
            len(data))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    # The 25 methods that wrap obsolete functions follow:

    def triggerSourceInfo(self) -> List[DwfTriggerSource]:
        """Get analog out trigger source info.

        This function is OBSOLETE.
        """
        c_trigger_source_info_bitset = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutTriggerSourceInfo(self.hdwf, c_trigger_source_info_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        trigger_source_info_bitset = c_trigger_source_info_bitset.value
        trigger_source_info_list = [trigger_source for trigger_source in DwfTriggerSource
                                    if trigger_source_info_bitset & (1 << trigger_source.value)]
        return trigger_source_info_list

    def enableSet(self, channel_index: int, enable: bool) -> None:
        """Enable or disable the specified AnalogOut channel.

        This function is OBSOLETE. Use `nodeEnableSet` instead.
        """
        result = self.lib.FDwfAnalogOutEnableSet(self.hdwf, channel_index, enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def enableGet(self, channel_index: int) -> bool:
        """Get the current enable/disable status of the specified AnalogOut channel.

        This function is OBSOLETE. Use `nodeEnableGet` instead.
        """
        c_enable = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutEnableGet(self.hdwf, channel_index, c_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        enable = bool(c_enable.value)
        return enable

    def functionInfo(self, channel_index: int) -> List[DwfAnalogOutFunction]:
        """Get AnalogOut function info.

        This function is OBSOLETE. Use `nodeFunctionInfo` instead.
        """
        c_function_info_bitset = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfAnalogOutFunctionInfo(self.hdwf, channel_index, c_function_info_bitset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        function_info_bitset = c_function_info_bitset.value
        function_info_list = [function_ for function_ in DwfAnalogOutFunction
                              if function_info_bitset & (1 << function_.value)]
        return function_info_list

    def functionSet(self, channel_index: int, func: DwfAnalogOutFunction) -> None:
        """Set AnalogOut function.

        This function is OBSOLETE. Use `nodeFunctionSet` instead.
        """
        result = self.lib.FDwfAnalogOutFunctionSet(self.hdwf, channel_index, func.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def functionGet(self, channel_index: int) -> DwfAnalogOutFunction:
        """Get AnalogOut function.

        This function is OBSOLETE. Use `nodeFunctionGet` instead.
        """
        c_func = typespec_ctypes.FUNC()
        result = self.lib.FDwfAnalogOutFunctionGet(self.hdwf, channel_index, c_func)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        func = DwfAnalogOutFunction(c_func.value)
        return func

    def frequencyInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get AnalogOut channel frequency range info.

        This function is OBSOLETE. Use `nodeFrequencyInfo` instead.
        """
        c_hzMin = typespec_ctypes.c_double()
        c_hzMax = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutFrequencyInfo(self.hdwf, channel_index, c_hzMin, c_hzMax)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        hzMin = c_hzMin.value
        hzMax = c_hzMax.value
        return (hzMin, hzMax)

    def frequencySet(self, channel_index: int, frequency: float) -> None:
        """Set AnalogOut channel frequency, in Hz.

        This function is OBSOLETE. Use `nodeFrequencySet` instead.
        """
        result = self.lib.FDwfAnalogOutFrequencySet(self.hdwf, channel_index, frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def frequencyGet(self, channel_index: int) -> float:
        """Get AnalogOut channel frequency.

        This function is OBSOLETE. Use `nodeFrequencyGet` instead.
        """
        c_hzFrequency = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutFrequencyGet(self.hdwf, channel_index, c_hzFrequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        hzFrequency = c_hzFrequency.value
        return hzFrequency

    def amplitudeInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get AnalogOut channel amplitude range info.

        This function is OBSOLETE. Use `nodeAmplitudeInfo` instead.
        """
        c_amplitude_min = typespec_ctypes.c_double()
        c_amplitude_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutAmplitudeInfo(self.hdwf, channel_index, c_amplitude_min, c_amplitude_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        amplitude_min = c_amplitude_min.value
        amplitude_max = c_amplitude_max.value
        return (amplitude_min, amplitude_max)

    def amplitudeSet(self, channel_index: int, amplitude: float) -> None:
        """Set AnalogOut channel amplitude.

        This function is OBSOLETE. Use `nodeAmplitudeSet` instead.
        """
        result = self.lib.FDwfAnalogOutAmplitudeSet(self.hdwf, channel_index, amplitude)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def amplitudeGet(self, channel_index: int) -> float:
        """Get AnalogOut channel amplitude.

        This function is OBSOLETE. Use `nodeAmplitudeGet` instead.
        """
        c_amplitude = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutAmplitudeGet(self.hdwf, channel_index, c_amplitude)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        amplitude = c_amplitude.value
        return amplitude

    def offsetInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get AnalogOut channel offset range info.

        This function is OBSOLETE. Use `nodeOffsetInfo` instead.
        """
        c_offset_min = typespec_ctypes.c_double()
        c_offset_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutOffsetInfo(self.hdwf, channel_index, c_offset_min, c_offset_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        offset_min = c_offset_min.value
        offset_max = c_offset_max.value
        return (offset_min, offset_max)

    def offsetSet(self, channel_index: int, offset: float) -> None:
        """Set AnalogOut channel offset.

        This function is OBSOLETE. Use `nodeOffsetSet` instead.
        """
        result = self.lib.FDwfAnalogOutOffsetSet(self.hdwf, channel_index, offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def offsetGet(self, channel_index: int) -> float:
        """Get AnalogOut channel offset.

        This function is OBSOLETE. Use `nodeOffsetGet` instead.
        """
        c_offset = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutOffsetGet(self.hdwf, channel_index, c_offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        offset = c_offset.value
        return offset

    def symmetryInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get AnalogOut channel symmetry range info.

        This function is OBSOLETE. Use `nodeSymmetryInfo` instead.
        """
        c_symmetry_min = typespec_ctypes.c_double()
        c_symmetry_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutSymmetryInfo(self.hdwf, channel_index, c_symmetry_min, c_symmetry_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        symmetry_min = c_symmetry_min.value
        symmetry_max = c_symmetry_max.value
        return (symmetry_min, symmetry_max)

    def symmetrySet(self, channel_index: int, symmetry: float) -> None:
        """Set AnalogOut channel symmetry.

        This function is OBSOLETE. Use `nodeSymmetrySet` instead.
        """
        result = self.lib.FDwfAnalogOutSymmetrySet(self.hdwf, channel_index, symmetry)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def symmetryGet(self, channel_index: int) -> float:
        """Get AnalogOut channel symmetry, in percent.

        This function is OBSOLETE. Use `nodeSymmetryGet` instead.
        """
        c_symmetry = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutSymmetryGet(self.hdwf, channel_index, c_symmetry)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        symmetry = c_symmetry.value
        return symmetry

    def phaseInfo(self, channel_index: int) -> Tuple[float, float]:
        """Get AnalogOut channel phase range info.

        This function is OBSOLETE. Use `nodePhaseInfo` instead.
        """
        c_phase_min = typespec_ctypes.c_double()
        c_phase_max = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutPhaseInfo(self.hdwf, channel_index, c_phase_min, c_phase_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        phase_min = c_phase_min.value
        phase_max = c_phase_max.value
        return (phase_min, phase_max)

    def phaseSet(self, channel_index: int, phase: float) -> None:
        """Set AnalogOut channel phase.

        This function is OBSOLETE. Use `nodePhaseSet` instead.
        """
        result = self.lib.FDwfAnalogOutPhaseSet(self.hdwf, channel_index, phase)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def phaseGet(self, channel_index: int) -> float:
        """Get AnalogOut channel phase, in percent.

        This function is OBSOLETE. Use `nodePhaseGet` instead.
        """
        c_phase = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogOutPhaseGet(self.hdwf, channel_index, c_phase)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        phase = c_phase.value
        return phase

    def dataInfo(self, channel_index: int):
        """Get data buffer info.

        This function is OBSOLETE. Use `nodeDataInfo` instead.
        """
        c_num_samples_min = typespec_ctypes.c_int()
        c_num_samples_max = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutDataInfo(self.hdwf, channel_index, c_num_samples_min, c_num_samples_max)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        num_samples_min = c_num_samples_min.value
        num_samples_max = c_num_samples_max.value
        return (num_samples_min, num_samples_max)

    def dataSet(self, channel_index: int, data: np.ndarray) -> None:
        """Set data.

        This function is OBSOLETE. Use `nodeDataSet` instead.
        """

        double_data = data.astype(np.float64)

        result = self.lib.FDwfAnalogOutDataSet(
            self.hdwf,
            channel_index,
            double_data.ctypes.data_as(typespec_ctypes.c_double_ptr),
            len(double_data))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def playStatus(self, channel_index: int) -> Tuple[int, int, int]:
        """Get play status.

        This function is OBSOLETE. Use `nodePlayStatus` instead.
        """
        c_data_free = typespec_ctypes.c_int()
        c_data_lost = typespec_ctypes.c_int()
        c_data_corrupted = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogOutPlayStatus(
            self.hdwf,
            channel_index,
            c_data_free,
            c_data_lost,
            c_data_corrupted)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        data_free = c_data_free.value
        data_lost = c_data_lost.value
        data_corrupted = c_data_corrupted.value
        return (data_free, data_lost, data_corrupted)

    def playData(self, channel_index: int, data: np.ndarray) -> None:
        """Play data.

        This function is OBSOLETE.

        (Add link to replacement.)
        """

        double_data = data.astype(np.float64)

        result = self.lib.FDwfAnalogOutPlayData(
            self.hdwf,
            channel_index,
            double_data.ctypes.data_as(typespec_ctypes.c_double_ptr),
            len(double_data))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
