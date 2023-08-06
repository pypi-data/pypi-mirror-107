"""The |pydwf.core.api.digital_spi| module implements a single class: |DigitalSpi|."""

from typing import List

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.auxiliary.enum_types import DwfDigitalOutIdle
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class DigitalSpi(DwfDevice_SubAPI):
    """The |DigitalSpi| class provides access to the SPI protocol functionality of a |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its public
        |digitalSpi:link| attribute for access by the user.
    """

    def reset(self) -> None:
        """Reset the SPI protocol support."""
        result = self.lib.FDwfDigitalSpiReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def frequencySet(self, frequency: float) -> None:
        """Set the SPI frequency, in Hz.

        Parameters:
            frequency (float): SPI frequency, in Hz.
        """
        result = self.lib.FDwfDigitalSpiFrequencySet(self.hdwf, frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def clockSet(self, channel_index: int) -> None:
        """Set the SPI clock channel.

        Parameters:
            channel_index (int):
                Digital channel (pin) for the clock signal.
        """
        result = self.lib.FDwfDigitalSpiClockSet(self.hdwf, channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def dataSet(self, spi_data_bit: int, channel_index: int) -> None:
        """Bind SPI data bit to physical channel pin.

        Parameters:
            spi_data_bit (int):
                SPI data bit:

                * 0: DQ0 / MOSI
                * 1: DQ1 / MISO
                * 2: DQ2
                * 3: DQ3

            channel_index (int):
                Digital channel (pin) for this data bit.
        """
        result = self.lib.FDwfDigitalSpiDataSet(self.hdwf, spi_data_bit, channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def idleSet(self, spi_data_bit: int, idle_mode: DwfDigitalOutIdle) -> None:
        """Set SPI data bit idle behavior.

        Parameters:
            spi_data_bit (int):
                SPI data bit:

                * 0: DQ0 / MOSI
                * 1: DQ1 / MISO
                * 2: DQ2
                * 3: DQ3

            idle_mode (DwfDigitalOutIdle):
                Idle behavior of this bit.
        """

        result = self.lib.FDwfDigitalSpiIdleSet(self.hdwf, spi_data_bit, idle_mode.value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def modeSet(self, spi_mode: int) -> None:
        """Set the SPI mode.

        Parameters:
            spi_mode (int):

                * 0: CPOL = 0, CPHA = 0
                * 1: CPOL = 0, CPHA = 1
                * 2: CPOL = 1, CPHA = 0
                * 3: CPOL = 1, CPHA = 1
        """
        result = self.lib.FDwfDigitalSpiModeSet(self.hdwf, spi_mode)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def orderSet(self, bit_order: int) -> None:
        """Set the SPI data bit order.

        Parameters:
            bit_order (int):

                * 1: MSB first, LSB last
                * 0: LSB first, MSB last
        """
        result = self.lib.FDwfDigitalSpiOrderSet(self.hdwf, bit_order)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def select(self, channel_index: int, level: int) -> None:
        """Set the chip select (CS) status.

        Parameters:
            channel_index (int):
                Digital channel (pin) for this data bit.
            level (int):
                *  0: low
                *  1: high
                * -1: Z (high impedance)
        """
        result = self.lib.FDwfDigitalSpiSelect(self.hdwf, channel_index, level)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def writeRead(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> List[int]:
        """Write and read multiple SPI data-words, with up to 8 bits per data-word.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits per data-word (1..8).
            tx (List[int]):
                The data-words to write.
        Returns:
            List[int]: The data-words received.
        """
        tx_list = list(tx)

        number_of_words = len(tx_list)

        buffer_type = typespec_ctypes.c_unsigned_char * number_of_words

        tx_buffer = buffer_type(*tx_list)
        rx_buffer = buffer_type()

        result = self.lib.FDwfDigitalSpiWriteRead(
            self.hdwf,
            transfer_type,
            bits_per_word,
            tx_buffer,
            number_of_words,
            rx_buffer,
            number_of_words)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        rx_list = list(rx_buffer)

        return rx_list

    def writeRead16(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> List[int]:
        """Write and read multiple SPI data-words, with up to 16 bits per word.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits per data-word (1..16).
            tx (List[int]):
                The data-words to write.
        Returns:
            List[int]: The data-words received.
        """
        tx_list = list(tx)

        number_of_words = len(tx_list)

        buffer_type = typespec_ctypes.c_unsigned_short * number_of_words

        tx_buffer = buffer_type(*tx_list)
        rx_buffer = buffer_type()

        result = self.lib.FDwfDigitalSpiWriteRead16(
            self.hdwf,
            transfer_type,
            bits_per_word,
            tx_buffer,
            number_of_words,
            rx_buffer,
            number_of_words)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        rx_list = list(rx_buffer)

        return rx_list

    def writeRead32(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> List[int]:
        """Write and read multiple SPI data-words, with up to 32 bits per word.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits per data-word (1..32).
            tx (List[int]):
                The data-words to write.
        Returns:
            List[int]: The data-words received.
        """

        tx_list = list(tx)

        number_of_words = len(tx_list)

        buffer_type = typespec_ctypes.c_unsigned_int * number_of_words

        tx_buffer = buffer_type(*tx_list)
        rx_buffer = buffer_type()

        result = self.lib.FDwfDigitalSpiWriteRead32(
            self.hdwf,
            transfer_type,
            bits_per_word,
            tx_buffer,
            number_of_words,
            rx_buffer,
            number_of_words)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        rx_list = list(rx_buffer)

        return rx_list

    def read(self, transfer_type: int, bits_per_word: int, number_of_words: int) -> List[int]:
        """Read multiple SPI data-words, with up to 8 bits per word.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits per data-word (1..8).
            number_of_words (int):
                The number of data-words to read.
        Returns:
            List[int]: The data-words received.
        """

        buffer_type = typespec_ctypes.c_unsigned_char * number_of_words

        rx_buffer = buffer_type()

        result = self.lib.FDwfDigitalSpiRead(
            self.hdwf,
            transfer_type,
            bits_per_word,
            rx_buffer,
            number_of_words)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        rx_list = list(rx_buffer)

        return rx_list

    def readOne(self, transfer_type: int, bits_per_word: int) -> int:
        """Read a single SPI data-word, with up to 32 bits.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits of the data-word (1..32).
        Returns:
            int: The data-word received.
        """
        c_rx = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalSpiReadOne(self.hdwf, transfer_type, bits_per_word, c_rx)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        rx = c_rx.value
        return rx

    def read16(self, transfer_type: int, bits_per_word: int, number_of_words: int) -> List[int]:
        """Read multiple SPI data-words, with up to 16 bits per word.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits per data-word (1..16).
            number_of_words (int):
                The number of data-words to read.
        Returns:
            List[int]: The data-words received.
        """

        buffer_type = typespec_ctypes.c_unsigned_short * number_of_words

        rx_buffer = buffer_type()

        result = self.lib.FDwfDigitalSpiRead16(
            self.hdwf,
            transfer_type,
            bits_per_word,
            rx_buffer,
            number_of_words)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        rx_list = list(rx_buffer)

        return rx_list

    def read32(self, transfer_type: int, bits_per_word: int, number_of_words: int) -> List[int]:
        """Read multiple SPI data-words, with up to 32 bits per word.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits per data-word (1..32).
            number_of_words (int):
                The number of data-words to read.
        Returns:
            List[int]: The data-words received.
        """

        buffer_type = typespec_ctypes.c_unsigned_int * number_of_words

        rx_buffer = buffer_type()

        result = self.lib.FDwfDigitalSpiRead32(
            self.hdwf,
            transfer_type,
            bits_per_word,
            rx_buffer,
            number_of_words)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

        rx_list = list(rx_buffer)

        return rx_list

    def write(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> None:
        """Write multiple SPI data-words, with up to 32 bits per data-word.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits per data-word (1..32).
            tx (List[int]):
                The data-words to write.
        """
        tx_list = list(tx)

        number_of_words = len(tx_list)

        buffer_type = typespec_ctypes.c_unsigned_char * number_of_words

        tx_buffer = buffer_type(*tx_list)

        result = self.lib.FDwfDigitalSpiWrite(
            self.hdwf,
            transfer_type,
            bits_per_word,
            tx_buffer,
            number_of_words)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def writeOne(self, transfer_type: int, bits_per_word: int, tx: int) -> None:
        """Write a single SPI data-word, with up to 32 bits per data-word.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits of the data-word (1..32).
            tx (int):
                The data-word to write.
        """
        result = self.lib.FDwfDigitalSpiWriteOne(self.hdwf, transfer_type, bits_per_word, tx)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def write16(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> None:
        """Write multiple SPI data-words, with up to 16 bits per data-word.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits per data-word (1..16).
            tx (List[int]):
                The data-words to write.
        """
        tx_list = list(tx)

        number_of_words = len(tx_list)

        buffer_type = typespec_ctypes.c_unsigned_short * number_of_words

        tx_buffer = buffer_type(*tx_list)

        result = self.lib.FDwfDigitalSpiWrite16(
            self.hdwf,
            transfer_type,
            bits_per_word,
            tx_buffer,
            number_of_words)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def write32(self, transfer_type: int, bits_per_word: int, tx: List[int]) -> None:
        """Write multiple SPI data-words, with up to 32 bits per data-word.

        Parameters:
            transfer_type (int):
                * 0: SISO
                * 1: MOSI/MISO
                * 2: dual
                * 4: quad
            bits_per_word (int):
                The number of bits per data-word (1..32).
            tx (List[int]):
                The data-words to write.
        """
        tx_list = list(tx)

        number_of_words = len(tx_list)

        buffer_type = typespec_ctypes.c_unsigned_int * number_of_words

        tx_buffer = buffer_type(*tx_list)

        result = self.lib.FDwfDigitalSpiWrite32(
            self.hdwf,
            transfer_type,
            bits_per_word,
            tx_buffer, number_of_words)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
