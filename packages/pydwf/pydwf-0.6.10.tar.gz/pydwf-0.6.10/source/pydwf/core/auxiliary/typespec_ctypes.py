"""This module provides the :py:class:`typespec_ctypes` class.

It is used to map the C types found in the 'dwf.h' header file to specific *ctypes* types.
"""

import ctypes


class typespec_ctypes:
    """Map the type specifications from :py:mod:`pydwf.core.auxiliary.dwf_function_signatures` to *ctypes* types."""

    # pylint: disable=too-few-public-methods

    c_bool                      = ctypes.c_bool # Note: the use of type 'bool' in dwf.h is probably not intentional.

    c_char                      = ctypes.c_char
    c_char_ptr                  = ctypes.POINTER(c_char)
    c_char_array_16             = c_char * 16
    c_char_array_32             = c_char * 32
    c_char_array_512            = c_char * 512

    c_short                     = ctypes.c_short
    c_short_ptr                 = ctypes.POINTER(c_short)

    c_int                       = ctypes.c_int
    c_int_ptr                   = ctypes.POINTER(c_int)

    c_unsigned_char             = ctypes.c_ubyte
    c_unsigned_char_ptr         = ctypes.POINTER(c_unsigned_char)

    c_unsigned_short            = ctypes.c_ushort
    c_unsigned_short_ptr        = ctypes.POINTER(c_unsigned_short)

    c_unsigned_int              = ctypes.c_uint
    c_unsigned_int_ptr          = ctypes.POINTER(c_unsigned_int)

    c_unsigned_long_long        = ctypes.c_ulonglong
    c_unsigned_long_long_ptr    = ctypes.POINTER(c_unsigned_long_long)

    c_double                    = ctypes.c_double
    c_double_ptr                = ctypes.POINTER(c_double)
    c_double_array_32           = c_double * 32

    c_void_ptr                  = ctypes.c_void_p

    HDWF                        = c_int
    HDWF_ptr                    = ctypes.POINTER(HDWF)

    DWFERC                      = c_int
    DWFERC_ptr                  = ctypes.POINTER(DWFERC)

    ENUMFILTER                  = c_int

    TRIGSRC                     = c_unsigned_char
    TRIGSRC_ptr                 = ctypes.POINTER(TRIGSRC)

    FUNC                        = c_unsigned_char
    FUNC_ptr                    = ctypes.POINTER(FUNC)

    DEVID                       = c_int
    DEVID_ptr                   = ctypes.POINTER(DEVID)

    DEVVER                      = c_int
    DEVVER_ptr                  = ctypes.POINTER(DEVVER)

    ACQMODE                     = c_int
    ACQMODE_ptr                 = ctypes.POINTER(ACQMODE)

    ANALOGIO                    = c_unsigned_char
    ANALOGIO_ptr                = ctypes.POINTER(ANALOGIO)

    FILTER                      = c_int
    FILTER_ptr                  = ctypes.POINTER(FILTER)

    TRIGTYPE                    = c_int
    TRIGTYPE_ptr                = ctypes.POINTER(TRIGTYPE)

    TRIGLEN                     = c_int
    TRIGLEN_ptr                 = ctypes.POINTER(TRIGLEN)

    DwfState                    = c_unsigned_char
    DwfState_ptr                = ctypes.POINTER(DwfState)

    DwfAnalogOutMode            = c_int
    DwfAnalogOutMode_ptr        = ctypes.POINTER(DwfAnalogOutMode)

    DwfAnalogOutIdle            = c_int
    DwfAnalogOutIdle_ptr        = ctypes.POINTER(DwfAnalogOutIdle)

    DwfTriggerSlope             = c_int
    DwfTriggerSlope_ptr         = ctypes.POINTER(DwfTriggerSlope)

    DwfDigitalInClockSource     = c_int
    DwfDigitalInClockSource_ptr = ctypes.POINTER(DwfDigitalInClockSource)

    DwfDigitalInSampleMode      = c_int
    DwfDigitalInSampleMode_ptr  = ctypes.POINTER(DwfDigitalInSampleMode)

    DwfDigitalOutOutput         = c_int
    DwfDigitalOutOutput_ptr     = ctypes.POINTER(DwfDigitalOutOutput)

    DwfDigitalOutType           = c_int
    DwfDigitalOutType_ptr       = ctypes.POINTER(DwfDigitalOutType)

    DwfDigitalOutIdle           = c_int
    DwfDigitalOutIdle_ptr       = ctypes.POINTER(DwfDigitalOutIdle)

    DwfParam                    = c_int
    DwfEnumConfigInfo           = c_int
    DwfAnalogImpedance          = c_int

    AnalogOutNode               = c_int
