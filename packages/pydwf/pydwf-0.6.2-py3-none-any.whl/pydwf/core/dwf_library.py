"""The |pydwf.core.dwf_library| module implements a single class: |DwfLibrary|."""

import sys
import ctypes

from pydwf.core.auxiliary.dwf_function_signatures import dwf_function_signatures, dwf_version as expected_dwf_version
from pydwf.core.auxiliary.exceptions import PyDwfError, DwfLibraryError
from pydwf.core.auxiliary.enum_types import DwfErrorCode, DwfParameter
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.api.device_enumeration import DeviceEnumeration
from pydwf.core.api.device_control import DeviceControl


class DwfLibrary:
    """The |DwfLibrary| class provides access to miscellaneous DWF functions, and to |device enumeration:link| and
    |device control:link| functionality via its |deviceEnum:link| and |deviceControl:link| attributes:

    Attributes:
        deviceEnum (DeviceEnumeration):
            Provides access to the |device enumeration:link| functionality.
        deviceControl (DeviceControl):
            Provides access to the |device control:link| functionality.
    """

    def __init__(self, check_library_version: bool = True) -> None:
        """Initialize a |DwfLibrary| instance.

        This method instantiates a |ctypes| shared library, type-annotates its functions, and initializes the
        |deviceEnum:link| and |deviceControl:link| attributes that provide access to |device enumeration:link| and
        |device control:link| functionality.

        Parameters:
            check_library_version (bool): If True (the default), the version number of the C library will be checked
                against the version of the DWF library that matches the type information used by |pydwf|. In case of
                a mismatch, an exception will be raised.

        Raises:
            PyDwfError: The version check failed, or a version mismatch was detected.
        """

        if sys.platform.startswith("win"):
            lib = ctypes.cdll.dwf
        elif sys.platform.startswith("darwin"):
            lib = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            lib = ctypes.cdll.LoadLibrary("libdwf.so")

        if check_library_version:
            # Note that the 'FDwfGetVersion' function has not been type-annotated yet here.
            c_version = ctypes.create_string_buffer(32)
            result = lib.FDwfGetVersion(c_version)
            if result != RESULT_SUCCESS:
                raise PyDwfError("Unable to verify library version")
            actual_dwf_version = c_version.value.decode()
            if actual_dwf_version != expected_dwf_version:
                raise PyDwfError("DWF library version mismatch: pydwf module expects {},"
                                 " but actual library is version {}".format(
                    expected_dwf_version, actual_dwf_version))

        self._annotate_function_signatures(lib)

        self._lib = lib

        # Initialize sub-API instances and assign them to attributes.

        self.deviceEnum = DeviceEnumeration(self)
        self.deviceControl = DeviceControl(self)

    @property
    def lib(self) -> ctypes.CDLL:
        """Return the |ctypes| shared library instance used to access the DWF library.

        This property is primarily provided for internal |pydwf| use.

        :meta private:
        """
        return self._lib

    @staticmethod
    def _annotate_function_signatures(lib: ctypes.CDLL) -> None:
        """Add |ctypes| return type and parameter type annotations for all known functions in the DWF shared library.

        This function uses a list of DWF function signatures derived from the *dwf.h* C header file to perform
        the type annotation.

        Parameters:
            lib (ctypes.CDLL): The shared library whose functions will be type-annotated.

        This method is intended exclusively for internal |pydwf| use by the :py:meth:`__init__` method.
        """

        function_signatures = dwf_function_signatures(typespec_ctypes)

        for (name, restype, argtypes, _obsolete_flag) in function_signatures:
            argtypes = [argtype for (argname, argtype) in argtypes]
            try:
                func = getattr(lib, name)
                func.restype = restype
                func.argtypes = argtypes
            except AttributeError:
                # Do not annotate functions that are not present in the shared library.
                # This can happen, for example, when pydwf is used with an older version of the shared library.
                pass

    def exception(self) -> DwfLibraryError:
        """Return an exception describing the most recent error.

        This method is used by |pydwf| to generate a descriptive |DwfLibraryError:link| exception
        in case a DWF C library function has just failed.

        This method should not be called by |pydwf| users. It is for internal |pydwf| use only.

        Note that this function *returns* an exception instance; it doesn't *raise* it.

        Returns:
            DwfLibraryError: an exception describing the error reported by the last DWF library call.

        :meta private:
        """
        return DwfLibraryError(self.getLastError(), self.getLastErrorMsg())

    def getLastError(self) -> DwfErrorCode:
        """Retrieve the last error code in the calling process.

        The error code is cleared when other API functions are called and is only set when an API function
        fails during execution.

        When using |pydwf| there is no need to call this method directly, since low-level errors reported by the
        C library are automatically converted to a |DwfLibraryError:link| exception, which includes
        both the error code and the corresponding message.

        Returns:
            DwfErrorCode: The DWF error code of last API call.

        Raises:
            DwfLibraryError: the last error code cannot be retrieved.
        """
        c_dwferc = typespec_ctypes.DWFERC()
        result = self._lib.FDwfGetLastError(c_dwferc)
        if result != RESULT_SUCCESS:
            # If the FDwfGetLastError call itself fails, we cannot get a proper error code or message.
            raise DwfLibraryError(None, "FDwfGetLastError() failed.")
        dwferc = DwfErrorCode(c_dwferc.value)
        return dwferc

    def getLastErrorMsg(self) -> str:
        """Retrieve the last error message.

        The error message is cleared when other API functions are called and is only set when an API function
        fails during execution.

        When using |pydwf| there is no need to call this method directly, since low-level errors reported by the
        C library are automatically converted to a |DwfLibraryError:link| exception, which includes
        both the error code and the corresponding message.

        Returns:
            str: The error message of the last API call.

            The description may consist of multiple of messages, separated by a newline character,
            that describe the events leading to the error.

        Raises:
            DwfLibraryError: The last error message cannot be retrieved.
        """
        c_error_message = ctypes.create_string_buffer(512)
        result = self._lib.FDwfGetLastErrorMsg(c_error_message)
        if result != RESULT_SUCCESS:
            raise DwfLibraryError(None, "FDwfGetLastErrorMsg() failed.")
        error_message = c_error_message.value.decode()
        return error_message

    def getVersion(self) -> str:
        """Retrieve the library version string.

        Returns:
            str: The version of the DWF C library, composed of major, minor, and build numbers
            (e.g., "|libdwf-version|").

        Raises:
            DwfLibraryError: The library version string cannot be retrieved.
        """
        c_version = ctypes.create_string_buffer(32)
        result = self._lib.FDwfGetVersion(c_version)
        if result != RESULT_SUCCESS:
            raise self.exception()
        version = c_version.value.decode()
        return version

    def paramSet(self, parameter: DwfParameter, value: int) -> None:
        """Configure a default parameter value.

        Parameters are settings of a specific |DwfDevice|.
        Different |DwfDevice| instances can have different values for each of the possible |DwfParameter| parameters.

        This method sets parameter values at the library level.
        They are used as default parameters for devices that are opened subsequently.

        Warning:
            The parameter values are not checked to make sure they correspond to a valid value
            for the specific parameter.

        Parameters:
            parameter (DwfParameter): The parameter to set.
            value (int): The desired parameter value.

        Raises:
            DwfLibraryError: The parameter value cannot be set.
        """
        result = self._lib.FDwfParamSet(parameter.value, value)
        if result != RESULT_SUCCESS:
            raise self.exception()

    def paramGet(self, parameter: DwfParameter) -> int:
        """Return a default parameter value.

        Parameters are settings of a specific |DwfDevice|.
        Different |DwfDevice| instances can have different values for each of the possible |DwfParameter| parameters.

        This method retrieves parameter values at the library level.
        They are used as default parameters for devices that are opened subsequently.

        Parameters:
            parameter (DwfParameter): The parameter for which to get the value.

        Returns:
            int: The retrieved parameter value.

        Raises:
            DwfLibraryError: The parameter value cannot be retrieved.
        """
        c_value = typespec_ctypes.c_int()
        result = self._lib.FDwfParamGet(parameter.value, c_value)
        if result != RESULT_SUCCESS:
            raise self.exception()
        value = c_value.value
        return value
