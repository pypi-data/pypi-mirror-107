"""Python equivalents of the enum types found in the C library header file *dwf.h*.

Note:
    The obsolete enum types *TRIGCOND* and *STS* that are defined in the C header file have not been defined here.
    TRIGCOND has been replaced by |DwfTriggerSlope.short|; STS has been replaced by |DwfState.short|.
"""

import enum


@enum.unique
class DwfEnumFilter(enum.Enum):
    """Device enumeration filter constants.

    This type is used exclusively by the |DwfLibrary.deviceEnum.enumerateDevices:link| method to constrain
    the type of devices that will be found during device enumeration.

    In the C API, this type is called 'ENUMFILTER', and it is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfEnumFilter.valueName".
        """
        return "DwfEnumFilter." + self.name

    All = 0
    """Enumerate all available devices."""

    EExplorer = 1
    """Enumerate only Electronics Explorer devices."""

    Discovery = 2
    """Enumerate only Analog Discovery devices."""

    Discovery2 = 3
    """Enumerate only Analog Discovery 2 devices."""

    DDiscovery = 4
    """Enumerate only Digital Discovery devices."""


@enum.unique
class DwfDeviceID(enum.Enum):
    """Device ID constants.

    This type is used exclusively by the |DwfLibrary.deviceEnum.deviceType:link| method to report on a selected device.

    In the C API, this type is called 'DEVID', and it is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfDeviceID.valueName".
        """
        return "DwfDeviceID." + self.name

    EExplorer  = 1
    """Electronics Explorer devices."""

    Discovery  = 2
    """Analog Discovery devices."""

    Discovery2 = 3
    """Analog Discovery 2 devices."""

    DDiscovery = 4
    """Digital Discovery devices."""

    ADP3X50    = 6
    """Analog Discovery Pro devices."""


class DwfDeviceVersion(enum.Enum):
    """Device versions (revisions).

    This type is used exclusively by the |DwfLibrary.deviceEnum.deviceType:link| method to report on a selected device.

    Note:
        The device revision listed here is not complete; it does not cover all devices.

        Additionally, the enumeration values :py:attr:`EExplorerC` and :py:attr:`DiscoveryB`
        have identical integer values (2).

    In the C API, this type is called 'DEVVER', and it is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfDeviceVersion.valueName".
        """
        return "DwfDeviceVersion." + self.name

    EExplorerC = 2
    """Electronics Explorer devices, revision C"""
    EExplorerE = 4
    """Electronics Explorer devices, revision E"""
    EExplorerF = 5
    """Electronics Explorer devices, revision F"""
    DiscoveryA = 1
    """Discovery devices, revision A"""
    DiscoveryB = 2
    """Discovery devices, revision B"""
    DiscoveryC = 3
    """Discovery devices, revision C"""


@enum.unique
class DwfTriggerSource(enum.Enum):
    """Trigger source.

    This type is used by the |DeviceControl| functionality and by the |AnalogIn|, |AnalogOut|, |DigitalIn|,
    and |DigitalOut| instruments.

    In the C API, this type is called 'TRIGSRC', and it is represented as an *unsigned char*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfTriggerSource.valueName".
        """
        return "DwfTriggerSource." + self.name

    None_ = 0
    """No trigger configured (device starts immediately)."""

    PC = 1
    """PC trigger."""

    DetectorAnalogIn  = 2
    """AnalogIn trigger detector."""

    DetectorDigitalIn = 3
    """DigitalIn trigger detector."""

    AnalogIn = 4
    """AnalogIn instrument start."""

    DigitalIn = 5
    """DigitalIn instrument start."""

    DigitalOut = 6
    """DigitalOut instrument start."""

    AnalogOut1 = 7
    """AnalogOut instrument channel 1 start."""

    AnalogOut2 = 8
    """AnalogOut instrument channel 2 start."""

    AnalogOut3 = 9
    """AnalogOut instrument channel 3 start."""

    AnalogOut4 = 10
    """AnalogOut instrument channel 4 start."""

    External1 = 11
    """External trigger #1"""

    External2 = 12
    """External trigger #2"""

    External3 = 13
    """External trigger #3"""

    External4 = 14
    """External trigger #4"""

    High = 15
    """High (undocumented)."""

    Low = 16
    """Low (undocumented)."""


