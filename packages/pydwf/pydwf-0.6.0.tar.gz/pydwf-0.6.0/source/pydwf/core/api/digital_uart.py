"""The |pydwf.core.api.digital_uart| module implements a single class: |DigitalUart|."""

import ctypes
from typing import Tuple

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.api.sub_api import DwfDevice_SubAPI


class DigitalUart(DwfDevice_SubAPI):
    """The |DigitalUart| class provides access to the UART protocol functionality of a |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its
        public |digitalUart:link| attribute for access by the user.
    """

    def reset(self) -> None:
        """Reset the UART protocol functionality."""
        result = self.lib.FDwfDigitalUartReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def rateSet(self, baudrate: float) -> None:
        """Set the baudrate.

        Parameters:
            baudrate (float): The baud-rate used by the receiver and transmitter.

                Commonly encountered values are 300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, and 115200,
                but other values are valid as well.
        """
        result = self.lib.FDwfDigitalUartRateSet(self.hdwf, baudrate)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def bitsSet(self, databits: int) -> None:
        """Set the number of data bits.

        Parameters:
            databits (int): The number of data-bits used by the receiver and transmitter.

                The most common choice is 8 nowadays, but other values are possible.
        """
        result = self.lib.FDwfDigitalUartBitsSet(self.hdwf, databits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def paritySet(self, parity: int) -> None:
        """Set parity.

        Parameters:
            parity (int): The parity used by the receiver and transmitter:

                * 0 — no parity;
                * 1 — odd parity;
                * 2 — even parity.

                The most common choice is no parity (i.e., 0) nowadays.
        """
        result = self.lib.FDwfDigitalUartParitySet(self.hdwf, parity)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def stopSet(self, stopbits: float) -> None:
        """Set number of stop bits.

        Note that, on the TX side, the actual number of stop-bits is the number specified here,
        rounded up to the next highest integer.

        Parameters:
            stopbits (float): The number of stop-bits used by the receiver and transmitter.

                The most common choice is 1 stop-bit. Other values that are (rarely)
                encountered are 1.5 and 2 stop-bits.
        """
        result = self.lib.FDwfDigitalUartStopSet(self.hdwf, stopbits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def txSet(self, channel_index: int) -> None:
        """Set TX channel.

        Parameters:
            channel_index (int): The channel (digital pin number) on which to transmit data.
        """
        result = self.lib.FDwfDigitalUartTxSet(self.hdwf, channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def rxSet(self, channel_index: int) -> None:
        """Set RX channel.

        Parameters:
            channel_index (int): The channel (digital pin number) on which to receive data.
        """
        result = self.lib.FDwfDigitalUartRxSet(self.hdwf, channel_index)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def tx(self, tx_data: bytes) -> None:
        """Transmit data according to the currently active settings.

        Parameters:
            tx_data (bytes): The data to be transmitted.
        """
        result = self.lib.FDwfDigitalUartTx(self.hdwf, tx_data, len(tx_data))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def rx(self, rx_max: int) -> Tuple[bytes, int]:
        """Receive data or prepare for reception.

        Important:
            This method must be called with value 0 prior to receiving data, to initialize the receiver.


        Parameters:
            rx_max (int): If 0, initialize the receiver.

                Otherwise, receive a number of characters.

        Returns:
            Tuple[bytes, int]: Bytes received and parity error indication.

            The meaning of the parity error indication is currently unclear.
        """
        c_rx_count = typespec_ctypes.c_int()
        c_parity_error = typespec_ctypes.c_int()
        c_rx_buffer = ctypes.create_string_buffer(rx_max)
        result = self.lib.FDwfDigitalUartRx(self.hdwf, c_rx_buffer, rx_max, c_rx_count, c_parity_error)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        rx_count = c_rx_count.value
        rx_buffer = c_rx_buffer.value[:rx_count]
        parity_error = c_parity_error.value
        return (rx_buffer, parity_error)
