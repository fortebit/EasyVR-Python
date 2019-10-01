"""
.. module:: easyvr

**************
EasyVR Library
**************

    | **EasyVR library for Python/Zerynth v1.11.1**
    | *Copyright (C) 2019 ROBOTECH srl*
    |

    Written for Python and Zerynth compatible boards for use with EasyVR modules or
    EasyVR Shield boards produced by RoboTech srl with the `Fortebit <http://fortebit.tech>`_
    brand (formerly `VeeaR <http://www.veear.eu>`_)

    Released under the terms of the MIT license, as found in the accompanying
    file COPYING.txt or at this address: `<http://www.opensource.org/licenses/MIT>`_

    """

# EasyVR protocol definitions

_CMD_BREAK        = b'b' # abort recog or ping
_CMD_SLEEP        = b's' # go to power down
_CMD_KNOB         = b'k' # set si knob <1>
_CMD_MIC_DIST     = b'k' # set microphone (<1>=-1) distance <2>
_CMD_LEVEL        = b'v' # set sd level <1>
_CMD_VERIFY_RP    = b'v' # verify filesystem (<1>=-1) with flags <2> (0=check only, 1=fix)
_CMD_LANGUAGE     = b'l' # set si language <1>
_CMD_LIPSYNC      = b'l' # start real-time lipsync (<1>=-1) with threshold <2-3>, timeout <4-5>
_CMD_TIMEOUT      = b'o' # set timeout <1>
_CMD_RECOG_SI     = b'i' # do si recog from ws <1>
_CMD_TRAIN_SD     = b't' # train sd command at group <1> pos <2>
_CMD_TRAILING     = b't' # set trailing (<1>=-1) silence <2> (0-31 = 100-875 milliseconds)
_CMD_GROUP_SD     = b'g' # insert new command at group <1> pos <2>
_CMD_UNGROUP_SD   = b'u' # remove command at group <1> pos <2>
_CMD_RECOG_SD     = b'd' # do sd recog at group <1> (0 = trigger mixed si/sd)
_CMD_DUMP_RP      = b'd' # dump message (<1>=-1) at pos <2>
_CMD_ERASE_SD     = b'e' # reset command at group <1> pos <2>
_CMD_ERASE_RP     = b'e' # erase recording (<1>=-1) at pos <2>
_CMD_NAME_SD      = b'n' # label command at group <1> pos <2> with length <3> name <4-n>
_CMD_COUNT_SD     = b'c' # get command count for group <1>
_CMD_DUMP_SD      = b'p' # read command data at group <1> pos <2>
_CMD_PLAY_RP      = b'p' # play recording (<1>=-1) at pos <2> with flags <3>
_CMD_MASK_SD      = b'm' # get active group mask
_CMD_RESETALL     = b'r' # reset all memory (commands/groups and messages), with <1>='R'
_CMD_RESET_SD     = b'r' # reset only commands/groups, with <1>='D'
_CMD_RESET_RP     = b'r' # reset only messages, with <1>='M'
_CMD_RECORD_RP    = b'r' # record message (<1>=-1) at pos <2> with bits <3> and timeout <4>
_CMD_ID           = b'x' # get version id
_CMD_DELAY        = b'y' # set transmit delay <1> (log scale)
_CMD_BAUDRATE     = b'a' # set baudrate <1> (bit time, 1=>115200)
_CMD_QUERY_IO     = b'q' # configure, read or write I/O pin <1> of type <2>
_CMD_PLAY_SX      = b'w' # wave table entry <1-2> (10-bit) playback at volume <3>
_CMD_PLAY_DTMF    = b'w' # play (<1>=-1) dial tone <2> for duration <3>
_CMD_DUMP_SX      = b'h' # dump wave table entries
_CMD_DUMP_SI      = b'z' # dump si settings for ws <1> (or total ws count if -1)
_CMD_SEND_SN      = b'j' # send sonicnet token with bits <1> index <2-3> at time <4-5>
_CMD_RECV_SN      = b'f' # receive sonicnet token with bits <1> rejection <2> timeout <3-4>
_CMD_FAST_SD      = b'f' # set sd/sv (<1>=-1) to use fast recognition <2> (0=normal/default, 1=fast)

_CMD_SERVICE      = b'~' # send service request
_SVC_EXPORT_SD    = b'X' # request export of command <2> in group <1> as raw dump
_SVC_IMPORT_SD    = b'I' # request import of command <2> in group <1> as raw dump
_SVC_VERIFY_SD    = b'V' # verify training of imported raw command <2> in group <1>

_STS_SERVICE      = b'~' # get service reply
_SVC_DUMP_SD      = b'D' # provide raw command data <1-512> followed by checksum <513-516>

_STS_MASK         = b'k' # mask of active groups <1-8>
_STS_COUNT        = b'c' # count of commands <1> (or number of ws <1>)
_STS_AWAKEN       = b'w' # back from power down mode
_STS_DATA         = b'd' # provide training <1>, conflict <2>, command label <3-35> (counted string)
_STS_ERROR        = b'e' # signal error code <1-2>
_STS_INVALID      = b'v' # invalid command or argument
_STS_TIMEOUT      = b't' # timeout expired
_STS_LIPSYNC      = b'l' # lipsync stream follows
_STS_INTERR       = b'i' # back from aborted recognition (see 'break')
_STS_SUCCESS      = b'o' # no errors status
_STS_RESULT       = b'r' # recognised sd command <1> - training similar to sd <1>
_STS_SIMILAR      = b's' # recognised si <1> (in mixed si/sd) - training similar to si <1>
_STS_OUT_OF_MEM   = b'm' # no more available commands (see 'group')
_STS_ID           = b'x' # provide version id <1>
_STS_PIN          = b'p' # return pin state <1>
_STS_TABLE_SX     = b'h' # table entries count <1-2> (10-bit), table name <3-35> (counted string)
_STS_GRAMMAR      = b'z' # si grammar: flags <1>, word count <2>, labels... <3-35> (n counted strings)
_STS_TOKEN        = b'f' # received sonicnet token <1-2>
_STS_MESSAGE      = b'g' # message status <1> (0=empty, 4/8=bits format), length <2-7>

# protocol arguments are in the range 0x40 (-1) to 0x60 (+31) inclusive
_ARG_MIN      = 0x40
_ARG_MAX      = 0x60
_ARG_ZERO     = 0x41

_ARG_ACK      = b' '     # to read more status arguments


# Define abstractions for different python environments

#-if TARGET

# TARGET symbol is always defined by Zerynth compiler
# On different python environments both code sections are executed,
# so the following functions will be overwritten

def _available(stream):
    return stream.available()

def _delay(ms):
    sleep(ms)

#-else

_api = False
try:
    # use CPython/circuitpython
    from time import sleep
    def _delay(ms):
        sleep(0.001*ms)
    def _available(stream):
        return stream.in_waiting
    _api = True
except:
    pass
if not _api:
    try:
        # use micropython
        from utime import sleep_ms
        def _delay(ms):
            sleep_ms(ms)
        def _available(stream):
            return stream.any()
        _api = True
    except:
        pass
if not _api:
    raise RuntimeException # python api not supported
del _api

#-endif