class DwfState(enum.Enum):
    """Instrument states, for the instruments that are controlled by an internal state-machine:

    * AnalogIn
    * AnalogOut
    * DigitalIn
    * DigitalOut
    * AnalogImpedance

    Specifically, this type is used to return the state from a *status()* method.

    Note:
        The enumeration values :py:attr:`Triggered` and :py:attr:`Running` have identical integer values (3).

        The state name :py:attr:`Triggered` is used for capture instruments (|AnalogIn|, |DigitalIn|),
        while :py:attr:`Running` is used for signal generation instruments (|AnalogOut|, |DigitalOut|).

    In the C API, this type is represented as an *unsigned char*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfState.valueName".
        """
        return "DwfState." + self.name

    Ready = 0
    """The instrument is idle, waiting to be configured or started."""

    Config = 4
    """The instrument is being configured."""

    Prefill = 5
    """The instrument is collecting data prior to arming itself, so it can deliver pre-trigger samples."""

    Armed = 1
    """The instrument is collecting samples and waiting for the trigger."""

    Wait = 7
    """The signal generation instrument is waiting before its next run."""

    Triggered = 3
    """The capture instrument is triggered and collecting data."""

    Running = 3
    """The signal generation instrument is running (generating signals)."""

    Done = 2
    """The instrument has completed a measurement or signal-generating sequence."""


@enum.unique
class DwfEnumConfigInfo(enum.Enum):
    """Enum configuration info.

    This type describes device parameters that vary between device configurations.

    This type is used exclusively by the |DwfLibrary.deviceEnum.configInfo:link| method to report the capabilities
    of the different configurations of a selected device.

    In the C API, this type is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfEnumConfigInfo.valueName".
        """
        return "DwfEnumConfigInfo." + self.name

    TooltipText = -1
    """Tooltip text (undocumented).

    Maximum length: 2048 characters.

    Note: This value is not officially documented. It was revealed in a message on the Digilent forum:
        https://forum.digilentinc.com/topic/21720-small-issue-and-questions-about-device-configurations/#comment-62717
    """

    OtherInfoText = -2
    """Other info text.

    Maximum length: 256 characters.

    Note: This value is not officially documented. It was revealed in a message on the Digilent forum:
        https://forum.digilentinc.com/topic/21720-small-issue-and-questions-about-device-configurations/#comment-62717
    """

    AnalogInChannelCount = 1
    """Number of analog input channels."""

    AnalogOutChannelCount = 2
    """Number of analog output channels."""

    AnalogIOChannelCount = 3
    """Number of analog power supply channels.

    Note:
        This is a different number than the number of channels reported by the |DwfDevice.AnalogIO.channelCount:link|
        method.
    """

    DigitalInChannelCount = 4
    """Number of digital input channels."""

    DigitalOutChannelCount = 5
    """Number of digital output channels."""

    DigitalIOChannelCount = 6
    """Number of digital I/O channels."""

    AnalogInBufferSize = 7
    """Analog in buffer size, in samples."""

    AnalogOutBufferSize = 8
    """Analog out buffer size, in samples."""

    DigitalInBufferSize = 9
    """Digital in buffer size, in samples."""

    DigitalOutBufferSize = 10
    """Digital out buffer size, in samples."""


