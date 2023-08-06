"""The |pydwf.core.api.analog_impedance| module implements a single class: |AnalogImpedance|."""

from typing import Tuple

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.enum_types import DwfState, DwfAnalogImpedance
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class AnalogImpedance(DwfDevice_SubAPI):
    """The |AnalogImpedance| class provides access to the Analog Impedance measurement functionality of a
    |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its public
        |analogImpedance:link| attribute for access by the user.
    """

    # pylint: disable=too-many-public-methods

    def reset(self) -> None:
        """Reset the Analog Impedance measurement instrument."""
        result = self.lib.FDwfAnalogImpedanceReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def modeSet(self, mode: int) -> None:
        """Set mode.

        0 W1-C1-DUT-C2-R-GND, 1 W1-C1-R-C2-DUT-GND, 8 Impedance Analyzer for AD
        """
        result = self.lib.FDwfAnalogImpedanceModeSet(self.hdwf, mode)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def modeGet(self) -> int:
        """Get mode."""
        c_mode = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogImpedanceModeGet(self.hdwf, c_mode)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        mode = c_mode.value
        return mode

    def referenceSet(self, ohms: float) -> None:
        """Set reference value."""
        result = self.lib.FDwfAnalogImpedanceReferenceSet(self.hdwf, ohms)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def referenceGet(self) -> float:
        """Get reference value."""
        c_ohms = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogImpedanceReferenceGet(self.hdwf, c_ohms)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        ohms = c_ohms.value
        return ohms

    def frequencySet(self, hz: float) -> None:
        """Set frequency."""
        result = self.lib.FDwfAnalogImpedanceFrequencySet(self.hdwf, hz)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def frequencyGet(self) -> float:
        """Get frequency."""
        c_frequency = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogImpedanceFrequencyGet(self.hdwf, c_frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        frequency = c_frequency.value
        return frequency

    def amplitudeSet(self, volts: float) -> None:
        """Set amplitude value."""
        result = self.lib.FDwfAnalogImpedanceAmplitudeSet(self.hdwf, volts)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def amplitudeGet(self) -> float:
        """Get amplitude value."""
        c_amplitude = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogImpedanceAmplitudeGet(self.hdwf, c_amplitude)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        amplitude = c_amplitude.value
        return amplitude

    def offsetSet(self, volts: float) -> None:
        """Set offset value."""
        result = self.lib.FDwfAnalogImpedanceOffsetSet(self.hdwf, volts)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def offsetGet(self) -> float:
        """Get offset value."""
        c_offset = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogImpedanceOffsetGet(self.hdwf, c_offset)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        offset = c_offset.value
        return offset

    def probeSet(self, resistance: float, capacitance: float) -> None:
        """Set probe parameters.

        Parameters:
            resistance: Probe resistance, in Ohms.
            capacitance: Probe capacitance, in Farads.
        """
        result = self.lib.FDwfAnalogImpedanceProbeSet(self.hdwf, resistance, capacitance)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def probeGet(self) -> Tuple[float, float]:
        """Get probe parameters.

        Returns:
            Tuple[float, float]:
                A two-element tuple: probe resistance, in Ohms, and probe capacity, in Farads.
        """
        c_resistance = typespec_ctypes.c_double()
        c_capacity = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogImpedanceProbeGet(self.hdwf, c_resistance, c_capacity)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        resistance = c_resistance.value
        capacity = c_capacity.value
        return (resistance, capacity)

    def periodSet(self, period: int) -> None:
        """Set period."""
        result = self.lib.FDwfAnalogImpedancePeriodSet(self.hdwf, period)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def periodGet(self) -> int:
        """Get period."""
        c_period = typespec_ctypes.c_int()
        result = self.lib.FDwfAnalogImpedancePeriodGet(self.hdwf, c_period)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        period = c_period.value
        return period

    def compReset(self) -> None:
        """Reset the computation."""
        result = self.lib.FDwfAnalogImpedanceCompReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def compSet(self, open_resistance: float, open_reactance: float,
                short_resistance: float, short_reactance: float) -> None:
        """Set computation parameters.

        Parameters:
            open_resistance (float): Open-circuit resistance, in Ohms.
            open_reactance (float): Open-circuit reactance, in Ohms.
            short_resistance (float): Short-circuit resistance, in Ohms.
            short_reactance (float): Short-circuit reactance, in Ohms.
        """
        result = self.lib.FDwfAnalogImpedanceCompSet(
            self.hdwf,
            open_resistance,
            open_reactance,
            short_resistance,
            short_reactance)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def compGet(self) -> Tuple[float, float, float, float]:
        """Get computation parameters."""
        c_open_resistance = typespec_ctypes.c_double()
        c_open_reactance = typespec_ctypes.c_double()
        c_short_resistance = typespec_ctypes.c_double()
        c_short_reactance = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogImpedanceCompGet(
            self.hdwf,
            c_open_resistance,
            c_open_reactance,
            c_short_resistance,
            c_short_reactance)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        open_resistance = c_open_resistance.value
        open_reactance = c_open_reactance.value
        short_resistance = c_short_resistance.value
        short_reactance = c_short_reactance.value
        return (open_resistance, open_reactance, short_resistance, short_reactance)

    def configure(self, start: int) -> None:
        """Configure the AnalogImpedance measurement functionality."""
        result = self.lib.FDwfAnalogImpedanceConfigure(self.hdwf, start)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def status(self) -> DwfState:
        """Return the status of the AnalogImpedance pseudo-instrument."""
        c_status = typespec_ctypes.DwfState()
        result = self.lib.FDwfAnalogImpedanceStatus(self.hdwf, c_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        status_ = DwfState(c_status.value)
        return status_

    def statusInput(self, channel_index: int) -> Tuple[float, float]:
        """Get input status."""
        c_gain = typespec_ctypes.c_double()
        c_radian = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogImpedanceStatusInput(
            self.hdwf,
            channel_index,
            c_gain,
            c_radian)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        gain = c_gain.value
        radian = c_radian.value
        return (gain, radian)

    def statusMeasure(self, measure: DwfAnalogImpedance) -> float:
        """Perform measurement."""
        c_value = typespec_ctypes.c_double()
        result = self.lib.FDwfAnalogImpedanceStatusInput(self.hdwf, measure.value, c_value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        value = c_value.value
        return value
