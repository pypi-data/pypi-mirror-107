"""The |pydwf.core.api.digital_can| module implements a single class: |DigitalCan|."""

from typing import Tuple
import ctypes

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.auxiliary.exceptions import PyDwfError
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class DigitalCan(DwfDevice_SubAPI):
    """The |DigitalCan| class provides access to the CAN bus protocol functionality of a |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its public
        |digitalCan:link| attribute for access by the user.
    """

    def reset(self) -> None:
        """Reset the digital-CAN protocol instrument."""
        result = self.lib.FDwfDigitalCanReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def rateSet(self, data_rate: float) -> None:
        """Set the CAN data rate, in Hz."""
        result = self.lib.FDwfDigitalCanRateSet(self.hdwf, data_rate)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def polaritySet(self, high: int) -> None:
        """Set the polarity."""
        result = self.lib.FDwfDigitalCanPolaritySet(self.hdwf, high)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def txSet(self, channel_index: int) -> None:
        """Set the TX (outgoing) channel."""
        result = self.lib.FDwfDigitalCanTxSet(self.hdwf, channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def rxSet(self, channel_index: int) -> None:
        """Set the RX (incoming) channel."""
        result = self.lib.FDwfDigitalCanRxSet(self.hdwf, channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def tx(self, v_id: int, extended: bool, remote: bool, data: bytes) -> None:
        """Transmit outgoing CAN data."""
        if len(data) > 8:
            raise PyDwfError("CAN message too long.")

        # We forcefully silence mypy here.
        #
        # See: https://github.com/sidneycadot/pydwf/issues/10
        #      https://stackoverflow.com/questions/67692907

        data_as_uchar_ptr = ctypes.cast(data, typespec_ctypes.c_unsigned_char_ptr)

        result = self.lib.FDwfDigitalCanTx(
                self.hdwf,
                v_id,
                extended,
                remote,
                len(data),
                data_as_uchar_ptr
            )

        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def rx(self, size: int = 8) -> Tuple[int, bool, bool, bytes, int]:
        """Receive incoming CAN data.

        Returns:
            Tuple[int, bool, bool, bytes, int]: A tuple (vID, extended, remote, data, status)
        """

        c_vID      = typespec_ctypes.c_int()
        c_extended = typespec_ctypes.c_int()
        c_remote   = typespec_ctypes.c_int()
        c_dlc      = typespec_ctypes.c_int()
        c_data     = ctypes.create_string_buffer(size)
        c_status   = typespec_ctypes.c_int()

        result = self.lib.FDwfDigitalCanRx(
            self.hdwf,
            c_vID,
            c_extended,
            c_remote,
            c_dlc,
            ctypes.cast(c_data, typespec_ctypes.c_unsigned_char_ptr),
            size,
            c_status)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        vID      = c_vID.value
        extended = bool(c_extended.value)
        remote   = bool(c_remote.value)
        dlc      = c_dlc.value
        data     = c_data.value[:dlc]
        status   = c_status.value

        return (vID, extended, remote, data, status)