class EasyVR():
    """
.. class:: EasyVR

    The EasyVR class implements the serial communication protocol of the EasyVR series of voice recognition modules.
    
    Some class attributes here below can be used as arguments to EasyVR object's methods and to test returned values.
    
.. _ModuleId:

    **ModuleId** - Module identification number (firmware version):
  
        * ``VRBOT`` Identifies a VRbot module 
        * ``EASYVR`` Identifies an EasyVR module 
        * ``EASYVR2`` Identifies an EasyVR module version 2 
        * ``EASYVR2_3`` Identifies an EasyVR module version 2, firmware revision 3 
        * ``EASYVR3`` Identifies an EasyVR module version 3, firmware revision 0 
        * ``EASYVR3_1`` Identifies an EasyVR module version 3, firmware revision 1 
        * ``EASYVR3_2`` Identifies an EasyVR module version 3, firmware revision 2 
        * ``EASYVR3_3`` Identifies an EasyVR module version 3, firmware revision 3 
        * ``EASYVR3_4`` Identifies an EasyVR module version 3, firmware revision 4 
        * ``EASYVR3_5`` Identifies an EasyVR module version 3, firmware revision 5 
        * ``EASYVR3PLUS`` Identifies an EasyVR module version 3+, firmware revision 0 
  
.. _Language:

    **Language** - Language to use for recognition of built-in words:
  
        * ``ENGLISH`` Uses the US English word sets 
        * ``ITALIAN`` Uses the Italian word sets 
        * ``JAPANESE`` Uses the Japanese word sets 
        * ``GERMAN`` Uses the German word sets 
        * ``SPANISH`` Uses the Spanish word sets 
        * ``FRENCH`` Uses the French word sets 
  
.. _Group:

    **Group** - Special group numbers for recognition of custom commands:
  
        * ``TRIGGER`` The trigger group (shared with built-in trigger word) 
        * ``PASSWORD`` The password group (uses speaker verification technology) 
  
.. _Wordset:

    **Wordset** - Index of built-in word sets:
  
        * ``TRIGGER_SET`` The built-in trigger word set 
        * ``ACTION_SET`` The built-in action word set 
        * ``DIRECTION_SET`` The built-in direction word set 
        * ``NUMBER_SET`` The built-in number word set 
  
.. _Distance:

    **Distance** - Microphone distance from the user's mouth, used by all recognition technologies:
  
        * ``HEADSET`` Nearest range (around 5cm) 
        * ``ARMS_LENGTH`` Medium range (from about 50cm to 1m) 
        * ``FAR_MIC`` Farthest range (up to 3m) 
  
.. _Knob:

    **Knob** - Confidence thresholds for the knob settings, used for recognition of built-in words or custom grammars (not used for the mixed trigger group):
  
        * ``LOOSER`` Lowest threshold, most results reported 
        * ``LOOSE`` Lower threshold, more results reported 
        * ``TYPICAL`` Typical threshold (default) 
        * ``STRICT`` Higher threshold, fewer results reported 
        * ``STRICTER`` Highest threshold, fewest results reported 
  
.. _Level:

    **Level** - Strictness values for the level settings, used for recognition of custom commands (not used for the mixed trigger group):
  
        * ``EASY`` Lowest value, most results reported 
        * ``NORMAL`` Typical value (default) 
        * ``HARD`` Slightly higher value, fewer results reported 
        * ``HARDER`` Higher value, fewer results reported 
        * ``HARDEST`` Highest value, fewest results reported 
  
.. _TrailingSilence:

    **TrailingSilence** - Trailing silence settings used for recognition of built-in words or custom grammars (including the mixed trigger group), in a range from 100ms to 875ms in steps of 25ms:
  
        * ``TRAILING_MIN`` Lowest value (100ms), minimum latency 
        * ``TRAILING_DEF`` Default value (400ms) after power on or reset 
        * ``TRAILING_MAX`` Highest value (875ms), maximum latency 
        * ``TRAILING_100MS`` Silence duration is 100ms 
        * ``TRAILING_200MS`` Silence duration is 200ms 
        * ``TRAILING_300MS`` Silence duration is 300ms 
        * ``TRAILING_400MS`` Silence duration is 400ms 
        * ``TRAILING_500MS`` Silence duration is 500ms 
        * ``TRAILING_600MS`` Silence duration is 600ms 
        * ``TRAILING_700MS`` Silence duration is 700ms 
        * ``TRAILING_800MS`` Silence duration is 800ms 
  
.. _CommandLatency:

    **CommandLatency** - Latency settings used for recognition of custom commands or passwords (excluding the mixed trigger group):
  
        * ``MODE_NORMAL`` Normal settings (default), higher latency 
        * ``MODE_FAST`` Fast settings, better response time 
  
.. _Baudrate:

    **Baudrate** - Constants to use for baudrate settings:
  
        * ``B115200`` 115200 bps 
        * ``B57600`` 57600 bps 
        * ``B38400`` 38400 bps 
        * ``B19200`` 19200 bps 
        * ``B9600`` 9600 bps (default) 
  
.. _WakeMode:

    **WakeMode** - Constants for choosing wake-up method in sleep mode:
  
        * ``WAKE_ON_CHAR`` Wake up on any character received 
        * ``WAKE_ON_WHISTLE`` Wake up on whistle or any character received 
        * ``WAKE_ON_LOUDSOUND`` Wake up on a loud sound or any character received 
        * ``WAKE_ON_2CLAPS`` Wake up on double hands-clap or any character received 
        * ``WAKE_ON_3CLAPS`` Wake up on triple hands-clap or any character received 
  
.. _ClapSense:

    **ClapSense** - Hands-clap sensitivity for wakeup from sleep mode. Use in combination with ``WAKE_ON_2CLAPS`` or ``WAKE_ON_3CLAPS``:
  
        * ``CLAP_SENSE_LOW`` Lowest threshold 
        * ``CLAP_SENSE_MID`` Typical threshold 
        * ``CLAP_SENSE_HIGH`` Highest threshold 
  
.. _PinConfig:

    **PinConfig** - Pin configuration options for the extra I/O connector:
  
        * ``OUTPUT_LOW`` Pin is an output at low level (0V) 
        * ``OUTPUT_HIGH`` Pin is an output at high level (3V) 
        * ``INPUT_HIZ`` Pin is an high impedance input 
        * ``INPUT_STRONG`` Pin is an input with strong pull-up (~10K) 
        * ``INPUT_WEAK`` Pin is an input with weak pull-up (~200K) 
  
.. _PinNumber:

    **PinNumber** - Available pin numbers on the extra I/O connector:
  
        * ``IO1`` Identifier of pin IO1 
        * ``IO2`` Identifier of pin IO2 
        * ``IO3`` Identifier of pin IO3 
        * ``IO4`` Identifier of pin IO4 [only EasyVR3] 
        * ``IO5`` Identifier of pin IO5 [only EasyVR3] 
        * ``IO6`` Identifier of pin IO6 [only EasyVR3] 
  
.. _SoundVolume:

    **SoundVolume** - Some quick volume settings for the sound playback functions (any value in the range 0-31 can be used):
  
        * ``VOL_MIN`` Lowest volume (almost mute) 
        * ``VOL_HALF`` Half scale volume (softer) 
        * ``VOL_FULL`` Full scale volume (normal) 
        * ``VOL_DOUBLE`` Double gain volume (louder) 
  
.. _SoundIndex:

    **SoundIndex** - Special sound index values, always available even when no soundtable is present:
  
        * ``BEEP`` Beep sound 
  
.. _GrammarFlag:

    **GrammarFlag** - Flags used by custom grammars:
  
        * ``GF_TRIGGER`` A bit mask that indicate grammar is a trigger (opposed to commands) 
  
.. _RejectionLevel:

    **RejectionLevel** - Noise rejection level for SonicNet token detection (higher value, fewer results):
  
        * ``REJECTION_MIN`` Lowest noise rejection, highest sensitivity 
        * ``REJECTION_AVG`` Medium noise rejection, medium sensitivity 
        * ``REJECTION_MAX`` Highest noise rejection, lowest sensitivity 
  
.. _MessageSpeed:

    **MessageSpeed** - Playback speed for recorded messages:
  
        * ``SPEED_NORMAL`` Normal playback speed 
        * ``SPEED_FASTER`` Faster playback speed 
  
.. _MessageAttenuation:

    **MessageAttenuation** - Playback attenuation for recorded messages:
  
        * ``ATTEN_NONE`` No attenuation (normalized volume) 
        * ``ATTEN_2DB2`` Attenuation of -2.2dB 
        * ``ATTEN_4DB5`` Attenuation of -4.5dB 
        * ``ATTEN_6DB7`` Attenuation of -6.7dB 
  
.. _MessageType:

    **MessageType** - Type of recorded message:
  
        * ``MSG_EMPTY`` Empty message slot 
        * ``MSG_8BIT`` Message recorded with 8-bits PCM 
  
.. _LipsyncThreshold:

    **LipsyncThreshold** - Threshold for real-time lip-sync:
  
        * ``RTLS_THRESHOLD_DEF`` Default threshold 
        * ``RTLS_THRESHOLD_MAX`` Maximum threshold 
  
.. _ErrorCode:

    **ErrorCode** - Error codes used by various functions:
  
    *Data collection errors (patgen, wordspot, t2si)*
        * ``ERR_DATACOL_TOO_LONG`` too long (memory overflow) 
        * ``ERR_DATACOL_TOO_NOISY`` too noisy 
        * ``ERR_DATACOL_TOO_SOFT`` spoke too soft 
        * ``ERR_DATACOL_TOO_LOUD`` spoke too loud 
        * ``ERR_DATACOL_TOO_SOON`` spoke too soon 
        * ``ERR_DATACOL_TOO_CHOPPY`` too many segments/too complex 
        * ``ERR_DATACOL_BAD_WEIGHTS`` invalid SI weights 
        * ``ERR_DATACOL_BAD_SETUP`` invalid setup 

    *Recognition errors (si, sd, sv, train, t2si)*
        * ``ERR_RECOG_FAIL`` recognition failed 
        * ``ERR_RECOG_LOW_CONF`` recognition result doubtful 
        * ``ERR_RECOG_MID_CONF`` recognition result maybe 
        * ``ERR_RECOG_BAD_TEMPLATE`` invalid SD/SV template 
        * ``ERR_RECOG_BAD_WEIGHTS`` invalid SI weights 
        * ``ERR_RECOG_DURATION`` incompatible pattern durations 

    *T2si errors (t2si)*
        * ``ERR_T2SI_EXCESS_STATES`` state structure is too big 
        * ``ERR_T2SI_BAD_VERSION`` RSC code version/Grammar ROM dont match 
        * ``ERR_T2SI_OUT_OF_RAM`` reached limit of available RAM 
        * ``ERR_T2SI_UNEXPECTED`` an unexpected error occurred 
        * ``ERR_T2SI_OVERFLOW`` ran out of time to process 
        * ``ERR_T2SI_PARAMETER`` bad macro or grammar parameter 

        * ``ERR_T2SI_NN_TOO_BIG`` layer size out of limits 
        * ``ERR_T2SI_NN_BAD_VERSION`` net structure incompatibility 
        * ``ERR_T2SI_NN_NOT_READY`` initialization not complete 
        * ``ERR_T2SI_NN_BAD_LAYERS`` not correct number of layers 

        * ``ERR_T2SI_TRIG_OOV`` trigger recognized Out Of Vocabulary 
        * ``ERR_T2SI_TOO_SHORT`` utterance was too short 

    *Record and Play errors (standard RP and messaging)*
        * ``ERR_RP_BAD_LEVEL``  play - illegal compression level 
        * ``ERR_RP_NO_MSG``  play, erase, copy - msg doesn't exist 
        * ``ERR_RP_MSG_EXISTS``  rec, copy - msg already exists 

    *Synthesis errors (talk, sxtalk)*
        * ``ERR_SYNTH_BAD_VERSION`` bad release number in speech file 
        * ``ERR_SYNTH_ID_NOT_SET`` (obsolete) bad sentence structure 
        * ``ERR_SYNTH_TOO_MANY_TABLES`` (obsolete) too many talk tables 
        * ``ERR_SYNTH_BAD_SEN`` (obsolete) bad sentence number 
        * ``ERR_SYNTH_BAD_MSG`` bad message data or SX technology files missing 

    *Custom errors*
        * ``ERR_CUSTOM_NOTA`` none of the above (out of grammar) 
        * ``ERR_CUSTOM_INVALID`` invalid data (for memory check) 

    *Internal errors (all)*
        * ``ERR_SW_STACK_OVERFLOW`` no room left in software stack 
        * ``ERR_INTERNAL_T2SI_BAD_SETUP`` T2SI test mode error 
  
.. _BridgeMode:

    **BridgeMode** - Type of Bridge mode requested :
  
        * ``BRIDGE_NONE`` Bridge mode has not been requested 
        * ``BRIDGE_NORMAL`` Normal bridge mode (EasyVR baudrate 9600) 
        * ``BRIDGE_BOOT`` Bridge mode for EasyVR bootloader (baudrate 115200) 
        * ``BRIDGE_ESCAPE_CHAR`` Special character to enter/exit Bridge mode 

    """

    # status flags
    _is_command   = 0x001
    _is_builtin   = 0x002
    _is_error     = 0x004
    _is_timeout   = 0x008
    _is_invalid   = 0x010
    _is_memfull   = 0x020
    _is_conflict  = 0x040
    _is_token     = 0x080
    _is_awakened  = 0x100

    # timeout constants
    _NO_TIMEOUT = 0
    _INFINITE   = -1

    # overridable constants
    DEF_TIMEOUT     = 200
    WAKE_TIMEOUT    = 300
    PLAY_TIMEOUT    = 5000
    TOKEN_TIMEOUT   = 1500
    STORAGE_TIMEOUT = 500

    """ Module identification number (firmware version) """
    VRBOT       = 0     #: Identifies a VRbot module
    EASYVR      = 1     #: Identifies an EasyVR module
    EASYVR2     = 2     #: Identifies an EasyVR module version 2
    EASYVR2_3   = 3     #: Identifies an EasyVR module version 2, firmware revision 3
    EASYVR3     = 8     #: Identifies an EasyVR module version 3, firmware revision 0
    EASYVR3_1   = 9     #: Identifies an EasyVR module version 3, firmware revision 1
    EASYVR3_2   = 10    #: Identifies an EasyVR module version 3, firmware revision 2
    EASYVR3_3   = 11    #: Identifies an EasyVR module version 3, firmware revision 3
    EASYVR3_4   = 12    #: Identifies an EasyVR module version 3, firmware revision 4
    EASYVR3_5   = 13    #: Identifies an EasyVR module version 3, firmware revision 5
    EASYVR3PLUS = 16    #: Identifies an EasyVR module version 3+, firmware revision 0

    """ Language to use for recognition of built-in words """
    ENGLISH     = 0     #: Uses the US English word sets
    ITALIAN     = 1     #: Uses the Italian word sets
    JAPANESE    = 2     #: Uses the Japanese word sets
    GERMAN      = 3     #: Uses the German word sets
    SPANISH     = 4     #: Uses the Spanish word sets
    FRENCH      = 5     #: Uses the French word sets

    """ Special group numbers for recognition of custom commands """
    TRIGGER     = 0     #: The trigger group (shared with built-in trigger word)
    PASSWORD    = 16    #: The password group (uses speaker verification technology)

    """ Index of built-in word sets """
    TRIGGER_SET     = 0 #: The built-in trigger word set
    ACTION_SET      = 1 #: The built-in action word set
    DIRECTION_SET   = 2 #: The built-in direction word set
    NUMBER_SET      = 3 #: The built-in number word set

    """ Microphone distance from the user's mouth,
    used by all recognition technologies """
    HEADSET     = 1 #: Nearest range (around 5cm)
    ARMS_LENGTH = 2 #: Medium range (from about 50cm to 1m)
    FAR_MIC     = 3 #: Farthest range (up to 3m)

    """ Confidence thresholds for the knob settings,
    used for recognition of built-in words or custom grammars
    (not used for the mixed trigger group) """
    LOOSER      = 0 #: Lowest threshold, most results reported
    LOOSE       = 1 #: Lower threshold, more results reported
    TYPICAL     = 2 #: Typical threshold (default)
    STRICT      = 3 #: Higher threshold, fewer results reported
    STRICTER    = 4 #: Highest threshold, fewest results reported

    """ Strictness values for the level settings,
    used for recognition of custom commands
    (not used for the mixed trigger group) """
    EASY    = 1 #: Lowest value, most results reported
    NORMAL  = 2 #: Typical value (default)
    HARD    = 3 #: Slightly higher value, fewer results reported
    HARDER  = 4 #: Higher value, fewer results reported
    HARDEST = 5 #: Highest value, fewest results reported

    """ Trailing silence settings used for recognition of built-in words or
    custom grammars (including the mixed trigger group), in a range from
    100ms to 875ms in steps of 25ms. """
    TRAILING_MIN    = 0     #: Lowest value (100ms), minimum latency
    TRAILING_DEF    = 12    #: Default value (400ms) after power on or reset
    TRAILING_MAX    = 31    #: Highest value (875ms), maximum latency
    TRAILING_100MS  = 0     #: Silence duration is 100ms
    TRAILING_200MS  = 4     #: Silence duration is 200ms
    TRAILING_300MS  = 8     #: Silence duration is 300ms
    TRAILING_400MS  = 12    #: Silence duration is 400ms
    TRAILING_500MS  = 16    #: Silence duration is 500ms
    TRAILING_600MS  = 20    #: Silence duration is 600ms
    TRAILING_700MS  = 24    #: Silence duration is 700ms
    TRAILING_800MS  = 28    #: Silence duration is 800ms

    """ Latency settings used for recognition of custom commands or passwords
    (excluding the mixed trigger group) """
    MODE_NORMAL = 0 #: Normal settings (default), higher latency
    MODE_FAST   = 1 #: Fast settings, better response time

    """ Constants to use for baudrate settings """
    B115200 = 1     #: 115200 bps
    B57600  = 2     #: 57600 bps
    B38400  = 3     #: 38400 bps
    B19200  = 6     #: 19200 bps
    B9600   = 12    #: 9600 bps (default)

    """ Constants for choosing wake-up method in sleep mode """
    WAKE_ON_CHAR        = 0 #: Wake up on any character received
    WAKE_ON_WHISTLE     = 1 #: Wake up on whistle or any character received
    WAKE_ON_LOUDSOUND   = 2 #: Wake up on a loud sound or any character received
    WAKE_ON_2CLAPS      = 3 #: Wake up on double hands-clap or any character received
    WAKE_ON_3CLAPS      = 6 #: Wake up on triple hands-clap or any character received

    """ Hands-clap sensitivity for wakeup from sleep mode.
    Use in combination with ``WAKE_ON_2CLAPS`` or ``WAKE_ON_3CLAPS`` """
    CLAP_SENSE_LOW  = 0 #: Lowest threshold
    CLAP_SENSE_MID  = 1 #: Typical threshold
    CLAP_SENSE_HIGH = 2 #: Highest threshold

    """ Pin configuration options for the extra I/O connector """
    OUTPUT_LOW      = 0 #: Pin is an output at low level (0V)
    OUTPUT_HIGH     = 1 #: Pin is an output at high level (3V)
    INPUT_HIZ       = 2 #: Pin is an high impedance input
    INPUT_STRONG    = 3 #: Pin is an input with strong pull-up (~10K)
    INPUT_WEAK      = 4 #: Pin is an input with weak pull-up (~200K)

    """ Available pin numbers on the extra I/O connector """
    IO1 = 1 #: Identifier of pin IO1
    IO2 = 2 #: Identifier of pin IO2
    IO3 = 3 #: Identifier of pin IO3
    IO4 = 4 #: Identifier of pin IO4 [only EasyVR3]
    IO5 = 5 #: Identifier of pin IO5 [only EasyVR3]
    IO6 = 6 #: Identifier of pin IO6 [only EasyVR3]

    """ Some quick volume settings for the sound playback functions
    (any value in the range 0-31 can be used) """
    VOL_MIN     = 0     #: Lowest volume (almost mute)
    VOL_HALF    = 7     #: Half scale volume (softer)
    VOL_FULL    = 15    #: Full scale volume (normal)
    VOL_DOUBLE  = 31    #: Double gain volume (louder)

    """ Special sound index values, always available even when no soundtable is present """
    BEEP    = 0 #: Beep sound

    """ Flags used by custom grammars """
    GF_TRIGGER  = 0x10  #: A bit mask that indicate grammar is a trigger (opposed to commands)

    """ Noise rejection level for SonicNet token detection (higher value, fewer results) """
    REJECTION_MIN   = 0 #: Lowest noise rejection, highest sensitivity
    REJECTION_AVG   = 1 #: Medium noise rejection, medium sensitivity
    REJECTION_MAX   = 2 #: Highest noise rejection, lowest sensitivity

    """ Playback speed for recorded messages """
    SPEED_NORMAL    = 0 #: Normal playback speed
    SPEED_FASTER    = 1 #: Faster playback speed

    """ Playback attenuation for recorded messages """
    ATTEN_NONE  = 0 #: No attenuation (normalized volume)
    ATTEN_2DB2  = 1 #: Attenuation of -2.2dB
    ATTEN_4DB5  = 2 #: Attenuation of -4.5dB
    ATTEN_6DB7  = 3 #: Attenuation of -6.7dB

    """ Type of recorded message """
    MSG_EMPTY   = 0 #: Empty message slot
    MSG_8BIT    = 8 #: Message recorded with 8-bits PCM

    """ Threshold for real-time lip-sync """
    RTLS_THRESHOLD_DEF  = 270   #: Default threshold
    RTLS_THRESHOLD_MAX  = 1023  #: Maximum threshold

    """ Error codes used by various functions """
    ## 0x: Data collection errors (patgen, wordspot, t2si)
    ERR_DATACOL_TOO_LONG        = 0x02  #: too long (memory overflow)
    ERR_DATACOL_TOO_NOISY       = 0x03  #: too noisy
    ERR_DATACOL_TOO_SOFT        = 0x04  #: spoke too soft
    ERR_DATACOL_TOO_LOUD        = 0x05  #: spoke too loud
    ERR_DATACOL_TOO_SOON        = 0x06  #: spoke too soon
    ERR_DATACOL_TOO_CHOPPY      = 0x07  #: too many segments/too complex
    ERR_DATACOL_BAD_WEIGHTS     = 0x08  #: invalid SI weights
    ERR_DATACOL_BAD_SETUP       = 0x09  #: invalid setup

    ## 1x: Recognition errors (si, sd, sv, train, t2si)
    ERR_RECOG_FAIL              = 0x11  #: recognition failed
    ERR_RECOG_LOW_CONF          = 0x12  #: recognition result doubtful
    ERR_RECOG_MID_CONF          = 0x13  #: recognition result maybe
    ERR_RECOG_BAD_TEMPLATE      = 0x14  #: invalid SD/SV template
    ERR_RECOG_BAD_WEIGHTS       = 0x15  #: invalid SI weights
    ERR_RECOG_DURATION          = 0x17  #: incompatible pattern durations

    ## 2x: T2si errors (t2si)
    ERR_T2SI_EXCESS_STATES      = 0x21  #: state structure is too big
    ERR_T2SI_BAD_VERSION        = 0x22  #: RSC code version/Grammar ROM dont match
    ERR_T2SI_OUT_OF_RAM         = 0x23  #: reached limit of available RAM
    ERR_T2SI_UNEXPECTED         = 0x24  #: an unexpected error occurred
    ERR_T2SI_OVERFLOW           = 0x25  #: ran out of time to process
    ERR_T2SI_PARAMETER          = 0x26  #: bad macro or grammar parameter

    ERR_T2SI_NN_TOO_BIG         = 0x29  #: layer size out of limits
    ERR_T2SI_NN_BAD_VERSION     = 0x2A  #: net structure incompatibility
    ERR_T2SI_NN_NOT_READY       = 0x2B  #: initialization not complete
    ERR_T2SI_NN_BAD_LAYERS      = 0x2C  #: not correct number of layers

    ERR_T2SI_TRIG_OOV           = 0x2D  #: trigger recognized Out Of Vocabulary
    ERR_T2SI_TOO_SHORT          = 0x2F  #: utterance was too short

    ## 3x: Record and Play errors (standard RP and messaging)
    ERR_RP_BAD_LEVEL            = 0x31  #:  play - illegal compression level
    ERR_RP_NO_MSG               = 0x38  #:  play, erase, copy - msg doesn't exist
    ERR_RP_MSG_EXISTS           = 0x39  #:  rec, copy - msg already exists

    ## 4x: Synthesis errors (talk, sxtalk)
    ERR_SYNTH_BAD_VERSION       = 0x4A  #: bad release number in speech file
    ERR_SYNTH_ID_NOT_SET        = 0x4B  #: (obsolete) bad sentence structure
    ERR_SYNTH_TOO_MANY_TABLES   = 0x4C  #: (obsolete) too many talk tables
    ERR_SYNTH_BAD_SEN           = 0x4D  #: (obsolete) bad sentence number
    ERR_SYNTH_BAD_MSG           = 0x4E  #: bad message data or SX technology files missing

    ## 8x: Custom errors
    ERR_CUSTOM_NOTA             = 0x80  #: none of the above (out of grammar)
    ERR_CUSTOM_INVALID          = 0x81  #: invalid data (for memory check)

    ## Cx: Internal errors (all)
    ERR_SW_STACK_OVERFLOW       = 0xC0  #: no room left in software stack
    ERR_INTERNAL_T2SI_BAD_SETUP = 0xCC  #: T2SI test mode error

    """ Type of Bridge mode requested """
    BRIDGE_NONE         = 0 #: Bridge mode has not been requested
    BRIDGE_NORMAL       = 1 #: Normal bridge mode (EasyVR baudrate 9600)
    BRIDGE_BOOT         = 2 #: Bridge mode for EasyVR bootloader (baudrate 115200)

    BRIDGE_ESCAPE_CHAR  = b'?'   #: Special character to enter/exit Bridge mode


    # internal functions

    def _flush(self):
        while True:
            a = _available(self._s)
            if a > 0:
                self._s.read(a)
            else:
                break

    def _send(self, c):
        _delay(1)
        self._s.write(c)

    def _sendCmd(self, c):
        self._flush()
        self._send(c)

    def _sendArg(self, i):
        self._send(bytes([i + _ARG_ZERO]))

    def _sendGroup(self, i):
        self._send(bytes([i + _ARG_ZERO]))
        if i != self._group:
            self._group = i
            # worst case time to cache a full group in memory
            if self._id >= EasyVR.EASYVR3PLUS:
                _delay(79)
            elif self._id >= EasyVR.EASYVR3:
                _delay(39)
            else:
                _delay(19)

    def _recv(self, timeout = _INFINITE):
        while timeout != 0 and _available(self._s) <= 0:
            _delay(1)
            if timeout > 0:
                timeout -= 1

        if _available(self._s) > 0:
            r = self._s.read()
            #print(r)
            return r
        raise TimeoutError

    def _recvArg(self):
        self._send(_ARG_ACK)
        r = self._recv(EasyVR.DEF_TIMEOUT)[0]
        if r < _ARG_MIN and r > _ARG_MAX:
            raise ValueError
        c = r - _ARG_ZERO
        return c

    def _readStatus(self,rx):
        self._status = 0
        self._value = 0

        if rx == _STS_SUCCESS:
            return

        if rx == _STS_SIMILAR:
            self._status |= EasyVR._is_builtin
            self._value = self._recvArg()
            return

        if rx == _STS_RESULT:
            self._status |= EasyVR._is_command
            self._value = self._recvArg()
            return

        if rx == _STS_TOKEN:
            self._status |= EasyVR._is_token
            self._value = self._recvArg() << 5
            self._value |= self._recvArg()
            return

        if rx == _STS_AWAKEN:
            self._status |= EasyVR._is_awakened
            return

        if rx == _STS_TIMEOUT:
            self._status |= EasyVR._is_timeout
            return

        if rx == _STS_INVALID:
            self._status |= EasyVR._is_invalid
            return

        if rx == _STS_ERROR:
            self._status |= EasyVR._is_error
            self._value = self._recvArg() << 4
            self._value |= self._recvArg()
            return

        # unexpected condition (communication error)
        self._status |= EasyVR._is_error
        raise ValueError


    def __init__(self,stream):
        """
.. method:: __init__(stream)

        Creates an EasyVR object, using a communication object implementing the
        *Stream* interface (such as *Serial*).

        :param stream: the *Stream* object to use for communication with the EasyVR module
        """

        self._s = stream
        self._value = -1
        self._group = -1
        self._id = -1
        self._status = 0


    def detect(self):
        """
.. method:: detect()

        Detects an EasyVR module, waking it from sleep mode and checking
        it responds correctly.

        :return: *True* if a compatible module has been found
        """
        for i in range(5):
            try:
                self._sendCmd(_CMD_BREAK)
                if self._recv(EasyVR.WAKE_TIMEOUT) == _STS_SUCCESS:
                    return True
            except TimeoutError:
                pass
        return False


    def stop(self):
        """
.. method:: stop()

        Interrupts pending recognition or playback operations.
        """
        self._sendCmd(_CMD_BREAK)

        rx = self._recv(EasyVR.STORAGE_TIMEOUT)
        if rx == _STS_INTERR or rx == _STS_SUCCESS:
            return
        raise ValueError


    def getID(self):
        """
.. method:: getID()

        Gets the module identification number (firmware version).

        :return: integer is one of the values in ModuleId_
        """
        self._id = -1
        self._sendCmd(_CMD_ID)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_ID:
            self._id = self._recvArg()
        return self._id

    def gotoSleep(self, mode):
        """
.. method:: gotoSleep(mode)

        Puts the module in sleep mode.

        :param mode: is one of values in WakeMode_, optionally combined with one of \
        the values in ClapSense_
        """
        self._sendCmd(_CMD_SLEEP);
        self._sendArg(mode);

        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def hasFinished(self):
        """
.. method:: hasFinished()

        Polls the status of on-going recognition, training or asynchronous \
        playback tasks.

        :return: *True* if the operation has completed
        """
        try:
            rx = self._recv(EasyVR._NO_TIMEOUT)
        except TimeoutError:
            return False
        self._readStatus(rx)
        return True

    def isAwakened(self):
        """
.. method:: isAwakened()

        Retrieves the wake-up indicator (only valid after :meth:`hasFinished()` has been \
        called).
        
        :return: *True* if the module has been awakened from sleep mode
        """
        return (self._status & EasyVR._is_awakened) != 0

    def getCommand(self):
        """
.. method:: getCommand()

        Gets the recognised command index if any.
        
        :return: (0-31) is the command index if recognition is successful, (-1) if no \
        command has been recognized or an error occurred
        """
        if (self._status & EasyVR._is_command) != 0:
            return self._value
        return -1

    def getWord(self):
        """
.. method:: getWord()

        Gets the recognised word index if any, from built-in sets or custom grammars.
        
        :return: (0-31) is the command index if recognition is successful, (-1) if no \
        built-in word has been recognized or an error occurred
        """
        if (self._status & EasyVR._is_builtin) != 0:
            return self._value
        return -1

    def getToken(self):
        """
.. method:: getToken()

        Gets the index of the received SonicNet token if any.
        
        :return: an integer with the index of the received SonicNet token (0-255 for 8-bit \
        tokens or 0-15 for 4-bit tokens) if detection was successful, (-1) if no \
        token has been received or an error occurred
        """
        if (self._status & EasyVR._is_token) != 0:
            return self._value
        return -1

    def getError(self):
        """
.. method:: getError()

        Gets the last error code if any.
        
        :return: (0-255) is the error code, (-1) if no error occurred
        """
        if (self._status & EasyVR._is_error) != 0:
            return self._value
        return -1

    def isTimeout(self):
        """
.. method:: isTimeout()

        Retrieves the timeout indicator.
        
        :return: *True* if the last operation timed out
        """
        return (self._status & EasyVR._is_timeout) != 0

    def isConflict(self):
        """
.. method:: isConflict()

        Retrieves the conflict indicator.
        
        :return: true is a conflict occurred during training. To know what \
        caused the conflict, use :meth:`getCommand()` and :meth:`getWord()` \
        (only valid for triggers)
        """
        return (self._status & EasyVR._is_conflict) != 0

    def isMemoryFull(self):
        """
.. method:: isMemoryFull()

        Retrieves the memory full indicator (only valid after :meth:`addCommand()` \
        returned false).
        
        :return: *True* if a command could not be added because of memory size \
        constraints (up to 32 custom commands can be created)
        """
        return (self._status & EasyVR._is_memfull) != 0

    def isInvalid(self):
        """
.. method:: isInvalid()

        Retrieves the invalid protocol indicator.
        
        :return: *True* if an invalid sequence has been detected in the communication \
        protocol
        """
        return (self._status & EasyVR._is_invalid) != 0

    def setLanguage(self, lang):
        """
.. method:: setLanguage(lang)

        Sets the language to use for recognition of built-in words.
        
        :param lang: (0-5) is one of values in Language_
        """
        self._sendCmd(_CMD_LANGUAGE)
        self._sendArg(lang)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def setTimeout(self, seconds):
        """
.. method:: setTimeout(seconds)

        Sets the timeout to use for any recognition task.
        
        :param seconds: (0-31) is the maximum time the module keep listening \
        for a word or a command
        """
        self._sendCmd(_CMD_TIMEOUT)
        self._sendArg(seconds)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def setMicDistance(self, dist):
        """
.. method:: setMicDistance(dist)

        Sets the operating distance of the microphone.
        
        This setting represents the distance between the microphone and the \
        user's mouth, in one of three possible configurations.
        
        :param dist: (1-3) is one of values in Distance_
        """
        self._sendCmd(_CMD_MIC_DIST)
        self._sendArg(-1)
        self._sendArg(dist)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def setKnob(self, knob):
        """
.. method:: setKnob(knob)

        Sets the confidence threshold to use for recognition of built-in words or custom grammars.
        
        :param knob: (0-4) is one of values in Knob_
        """
        self._sendCmd(_CMD_KNOB)
        self._sendArg(knob)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def setTrailingSilence(self,dur):
        """
.. method:: setTrailingSilence(dur)

        Sets the trailing silence duration for recognition of built-in words or custom grammars.
        
        :param dur: (0-31) is the silence duration as defined in TrailingSilence_
        """
        self._sendCmd(_CMD_TRAILING)
        self._sendArg(-1)
        self._sendArg(dur)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def setLevel(self,level):
        """
.. method:: setLevel(level)

        Sets the strictness level to use for recognition of custom commands.
        
        :param level: (1-5) is one of values in Level_
        """
        self._sendCmd(_CMD_LEVEL)
        self._sendArg(level)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def setCommandLatency(self,mode):
        """
.. method:: setCommandLatency(mode)

        Enables or disables fast recognition for custom commands and passwords.
        
        Fast SD/SV recognition can improve response time.
        
        :param mode: (0-1) is one of the values in CommandLatency_
        """
        self._sendCmd(_CMD_FAST_SD)
        self._sendArg(-1)
        self._sendArg(mode)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def setDelay(self,millis):
        """
.. method:: setDelay()

        Sets the delay before any reply of the module.
        
        :param millis: (0-1000) is the delay duration in milliseconds, rounded to \
        10 units in range 10-100 and to 100 units in range 100-1000.
        """
        self._sendCmd(_CMD_DELAY)
        if millis <= 10:
            self._sendArg(millis)
        elif millis <= 100:
            self._sendArg(int(millis / 10 + 9))
        elif millis <= 1000:
            self._sendArg(int(millis / 100 + 18))
        else:
            raise ValueError
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def changeBaudrate(self, baud):
        """
.. method:: changeBaudrate(baud)

        Sets the new communication speed. You need to modify the baudrate of the \
        underlying Stream object accordingly, after the function returns successfully.
        
        :param baud: is one of values in Baudrate_
        """
        self._sendCmd(_CMD_BAUDRATE)
        self._sendArg(baud)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def addCommand(self, group, index):
        """
.. method:: addCommand(group, index)

        Adds a new custom command to a group.
        
        :param group: (0-16) is the target group, or one of the values in Group_
        :param index: (0-31) is the index of the command within the selected group
        """
        self._sendCmd(_CMD_GROUP_SD)
        self._sendGroup(group)
        self._sendArg(index)
        rx = self._recv(EasyVR.STORAGE_TIMEOUT)
        if rx == _STS_SUCCESS:
            return
        self._status = 0
        if rx == _STS_OUT_OF_MEM:
            self._status |= EasyVR._is_memfull
        raise ValueError

    def removeCommand(self, group, index):
        """
.. method:: removeCommand(group, index)

        Removes a custom command from a group.
        
        :param group: (0-16) is the target group, or one of the values in Group_
        :param index: (0-31) is the index of the command within the selected group
        """
        self._sendCmd(_CMD_UNGROUP_SD)
        self._sendGroup(group)
        self._sendArg(index)
        if self._recv(EasyVR.STORAGE_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def setCommandLabel(self, group, index, name):
        """
.. method:: setCommandLabel(group, index, name)

        Sets the name of a custom command.
        
        :param group: (0-16) is the target group, or one of the values in Group_
        :param index: (0-31) is the index of the command within the selected group
        :param name: is a string containing the label to be assigned to the \
        specified command
        """
        self._sendCmd(_CMD_NAME_SD)
        self._sendGroup(group)
        self._sendArg(index)
        name = name.upper() #to uppercase
        length = 0
        name_end = 0
        for c in name:
            name_end += 1
            length += 1
            #if c.isdigit():
            if c >= '0' and c <= '9':
                length += 1
            if length == 31:
                break
        self._sendArg(length)
        for i in range(0,name_end):
            c = name[i]
            #if c.isdigit():
            if c >= '0' and c <= '9':
                self._send(b'^')
                self._sendArg(ord(c) - ord('0'))
            #elif c.isalpha():
            elif c >= 'A' and c <= 'Z':
                self._send(bytes(c))
            else:
                self._send(b'_')
        if self._recv(EasyVR.STORAGE_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def eraseCommand(self, group, index):
        """
.. method:: eraseCommand(group, index)

        Erases the training data of a custom command.
        
        :param group: (0-16) is the target group, or one of the values in Group_
        :param index: (0-31) is the index of the command within the selected group
        """
        self._sendCmd(_CMD_ERASE_SD)
        self._sendGroup(group)
        self._sendArg(index)
        if self._recv(EasyVR.STORAGE_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def getGroupMask(self):
        """
.. method:: getGroupMask()

        Gets a bit mask of groups that contain at least one command.
        
        :return mask: the group mask when the function returns normally
        """
        self._sendCmd(_CMD_MASK_SD)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_MASK:
            mask = 0
            for i in range(0,4):
                rx = self._recvArg()
                mask |= (rx & 0x0F) << (i * 8)
                rx = self._recvArg()
                mask |= ((rx << 4) & 0xF0) << (i * 8)
            return mask
        raise ValueError

    def getCommandCount(self, group):
        """
.. method:: getCommandCount(group)

        Gets the number of commands in the specified group.
        
        :param group: (0-16) is the target group, or one of the values in Group_
        
        :return: integer is the count of commands (negative in case of errors)
        """
        self._sendCmd(_CMD_COUNT_SD)
        self._sendArg(group)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_COUNT:
            rx = self._recvArg()
            if rx == -1:
                return 32
            return rx
        return -1

    def dumpCommand(self, group, index):
        """
.. method:: dumpCommand(group, index)

        Retrieves the name and training data of a custom command.
        
        :param group: (0-16) is the target group, or one of the values in Group_
        :param index: (0-31) is the index of the command within the selected group
        
        :return: a tuple of the form (**name**, **training**)
        
        **name**
            is a string that holds the command label (max length 32)
        
        **training**
            is an integer that holds the training count
        
        Additional information about training is available \
        through the functions :meth:`isConflict()` and :meth:`getWord()` or :meth:`getCommand()`
        """
        self._sendCmd(_CMD_DUMP_SD)
        self._sendGroup(group)
        self._sendArg(index)
        if self._recv(EasyVR.DEF_TIMEOUT) != _STS_DATA:
            raise ValueError
        rx = self._recvArg()
        training = rx & 0x07
        if rx == -1 or training == 7:
            training = 0
        self._status = 0
        if (rx & 0x18) != 0:
            self._status |= EasyVR._is_conflict
            self._status |= EasyVR._is_command
            self._status |= EasyVR._is_builtin
        rx = self._recvArg()
        _value = rx
        rx = self._recvArg()
        length = 32 if rx == -1 else rx
        name = ''
        i = 0
        while i < length:
            rx = self._recvArg()
            i += 1
            if rx == ord('^') - _ARG_ZERO:
                rx = self._recvArg()
                i += 1
                name += chr(ord('0') + rx)
            else:
                name += chr(_ARG_ZERO + rx)
        return(name,training)

    def getGrammarsCount(self):
        """
.. method:: getGrammarsCount()

        Gets the total number of grammars available, including built-in and custom.
        
        :return: integer is the count of grammars (negative in case of errors)
        """
        self._sendCmd(_CMD_DUMP_SI)
        self._sendArg(-1)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_COUNT:
            rx = self._recvArg()
            if rx == -1:
                return 32
            return rx
        return -1

    def dumpGrammar(self, grammar):
        """
.. method:: dumpGrammar(grammar)

        Retrieves the contents of a built-in or a custom grammar.
        Command labels contained in the grammar can be obtained by calling :meth:`getNextWordLabel()`
        
        :param grammar: (0-31) is the target grammar, or one of the values in Wordset_

        :return: a tuple of the form (**count**, **flags**)
        
        **flags**
            is an integer that contains grammar flags. See GrammarFlag_
            
        **count**
            is an integer that holds the number of words in the grammar
        """
        self._sendCmd(_CMD_DUMP_SI)
        self._sendArg(grammar)
        if self._recv(EasyVR.DEF_TIMEOUT) != _STS_GRAMMAR:
            raise ValueError
        rx = self._recvArg()
        if rx == -1:
            flags = 32
        else:
            flags = rx
        rx = self._recvArg()
        return(rx,flags)

    def getNextWordLabel(self):
        """
.. method:: getNextWordLabel()

        Retrieves the name of a command contained in a custom grammar.
        It must be called after :meth:`dumpGrammar()`
        
        :return: a string that holds the command label (max length 32)
        """
        count = self._recvArg()
        if count == -1:
            count = 32
        name = ''
        i = 0
        while i < count:
            rx = self._recvArg()
            i += 1
            if rx == ord('^') - _ARG_ZERO:
                rx = self._recvArg()
                i += 1
                name += chr(ord('0') + rx)
            else:
                name += chr(_ARG_ZERO + rx)
        return name

    def trainCommand(self, group, index):
        """
.. method:: trainCommand(group, index)

        Starts training of a custom command. Results are available after
        :meth:`hasFinished()` returns true.
        
        :param group: (0-16) is the target group, or one of the values in Group_
        :param index: (0-31) is the index of the command within the selected group
        
        :note: The module is busy until training completes and it cannot \
        accept other commands. You can interrupt training with :meth:`stop()`.
        """
        self._sendCmd(_CMD_TRAIN_SD)
        self._sendGroup(group)
        self._sendArg(index)

    def recognizeCommand(self, group):
        """
.. method:: recognizeCommand(group)

        Starts recognition of a custom command. Results are available after
        :meth:`hasFinished()` returns true.
        
        :param group: (0-16) is the target group, or one of the values in Group_
        
        :note: The module is busy until recognition completes and it cannot \
        accept other commands. You can interrupt recognition with :meth:`stop()`.
        """
        self._sendCmd(_CMD_RECOG_SD)
        self._sendArg(group)

    def recognizeWord(self, wordset):
        """
.. method:: recognizeWord(wordset)

        Starts recognition of a built-in word. Results are available after
        :meth:`hasFinished()` returns true.
        
        :param wordset: (0-3) is the target word set, or one of the values in\
        :meth:`Wordset, (4-31)` is the target custom grammar, if present
        
        :note: The module is busy until recognition completes and it cannot \
        accept other commands. You can interrupt recognition with :meth:`stop()`.
          """
        self._sendCmd(_CMD_RECOG_SI)
        self._sendArg(wordset)

    def setPinOutput(self, pin, config):
        """
.. method:: setPinOutput(pin, config)

        Configures an I/O pin as an output and sets its value
        
        :param pin: (1-3) is one of the values in PinNumber_
        :param config: (0-1,5-6) is one of the output values in PinConfig_ \
        (`OUTPUT_LOW`, `OUTPUT_HIGH`) or Arduino style HIGH and LOW macros
        """
        self._sendCmd(_CMD_QUERY_IO)
        self._sendArg(pin)
        self._sendArg(config)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def getPinInput(self, pin, config):
        """
.. method:: getPinInput(pin, config)

        Configures an I/O pin as an input with optional pull-up and
        return its value
        
        :param pin: (1-3) is one of the values in PinNumber_
        :param config: (2-4) is one of the input values in PinConfig_ (`INPUT_HIZ`, \
        `INPUT_STRONG`, `INPUT_WEAK)`
        
        :return: integer is the logical value of the pin
        """
        self._sendCmd(_CMD_QUERY_IO)
        self._sendArg(pin)
        self._sendArg(config)
        if self._recv(EasyVR.DEF_TIMEOUT) == _STS_PIN:
            return self._recvArg()
        return -1

    def playPhoneTone(self, tone, duration):
        """
.. method:: playPhoneTone(tone, duration)

        Plays a phone tone and waits for completion
        
        :param tone: is the index of the tone (0-9 for digits, 10 for '*' key, 11 \
        for '#' key and 12-15 for extra keys 'A' to 'D', -1 for the dial tone)
        :param duration: (1-32) is the tone duration in 40 milliseconds units, or \
        in seconds for the dial tone
        """
        self._sendCmd(_CMD_PLAY_DTMF)
        self._sendArg(-1)  #distinguish DTMF from SX
        self._sendArg(tone)
        self._sendArg(duration - 1)
        if tone < 0:
            duration = duration * 1000
        else:
            duration = duration * 40
        if self._recv(duration + EasyVR.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def playSound(self, index, volume):
        """
.. method:: playSound(index, volume)

        Plays a sound from the sound table and waits for completion
        
        :param index: is the index of the target sound in the sound table
        :param volume: (0-31) may be one of the values in SoundVolume_
        
        :note: To alter the maximum time for the wait, define the \
        EASYVR_PLAY_TIMEOUT macro before including the EasyVR library.
        """
        self._sendCmd(_CMD_PLAY_SX)
        self._sendArg((index >> 5) & 0x1F)
        self._sendArg(index & 0x1F)
        self._sendArg(volume)
        if self._recv(EasyVR.PLAY_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def playSoundAsync(self, index, volume):
        """
.. method:: playSoundAsync(index, volume)

        Starts playback of a sound from the sound table. Manually check for
        completion with :meth:`hasFinished()`.
        
        :param index: is the index of the target sound in the sound table
        :param volume: (0-31) may be one of the values in SoundVolume_
        
        :note: The module is busy until playback completes and it cannot \
        accept other commands. You can interrupt playback with :meth:`stop()`.
        """
        self._sendCmd(_CMD_PLAY_SX)
        self._sendArg((index >> 5) & 0x1F)
        self._sendArg(index & 0x1F)
        self._sendArg(volume)

    def detectToken(self, bits, rejection, timeout):
        """
.. method:: detectToken(bits, rejection, timeout)

        Starts listening for a SonicNet token. Manually check for
        completion with :meth:`hasFinished()`.
        
        :param bits: (4 or 8) specifies the length of received tokens
        :param rejection: (0-2) specifies the noise rejection level, \
        it can be one of the values in RejectionLevel_
        :param timeout: (1-28090) is the maximum time in milliseconds to keep \
        listening for a valid token or (0) to listen without time limits.
        
        :note: The module is busy until token detection completes and it cannot \
        accept other commands. You can interrupt listening with :meth:`stop()`.
        """
        self._sendCmd(_CMD_RECV_SN)
        self._sendArg(bits)
        self._sendArg(rejection)
        if timeout > 0:
            timeout = int((timeout * 2 + 53)/ 55) # approx / 27.46 - err < 0.15%
        self._sendArg((timeout >> 5) & 0x1F)
        self._sendArg(timeout & 0x1F)

    def sendToken(self, bits, token):
        """
.. method:: sendToken(bits, token)

        Starts immediate playback of a SonicNet token. Manually check for
        completion with :meth:`hasFinished()`.
        
        :param bits: (4 or 8) specifies the length of trasmitted token
        :param token: is the index of the SonicNet token to play (0-255 for 8-bit \
        tokens or 0-15 for 4-bit tokens)
        
        :note: The module is busy until playback completes and it cannot \
        accept other commands. You can interrupt playback with :meth:`stop()`.
        """
        self._sendCmd(_CMD_SEND_SN)
        self._sendArg(bits)
        self._sendArg((token >> 5) & 0x1F)
        self._sendArg(token & 0x1F)
        self._sendArg(0)
        self._sendArg(0)
        if self._recv(EasyVR.TOKEN_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def sendTokenAsync(self, bits, token):
        """
.. method:: sendTokenAsync(bits, token)

        Plays a SonicNet token and waits for completion.
        
        :param bits: (4 or 8) specifies the length of trasmitted token
        :param token: is the index of the SonicNet token to play (0-255 for 8-bit \
        tokens or 0-15 for 4-bit tokens)
        """
        self._sendCmd(_CMD_SEND_SN)
        self._sendArg(bits)
        self._sendArg((token >> 5) & 0x1F)
        self._sendArg(token & 0x1F)
        self._sendArg(0)
        self._sendArg(0)

    def embedToken(self, bits, token, delay):
        """
.. method:: embedToken(bits, token, delay)

        Schedules playback of a SonicNet token after the next sound starts playing.
        
        :param bits: (4 or 8) specifies the length of trasmitted token
        :param token: is the index of the SonicNet token to play (0-255 for 8-bit \
        tokens or 0-15 for 4-bit tokens)
        :param delay: (1-28090) is the time in milliseconds at which to send the token, \
        since the beginning of the next sound playback
        
        :note: The scheduled token remains valid for one operation only, so you have \
        to call :meth:`playSound()` or :meth:`playSoundAsync()` immediately after this function.
        """
        self._sendCmd(_CMD_SEND_SN)
        self._sendArg(bits)
        self._sendArg((token >> 5) & 0x1F)
        self._sendArg(token & 0x1F)
        delay = int((delay * 2 + 27) / 55) # approx / 27.46 - err < 0.15%
        if delay == 0: # must be > 0 to embed in some audio
            delay = 1
        self._sendArg((delay >> 5) & 0x1F)
        self._sendArg(delay & 0x1F)
        if self._recv(self.DEF_TIMEOUT) == _STS_SUCCESS:
            return
        raise ValueError

    def dumpSoundTable(self):
        """
.. method:: dumpSoundTable()

        Retrieves the name of the sound table and the number of sounds it contains
        
        :param name: points to an array of at least 32 characters that holds the \
        sound table label when the function returns
        :param count: is a variable that holds the number of sounds when the \
        function returns
        """
        self._sendCmd(_CMD_DUMP_SX)
        if self._recv(EasyVR.DEF_TIMEOUT) != _STS_TABLE_SX:
            raise ValueError
        rx = self._recvArg()
        count = rx << 5
        rx = self._recvArg()
        count |= rx
        rx = self._recvArg()
        len = rx
        name = ''
        for i in range(len):
            rx = self._recvArg()
            if rx == ord('^') - _ARG_ZERO:
                rx = self._recvArg()
                i += 1
                name += chr(ord('0') + rx)
            else:
                name += chr(_ARG_ZERO + rx)
        return(name,count)

    def resetAll(self, wait):
        """
.. method:: resetAll(wait)

        Empties internal memory for custom commands/groups and messages.
        
        :param wait: specifies whether to wait until the operation is complete (or times out)
        
        :note: It will take some time for the whole process to complete (EasyVR3 is faster) \
        and it cannot be interrupted. During this time the module cannot \
        accept any other command. The sound table and custom grammars data is not affected.
        """
        timeout = 40 # seconds
        if self.getID() >= EasyVR.EASYVR3:
            timeout = 5
        self._sendCmd(_CMD_RESETALL)
        self._sendArg(ord('R') - _ARG_ZERO)
        if not wait:
            return
        while timeout != 0 and _available(self._s) == 0:
            _delay(1000)
            --timeout
        if self._s.read() == _STS_SUCCESS:
            return
        raise ValueError

    def resetCommands(self, wait):
        """
.. method:: resetCommands(wait)

        Empties internal memory for custom commands/groups only. Messages are not affected.
        
        :param wait: specifies whether to wait until the operation is complete (or times out)
        
        :note: It will take some time for the whole process to complete (EasyVR3 is faster) \
        and it cannot be interrupted. During this time the module cannot \
        accept any other command. The sound table and custom grammars data is not affected.
        """
        if self.getID() >= EasyVR.EASYVR3_1:
            return self.resetAll(wait) # map to reset all for older firmwares
        self._sendCmd(_CMD_RESET_SD)
        self._sendArg(ord('D') - _ARG_ZERO)
        if not wait:
            return
        timeout = 5 # seconds
        while timeout != 0 and _available(self._s) == 0:
            _delay(1000)
            --timeout
        if self._s.read() == _STS_SUCCESS:
            return
        raise ValueError

    def resetMessages(self, wait):
        """
.. method:: resetMessages(wait)

        Empties internal memory used for messages only. Commands/groups are not affected.
        
        :param wait: specifies whether to wait until the operation is complete (or times out)
        
        :note: It will take some time for the whole process to complete (EasyVR3 is faster) \
        and it cannot be interrupted. During this time the module cannot \
        accept any other command. The sound table and custom grammars data is not affected.
        """
        self._sendCmd(_CMD_RESET_RP)
        self._sendArg(ord('M') - _ARG_ZERO)
        if not wait:
            return
        timeout = 15 # seconds
        while timeout != 0 and _available(self._s) == 0:
            _delay(1000)
        --timeout
        if self._s.read() == _STS_SUCCESS:
            return
        raise ValueError

    def checkMessages(self):
        """
.. method:: checkMessages()

        Performs a memory check for consistency.
        
        :return: *True* if no errors detected
        
        :note: If a memory write or erase operation does not complete due to unexpected \
        conditions, like power losses, the memory contents may be corrupted. When the \
        check fails :meth:`getError()` returns ``ERR_CUSTOM_INVALID``.
        """  
        self._sendCmd(_CMD_VERIFY_RP)
        self._sendArg(-1)
        self._sendArg(0)
        rx = self._recv(EasyVR.STORAGE_TIMEOUT)
        self._readStatus(rx)
        return self._status == 0

    def fixMessages(self, wait):
        """
.. method:: fixMessages(wait)

        Starts recording a message. Manually check for completion with :meth:`hasFinished()`.
        
        :param index: (0-31) is the index of the target message slot
        :param bits: \(8\) specifies the audio format (see MessageType_)
        :param timeout: (0-31) is the maximum recording time (0=infinite)
        
        :note: The module is busy until recording times out or the end of memory is \
        reached. You can interrupt an ongoing recording with :meth:`stop()`.
        """
        self._sendCmd(_CMD_VERIFY_RP)
        self._sendArg(-1)
        self._sendArg(1)
        if not wait:
            return
        timeout = 25 # seconds
        while timeout != 0 and _available(self._s) == 0:
            _delay(1000)
            --timeout
        if self._s.read() == _STS_SUCCESS:
            return
        raise ValueError

    def recordMessageAsync(self, index, bits, timeout):
        """
.. method:: recordMessageAsync(index, bits, timeout)

        Starts recording a message. Manually check for completion with :meth:`hasFinished()`.
        
        :param index: (0-31) is the index of the target message slot
        :param bits: \(8\) specifies the audio format (see MessageType_)
        :param timeout: (0-31) is the maximum recording time (0=infinite)
        
        :note: The module is busy until recording times out or the end of memory is \
        reached. You can interrupt an ongoing recording with :meth:`stop()`.
        """
        self._sendCmd(_CMD_RECORD_RP)
        self._sendArg(-1)
        self._sendArg(index)
        self._sendArg(bits)
        self._sendArg(timeout)

    def playMessageAsync(self, index, speed, atten):
        """
.. method:: playMessageAsync(index, speed, atten)

        Starts playback of a recorded message. Manually check for completion with :meth:`hasFinished()`.
        
        :param index: (0-31) is the index of the target message slot
        :param speed: (0-1) may be one of the values in MessageSpeed_
        :param atten: (0-3) may be one of the values in MessageAttenuation_
        
        :note: The module is busy until playback completes and it cannot \
        accept other commands. You can interrupt playback with :meth:`stop()`.
        """
        self._sendCmd(_CMD_PLAY_RP)
        self._sendArg(-1)
        self._sendArg(index)
        self._sendArg((speed << 2) | (atten & 3))

    def eraseMessageAsync(self, index):
        """
.. method:: eraseMessageAsync(index)

        Erases a recorded message. Manually check for completion with :meth:`hasFinished()`.
        
        :param index: (0-31) is the index of the target message slot
        """
        self._sendCmd(_CMD_ERASE_RP)
        self._sendArg(-1)
        self._sendArg(index)

    def dumpMessage(self, index):
        """
.. method:: dumpMessage(index)

        Retrieves the type and length of a recorded message
        
        :param index: (0-31) is the index of the target message slot

        :return: a tuple of the form (**type**, **length**)
        
        **type**
            (0,8) is an integer that holds the message format (see `MessageType`)
            
        **length**
            is an integer that holds the message length in bytes

        :note: The specified message may have errors. Use :meth:`getError()` when the \
        function fails, to know the reason of the failure.
        """
        self._sendCmd(_CMD_DUMP_RP)
        self._sendArg(-1)
        self._sendArg(index)        
        sts = self._recv(EasyVR.STORAGE_TIMEOUT)        
        if sts != _STS_MESSAGE:
            self._readStatus(sts)
            raise ValueError
        #if communication should fail
        self._status = 0
        self._status |= EasyVR._is_error
        msgType = self._recvArg()        
        if msgType == 0:
            return # skip reading if empty
        length = 0
        for i in range(3):            
            rx = self._recvArg()            
            length |= (rx & 0x0F) << (i * 8)
            rx = self._recvArg()            
            length |= ((rx << 4) & 0xF0) << (i * 8)            
        self._status = 0
        return (msgType, length)

    def realtimeLipsync(self, threshold, timeout):
        """
.. method:: realtimeLipsync(threshold, timeout)

        Starts real-time lip-sync on the input voice signal.
        Retrieve output values with :meth:`fetchMouthPosition()` or abort with :meth:`stop()`.
        
        :param threshold: (0-1023) is a measure of the strength of the input signal \
        below which the mouth is considered to be closed (see LipsyncThreshold_, \
        adjust based on microphone settings, distance and background noise)
        :param timeout: (0-255) is the maximum duration of the function in seconds, \
        0 means infinite
        """
        self._sendCmd(_CMD_LIPSYNC)
        self._sendArg(-1)
        self._sendArg((threshold >> 5) & 0x1F)
        self._sendArg(threshold & 0x1F)
        self._sendArg((timeout >> 4) & 0x0F)
        self._sendArg(timeout & 0x0F)
        sts = self._recv(EasyVR.DEF_TIMEOUT)
        if sts != _STS_LIPSYNC:
            self._readStatus(sts)
            raise ValueError

    def fetchMouthPosition(self):
        """
.. method:: fetchMouthPosition()

        Retrieves the current mouth opening position during lip-sync.
        
        :return: (0-31) is the current mouth opening position, \
        (-1) if lip-sync has finished
        """
        self._send(_ARG_ACK)
        rx = self._recv(EasyVR.DEF_TIMEOUT)[0]
        if rx >= _ARG_MIN and rx <= _ARG_MAX:
            return rx - _ARG_ZERO            
        # check if finished
        if rx != _STS_SUCCESS:
            self.readStatus(rx)
            raise ValueError
        return -1

    def exportCommand(self, group, index):
        """
.. method:: exportCommand(group, index)

        Retrieves all internal data associated to a custom command.
        
        :param group: (0-16) is the target group, or one of the values in Group_
        :param index: (0-31) is the index of the command within the selected group

        :return: an array of 258 bytes that holds the command raw data
        """
        self._sendCmd(_CMD_SERVICE)
        self._sendArg(ord(_SVC_EXPORT_SD) - _ARG_ZERO)
        self._sendGroup(group)
        self._sendArg(index)
        data = bytearray(258)
        if self._recv(EasyVR.STORAGE_TIMEOUT) != _STS_SERVICE:
            raise ValueError
        rx = self._recvArg()
        if rx != ord(_SVC_DUMP_SD) - _ARG_ZERO:
            raise ValueError
        for i in range(258):
            d = 0
            rx = self._recvArg()
            d = (rx << 4) & 0xF0
            rx = self._recvArg()
            d |= (rx & 0x0F)
            data[i] = d
        return data

    def importCommand(self, group, index, data):
        """
.. method:: importCommand(group, index, data)

        Overwrites all internal data associated to a custom command.
        When commands are imported this way, their training should be tested again
        with :meth:`verifyCommand()`
        
        :param group: (0-16) is the target group, or one of the values in Group_
        :param index: (0-31) is the index of the command within the selected group
        :param data: an array of 258 bytes that holds the command raw data
        """
        self._sendCmd(_CMD_SERVICE)
        self._sendArg(ord(_SVC_IMPORT_SD) - _ARG_ZERO)
        self._sendGroup(group)
        self._sendArg(index)
        for i in range(258):
            tx = (data[i] >> 4) & 0x0F
            self._sendArg(tx)
            tx = data[i] & 0x0F
            self._sendArg(tx)
        if self._recv(EasyVR.STORAGE_TIMEOUT) != _STS_SUCCESS:
            raise ValueError

    def verifyCommand(self, group, index):
        """
.. method:: verifyCommand(group, index)

        Verifies training of a custom command (useful after import).
        Similarly to :meth:`trainCommand()`, you should check results after :meth:`hasFinished()`
        returns true
        
        :param group: (0-16) is the target group, or one of the values in Group_
        :param index: (0-31) is the index of the command within the selected group
        """
        self._sendCmd(_CMD_SERVICE)
        self._sendArg(ord(_SVC_VERIFY_SD) - _ARG_ZERO)
        self._sendGroup(group)
        self._sendArg(index)