@enum.unique
class DwfAcquisitionMode(enum.Enum):
    """Acquisition mode.

    This type is used by the |AnalogIn| and |DigitalIn| instruments.

    In the C API, this type is called 'ACQMODE', and it is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfAcquisitionMode.valueName".
        """
        return "DwfAcquisitionMode." + self.name

    Single = 0
    """Perform a single buffer acquisition.

    Re-arm the instrument for the next capture after the data is fetched to the host
    using the `status` function.

    The difference with the :py:attr:`Single` mode is unclear.
    """

    ScanShift = 1
    """Perform a continuous acquisition in FIFO style.

    The trigger setting is ignored. The last sample is at the end of the buffer.
    The *statusSamplesValid* method shows the number of the acquired samples,
    which will grow until reaching the buffer size.
    After that, the waveform image is shifted for every new sample.
    """

    ScanScreen = 2
    """Perform continuous acquisition circularly writing samples into the buffer.

    This is similar to a heart-monitor display.

    The trigger setting is ignored.

    The *statusIndexWrite* value shows the buffer write position.
    """

    Record = 3
    """Perform acquisition for the length of time set by *recordLengthSet* method."""

    Overs = 4
    """Overscan mode (undocumented)."""

    Single1 = 5
    """Perform a single buffer acquisition.

    The difference with the :py:attr:`Single` mode is unclear.
    """


@enum.unique
class DwfAnalogInFilter(enum.Enum):
    """Analog acquisition filter.

    This type is used exclusively in the |AnalogIn| instrument to specify a filtering algorithm for the input-
    and trigger-channels.

    In the C API, this type is called 'FILTER", and it is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfAnalogInFilter.valueName".
        """
        return "DwfAnalogInFilter." + self.name

    Decimate = 0
    """Decimation filter."""

    Average = 1
    """Averaging filter."""

    MinMax = 2
    """Min/max filter."""


@enum.unique
class DwfTriggerType(enum.Enum):
    """Analog in trigger mode.

    This type is used exclusively in the |AnalogIn| instrument to specify the trigger type.

    In the C API, this type is called 'TRIGTYPE', and it is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfTriggerType.valueName".
        """
        return "DwfTriggerType." + self.name

    Edge = 0
    """Edge trigger type."""

    Pulse = 1
    """Pulse trigger type."""

    Transition = 2
    """Transition trigger type."""

    Window = 3
    """Window trigger type."""


@enum.unique
class DwfTriggerSlope(enum.Enum):
    """Trigger slope.

    This type is used by the |AnalogIn|, |AnalogOut|, |DigitalIn|, and |DigitalOut| instruments to select
    the trigger slope.

    In addition, the |AnalogIn| instrument uses it to select the slope of the sampling clock.

    In the C API, this type is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfTriggerSlope.valueName".
        """
        return "DwfTriggerSlope." + self.name

    Rise = 0
    """Rising trigger slope."""

    Fall = 1
    """Falling trigger slope."""

    Either = 2
    """Either rising or falling trigger slope."""


@enum.unique
class DwfTriggerLength(enum.Enum):
    """Analog in trigger length condition.

    This type is used by the |AnalogIn| instrument to specify the trigger length condition.

    Todo:
        Decide if we are going to rename this class to DwfTriggerLengthCondition.

    In the C API, this type is called 'TRIGLEN', and it is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfTriggerLength.valueName".
        """
        return "DwfTriggerLength." + self.name

    Less = 0
    """Trigger length condition 'less'."""

    Timeout = 1
    """Trigger length condition 'timeout'."""

    More = 2
    """Trigger length condition 'more'."""


@enum.unique
class DwfErrorCode(enum.Enum):
    """Error codes for the DWF public API.

    This type is used by the |DwfLibrary.getLastError:link| method to report the error condition of the most
    recent C API call.

    In |pydwf|, it is only seen as the contents of the :py:attr:`~pydwf.core.auxiliary.exceptions.DwfLibraryError.code`
    field of |DwfLibraryError:link| instances.

    In the C API, this type is called 'DWFERC', and it is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfErrorCode.valueName".
        """
        return "DwfErrorCode." + self.name

    NoErc = 0
    """No error occurred."""

    UnknownError = 1
    """Unknown error."""

    ApiLockTimeout = 2
    """API waiting on pending API timed out."""

    AlreadyOpened = 3
    """Device already opened."""

    NotSupported = 4
    """Device not supported."""

    InvalidParameter0 = 0x10
    """Invalid parameter sent in API call."""

    InvalidParameter1 = 0x11
    """Invalid parameter sent in API call."""

    InvalidParameter2 = 0x12
    """Invalid parameter sent in API call."""

    InvalidParameter3 = 0x13
    """Invalid parameter sent in API call."""

    InvalidParameter4 = 0x14
    """Invalid parameter sent in API call."""


