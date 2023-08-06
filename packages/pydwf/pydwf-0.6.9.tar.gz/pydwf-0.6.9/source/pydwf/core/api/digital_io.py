"""The |pydwf.core.api.digital_io| module implements a single class: |DigitalIO|."""

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class DigitalIO(DwfDevice_SubAPI):
    """The |DigitalIO| class provides access to the digital I/O functionality of a |DwfDevice:link|.

    The class implements 3 generic functions (reset, configure, and status), and 8 functions that come in both
    32- and 64-bits variants.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its
        public |digitalIO:link| attribute for access by the user.
    """

    def reset(self) -> None:
        """Reset all DigitalIO instrument parameters to default values.

        It sets the output enables to zero (tri-state), output value to zero, and configures the DigitalIO instrument.

        If auto-configure is enabled, the values are immediately effectuated.
        """
        result = self.lib.FDwfDigitalIOReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def configure(self) -> None:
        """Configure the DigitalIO instrument.

        This does not have to be used if AutoConfiguration is enabled."""
        result = self.lib.FDwfDigitalIOConfigure(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def status(self) -> None:
        """Read the status and input values, of the device DigitalIO to the PC.

        The status and values are accessed from the FDwfDigitalIOInputStatus function.
        """
        result = self.lib.FDwfDigitalIOStatus(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputEnableInfo(self) -> int:
        """Return the output enable mask (bit set) that can be used on this device.

        These are the pins that can be used as outputs on the device.
        """
        c_output_enable_mask = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOOutputEnableInfo(self.hdwf, c_output_enable_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_enable_mask = c_output_enable_mask.value
        return output_enable_mask

    def outputEnableSet(self, output_enable: int) -> None:
        """Enable specific pins for output.

        This is done by setting bits in the fsOutEnable bit field (1 for enabled, 0 for disabled).
        """
        result = self.lib.FDwfDigitalIOOutputEnableSet(self.hdwf, output_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputEnableGet(self) -> int:
        """Return a bit field that specifies which output pins have been enabled."""
        c_output_enable = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOOutputEnableGet(self.hdwf, c_output_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_enable = c_output_enable.value
        return output_enable

    def outputInfo(self) -> int:
        """Return the settable output value mask (bit set) that can be used on this device."""
        c_output_mask = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOOutputInfo(self.hdwf, c_output_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_mask = c_output_mask.value
        return output_mask

    def outputSet(self, output: int) -> None:
        """Set the output logic value on all output pins."""
        result = self.lib.FDwfDigitalIOOutputSet(self.hdwf, output)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputGet(self) -> int:
        """Return the currently set output values across all output pins."""
        c_output = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOOutputGet(self.hdwf, c_output)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output = c_output.value
        return output

    def inputInfo(self) -> int:
        """Return the readable input value mask (bit set) that can be used on the device."""
        c_input_mask = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOInputInfo(self.hdwf, c_input_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        input_mask = c_input_mask.value
        return input_mask

    def inputStatus(self) -> int:
        """Return the input states of all I/O pins.

        Before calling this method, call the `status` method to read the Digital I/O states from the device.
        """
        c_input = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOInputStatus(self.hdwf, c_input)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        input_ = c_input.value
        return input_

    def outputEnableInfo64(self) -> int:
        """Return the output enable mask (bit set) that can be used on this device.

        These are the pins that can be used as outputs on the device.
        """
        c_output_enable_mask = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOOutputEnableInfo64(self.hdwf, c_output_enable_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_enable_mask = c_output_enable_mask.value
        return output_enable_mask

    def outputEnableSet64(self, output_enable: int) -> None:
        """Enable specific pins for output.

        This is done by setting bits in the fsOutEnable bit field (1 for enabled, 0 for disabled).
        """
        result = self.lib.FDwfDigitalIOOutputEnableSet64(self.hdwf, output_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputEnableGet64(self) -> int:
        """Return a bit field that specifies which output pins have been enabled."""
        c_output_enable = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOOutputEnableGet64(self.hdwf, c_output_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_enable = c_output_enable.value
        return output_enable

    def outputInfo64(self) -> int:
        """Return the settable output value mask (bit set) that can be used on this device."""
        c_output_mask = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOOutputInfo64(self.hdwf, c_output_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_mask = c_output_mask.value
        return output_mask

    def outputSet64(self, output: int) -> None:
        """Set the output logic value on all output pins."""
        result = self.lib.FDwfDigitalIOOutputSet64(self.hdwf, output)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputGet64(self) -> int:
        """Return the currently set output values across all output pins."""
        c_output = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOOutputGet64(self.hdwf, c_output)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output = c_output.value
        return output

    def inputInfo64(self) -> int:
        """Return the readable input value mask (bit set) that can be used on the device."""
        c_input_mask = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOInputInfo64(self.hdwf, c_input_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        input_mask = c_input_mask.value
        return input_mask

    def inputStatus64(self) -> int:
        """Return the input states of all I/O pins.

        Before calling this method, call the `status` method to read the Digital I/O states from the device.
        """
        c_input = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOInputStatus64(self.hdwf, c_input)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        input_ = c_input.value
        return input_
