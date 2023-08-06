"""The |pydwf.core.api.DigitalI2c| module implements a single class: |DigitalI2c|."""

from typing import List, Tuple

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class DigitalI2c(DwfDevice_SubAPI):
    """The |DigitalI2c| class provides access to the I²C protocol functionality of a |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its public
        |digitalI2c:link| attribute for access by the user.
    """

    def reset(self) -> None:
        """Reset the I²C protocol instrument."""
        result = self.lib.FDwfDigitalI2cReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def clear(self) -> int:
        """Clear the I²C bus."""
        c_bus_free = typespec_ctypes.c_int()
        result = self.lib.FDwfDigitalI2cClear(self.hdwf, c_bus_free)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        bus_free = c_bus_free.value
        return bus_free

    def stretchSet(self, stretch_enable: int) -> None:
        """Set stretch behavior."""
        result = self.lib.FDwfDigitalI2cStretchSet(self.hdwf, stretch_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def rateSet(self, rate: float) -> None:
        """Set rate."""
        result = self.lib.FDwfDigitalI2cRateSet(self.hdwf, rate)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def readNakSet(self, nak_last_read_byte: int) -> None:
        """Set read NAK state."""
        result = self.lib.FDwfDigitalI2cReadNakSet(self.hdwf, nak_last_read_byte)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def sclSet(self, channel_index: int) -> None:
        """Set SCL."""
        result = self.lib.FDwfDigitalI2cSclSet(self.hdwf, channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def sdaSet(self, channel_index: int) -> None:
        """Set SDA."""
        result = self.lib.FDwfDigitalI2cSdaSet(self.hdwf, channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def writeRead(self, address: int, tx: List[int], number_of_rx_bytes: int) -> Tuple[int, List[int]]:
        """Perform I²C combined write, read."""
        c_nak = typespec_ctypes.c_int()

        tx_list = list(tx)

        number_of_tx_bytes = len(tx_list)

        tx_buffer_type = typespec_ctypes.c_unsigned_char * number_of_tx_bytes
        rx_buffer_type = typespec_ctypes.c_unsigned_char * number_of_rx_bytes

        tx_buffer = tx_buffer_type(*tx_list)
        rx_buffer = rx_buffer_type()

        result = self.lib.FDwfDigitalI2cWriteRead(
            self.hdwf,
            address,
            tx_buffer,
            number_of_tx_bytes,
            rx_buffer,
            number_of_rx_bytes,
            c_nak)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        nak = c_nak.value

        rx_list = list(rx_buffer)

        return (nak, rx_list)

    def read(self, address: int, number_of_words: int) -> Tuple[int, List[int]]:
        """Perform I²C read."""

        c_nak = typespec_ctypes.c_int()

        buffer_type = typespec_ctypes.c_unsigned_char * number_of_words

        rx_buffer = buffer_type()

        result = self.lib.FDwfDigitalI2cRead(self.hdwf, address, rx_buffer, number_of_words, c_nak)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        nak = c_nak.value

        rx_list = list(rx_buffer)

        return (nak, rx_list)

    def write(self, address: int, tx: List[int]) -> int:
        """Perform I²C write."""

        c_nak = typespec_ctypes.c_int()

        tx_list = list(tx)

        number_of_words = len(tx_list)

        buffer_type = typespec_ctypes.c_unsigned_char * number_of_words

        tx_buffer = buffer_type(*tx_list)

        result = self.lib.FDwfDigitalI2cWrite(self.hdwf, address, tx_buffer, number_of_words, c_nak)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        nak = c_nak.value

        return nak

    def writeOne(self, address: int, tx: int) -> int:
        """Perform I²C write of a single octet."""
        c_nak = typespec_ctypes.c_int()

        result = self.lib.FDwfDigitalI2cWriteOne(self.hdwf, address, tx, c_nak)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        nak = c_nak.value

        return nak