@enum.unique
class DwfAnalogOutFunction(enum.Enum):
    """Analog out waveform function types.

    This type is used exclusively by the |AnalogOut| instrument to represent the wave-shape produced on an
    analog output channel node.

    In the C API, this type is called 'FUNC', and it is represented as an *unsigned char*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfAnalogOutFunction.valueName".
        """
        return "DwfAnalogOutFunction." + self.name

    DC        = 0
    Sine      = 1
    Square    = 2
    Triangle  = 3
    RampUp    = 4
    RampDown  = 5
    Noise     = 6
    Pulse     = 7
    Trapezium = 8
    SinePower = 9
    Custom    = 30
    Play      = 31


@enum.unique
class DwfAnalogIO(enum.Enum):
    """Analog I/O channel node types.

    This type is used exclusively by the |AnalogIO| functionality to report node information.

    In the C API, this type is called 'ANALOGIO', and it is represented as an *unsigned char*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfAnalogIO.valueName".
        """
        return "DwfAnalogIO." + self.name

    Enable      = 1
    Voltage     = 2
    Current     = 3
    Power       = 4
    Temperature = 5
    Dmm         = 6
    Range       = 7
    Measure     = 8
    Time        = 9
    Frequency   = 10


@enum.unique
class DwfAnalogOutNode(enum.Enum):
    """Analog Out node type.

    This type is used exclusively by the |AnalogOut| instrument to represent one of the
    nodes associated with each output channel.

    In the C API, this type is called 'AnalogOutNode' (without the *Dwf* prefix), and it is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfAnalogOutNode.valueName".
        """
        return "DwfAnalogOutNode." + self.name

    Carrier = 0
    FM      = 1
    AM      = 2


@enum.unique
class DwfAnalogOutMode(enum.Enum):
    """Analog Out mode (voltage or current).

    This type is used exclusively by the |AnalogOut| instrument to set or retrieve to
    mode of a channel.

    In the C API, this type is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfAnalogOutMode.valueName".
        """
        return "DwfAnalogOutMode." + self.name

    Voltage = 0
    Current = 1


@enum.unique
class DwfAnalogOutIdle(enum.Enum):
    """Analog Out idle state.

    This type is used exclusively by the |AnalogOut| instrument to set the idle behavior
    of an output channel.

    In the C API, this type is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfAnalogOutIdle.valueName".
        """
        return "DwfAnalogOutIdle." + self.name

    Disable  = 0
    Offset   = 1
    Initial  = 2


@enum.unique
class DwfDigitalInClockSource(enum.Enum):
    """Digital In clock source.

    This type is used exclusively by the |DigitalIn| instrument to specify a clock source.

    In the C API, this type is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfDigitalInClockSource.valueName".
        """
        return "DwfDigitalInClockSource." + self.name

    Internal  = 0
    External  = 1
    External2 = 2


@enum.unique
class DwfDigitalInSampleMode(enum.Enum):
    """Digital In sample mode.

    This type is used exclusively by the |DigitalIn| instrument to specify a sample mode.

    In the C API, this type is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfDigitalInSampleMode.valueName".
        """
        return "DwfDigitalInSampleMode." + self.name

    Simple = 0
    """
    Only digital samples (no noise).
    """
    Noise  = 1
    """
    Alternate samples: (noise, sample, noise, sample, …) where noise is more than 1 transition between 2 samples.
    """


@enum.unique
class DwfDigitalOutOutput(enum.Enum):
    """Digital Out output mode.

    This type is used exclusively by the |DigitalOut| instrument to specify the electronic behavior of a digital
    output channel.

    In the C API, this type is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfDigitalOutOutput.valueName".
        """
        return "DwfDigitalOutOutput." + self.name

    PushPull   = 0
    """Push/Pull"""
    OpenDrain  = 1
    """Open Drain"""
    OpenSource = 2
    """Open Source"""
    ThreeState = 3
    """Tristate (for custom and random)"""


@enum.unique
class DwfDigitalOutType(enum.Enum):
    """Digital Out type.

    This type is used exclusively by the |DigitalOut| instrument to specify the behavior mode of a digital
    output channel.

    In the C API, this type is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfDigitalOutType.valueName".
        """
        return "DwfDigitalOutType." + self.name

    Pulse  = 0
    Custom = 1
    Random = 2
    ROM    = 3
    State  = 4
    Play   = 5


@enum.unique
class DwfDigitalOutIdle(enum.Enum):
    """Digital Out idle mode.

    This type is used primarily by the |DigitalOut| instrument to specify the idle behavior mode of a digital
    output channel.

    In addition to that, it is used by the |DigitalSpi| protocol functionality to specify the idle behavior
    of the pins it controls.

    In the C API, this type is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfDigitalOutIdle.valueName".
        """
        return "DwfDigitalOutIdle." + self.name

    Init = 0
    """Same as initial value of selected output pattern."""

    Low  = 1
    """Low signal level."""

    High = 2
    """High signal level."""

    Zet  = 3
    """High impedance."""


@enum.unique
class DwfAnalogImpedance(enum.Enum):
    """Analog Impedance measurement setting.

    This type is used exclusively by the |AnalogImpedance| measurement functionality to specify a measurement type.

    In the C API, this type is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfAnalogImpedance.valueName".
        """
        return "DwfAnalogImpedance." + self.name

    Impedance           =  0  # Ohms
    ImpedancePhase      =  1  # Radians
    Resistance          =  2  # Ohms
    Reactance           =  3  # Ohms
    Admittance          =  4  # Siemens
    AdmittancePhase     =  5  # Radians
    Conductance         =  6  # Siemens
    Susceptance         =  7  # Siemens
    SeriesCapacitance   =  8  # Farad
    ParallelCapacitance =  9  # Farad
    SeriesInductance    = 10  # Henry
    ParallelInductance  = 11  # Henry
    Dissipation         = 12  # factor
    Quality             = 13  # factor


@enum.unique
class DwfParameter(enum.Enum):
    """Device parameter selection.

    This type is used to select device parameters, either to set/get global defaults (|DwfLibrary|)
    or to set/get parameters on a specific, open device (|DwfDevice|).

    In the C API, this type is called 'DwfParam', and it is represented as an *int*.
    """

    def __repr__(self):
        """Override the default Enum implementation which returns a strangely formatted string.

        Returns:
            str: A string representation of the enum value, as "DwfParameter.valueName".
        """
        return "DwfParameter." + self.name

    UsbPower = 2
    """USB power behavior if AUX power is connected.

    Possible values:

    * 0: Disable USB power.
    * 1: Keep USB power enabled.

    This setting is implemented on the Analog Discovery 2.
    """

    LedBrightness = 3
    """Set multicolor LED brightness.

    The Digital Discovery features a multi-color LED that normally emits bright blue light.

    Setting this parameter from 0 to 100 changes the LED's color to green and sets its relative brightness, in percents.

    On the Analog Discovery 2, this setting has no effect.
    """

    OnClose = 4
    """Define behavior on close.

    Possible values:

    * 0: On close, continue.
    * 1: On close, stop the device.
    * 2: On close, shut down the device.
    """

    AudioOut = 5
    """Enable or disable audio output.

    Possible values:

    * 0: Disable audio output.
    * 1: Enable audio output.

    This setting is implemented on the Analog Discovery and the Analog Discovery 2.
    """

    UsbLimit = 6
    """USB power limit.

    The value ranges from 0 to 1000, in mA. The value -1 denotes no limit.

    This setting is implemented on the Analog Discovery and the Analog Discovery 2.
    """

    AnalogOut = 7
    """Enable or disable analog output.

    Possible values:

    * 0: Disable analog output.
    * 1: Enable analog output.
    """

    Frequency = 8
    """This parameter is undocumented.

    The function of this parameter needs to be ascertained.

    It is some frequency, expressed in MHz.
    """
