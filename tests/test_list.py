import unittest
from unittest.mock import patch

import cantools.subparsers.list as list_module

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class Args:

    def __init__(self, input_file_name):
        self.exclude_normal = False
        self.exclude_extended = False
        self.print_all = False
        self.no_strict = False
        self.skip_format_specifics = False
        self.prune = True
        self.input_file_name = (input_file_name, )
        self.print_buses = False
        self.print_nodes = False
        self.items = []

class CanToolsListTest(unittest.TestCase):
    def test_dbc(self):
        # Prepare mocks.
        args = Args('tests/files/dbc/motohawk.dbc')

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
ExampleMessage
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        # Prepare mocks.
        args = Args('tests/files/dbc/motohawk.dbc')
        args.print_all = True

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
ExampleMessage:
  Comment[None]: Example message used as template in MotoHawk models.
  Sending ECUs: PCM1
  Frame ID: 0x1f0 (496)
  Size: 8 bytes
  Is extended frame: False
  Is CAN-FD frame: False
  Signal tree:

    -- {root}
       +-- Enable
       +-- AverageRadius
       +-- Temperature

  Signal details:
    Enable:
      Internal type: Integer
      Start bit: 7
      Length: 1 bits
      Byte order: big_endian
      Unit: -
      Is signed: False
      Named values:
        0: Disabled
        1: Enabled
    AverageRadius:
      Internal type: Integer
      Start bit: 6
      Length: 6 bits
      Byte order: big_endian
      Unit: m
      Is signed: False
      Minimum: 0 m
      Maximum: 5 m
      Offset: 0 m
      Scaling factor: 0.1 m
    Temperature:
      Receiving ECUs: FOO, PCM1
      Internal type: Integer
      Start bit: 0
      Length: 12 bits
      Byte order: big_endian
      Unit: degK
      Is signed: True
      Minimum: 229.52 degK
      Maximum: 270.47 degK
      Offset: 250 degK
      Scaling factor: 0.01 degK
"""
            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

    def test_arxml3(self):
        args = Args('tests/files/arxml/system-3.2.3.arxml')
        args.print_buses = True

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
Network:
  Baudrate: 250000
  CAN-FD enabled: False
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        args = Args('tests/files/arxml/system-3.2.3.arxml')
        args.print_nodes = True

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
Driver:
  Comment[DE]: Der rätselhafte Fahrer
  Comment[EN]: The enigmatic driver
Passenger:
  Comment[FOR-ALL]: A boring passenger
  Comment[DE]: Ein langweiliger Passagier
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

    def test_arxml4(self):
        args = Args('tests/files/arxml/system-4.2.arxml')
        args.print_nodes = True

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
DJ:
Dancer:
  Comment[FOR-ALL]: Rhythm is a Dancer!
Guard:
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        # Prepare mocks.
        args = Args('tests/files/arxml/system-4.2.arxml')
        args.items = ['Message2']

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
Message2:
  Bus: Pch0
  Sending ECUs: Dancer
  Frame ID: 0x6 (6)
  Size: 7 bytes
  Is extended frame: True
  Is CAN-FD frame: True
  Cycle time: 200 ms
  Is network management frame: False
  Is secured: False
  Signal tree:

    -- {root}
       +-- signal3
       +-- signal2
       +-- signal4

  Signal details:
    signal3:
      Receiving ECUs: DJ
      Internal type: Integer
      Start bit: 6
      Length: 2 bits
      Byte order: little_endian
      Is signed: False
    signal2:
      Comment[FOR-ALL]: Signal comment!
      Receiving ECUs: DJ
      Internal type: Integer
      Start bit: 18
      Length: 11 bits
      Byte order: little_endian
      Is signed: True
    signal4:
      Receiving ECUs: DJ
      Internal type: Integer
      Start bit: 30
      Length: 4 bits
      Byte order: little_endian
      Is signed: False
      Named values:
        1: one
          Comment[EN]: One Comment
          Comment[DE]: Ein Kommentar
        2: two
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        args = Args('tests/files/arxml/system-4.2.arxml')
        args.items = ['AlarmStatus']

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
AlarmStatus:
  Bus: Pch0
  Sending ECUs: Guard
  Frame ID: 0x3e9 (1001)
  Size: 1 bytes
  Is extended frame: False
  Is CAN-FD frame: False
  Is network management frame: True
  Is secured: False
  Signal tree:

    -- {root}
       +-- FireAlarm

  Signal details:
    FireAlarm:
      Receiving ECUs: DJ, Dancer
      Internal type: Integer
      Start bit: 0
      Length: 1 bits
      Byte order: little_endian
      Initial value: 0
      Is signed: False
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        args = Args('tests/files/arxml/system-4.2.arxml')
        args.exclude_normal = True

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = 'Message2\n'

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        args = Args('tests/files/arxml/system-4.2.arxml')
        args.exclude_extended = True

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
AlarmStatus
Message1
Message3
Message4
MessageWithoutPDU
MultiplexedMessage
OneToContainThemAll
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        args = Args('tests/files/arxml/system-4.2.arxml')
        args.items = [ 'IAmAGhost' ]

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
No message named "IAmAGhost" has been found in input file.
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        args = Args('tests/files/arxml/system-4.2.arxml')
        args.items = [ 'Message1' ]

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
Message1:
  Comment[EN]: Comment1
  Comment[DE]: Kommentar1
  Bus: Pch0
  Sending ECUs: DJ
  Frame ID: 0x5 (5)
  Size: 9 bytes
  Is extended frame: False
  Is CAN-FD frame: True
  Is network management frame: False
  End-to-end properties:
    Category: Profile2
    Data IDs: [123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138]
    Protected size: 9 bytes
  Is secured: False
  Signal tree:

    -- {root}
       +-- message1_SeqCounter
       +-- message1_CRC
       +-- signal6
       +-- signal1
       +-- signal5

  Signal details:
    message1_SeqCounter:
      Receiving ECUs: Dancer
      Internal type: Integer
      Start bit: 0
      Length: 16 bits
      Byte order: little_endian
      Is signed: False
    message1_CRC:
      Receiving ECUs: Dancer
      Internal type: Integer
      Start bit: 16
      Length: 16 bits
      Byte order: little_endian
      Is signed: False
    signal6:
      Receiving ECUs: Dancer
      Internal type: Integer
      Start bit: 32
      Length: 1 bits
      Byte order: little_endian
      Unit: wp
      Initial value: zero
      Is signed: False
      Minimum: 0.0 wp
      Maximum: 0.1 wp
      Offset: 0.0 wp
      Scaling factor: 0.1 wp
      Named values:
        0: zero
          Comment[EN]: Nothing
          Comment[DE]: Nichts
    signal1:
      Comment[EN]: Signal comment!
      Comment[DE]: Signalkommentar!
      Receiving ECUs: Dancer
      Internal type: Integer
      Start bit: 36
      Length: 3 bits
      Byte order: big_endian
      Unit: m
      Initial value: 25 m
      Is signed: False
      Minimum: 0.0 m
      Maximum: 20.0 m
      Offset: 0 m
      Scaling factor: 5 m
    signal5:
      Receiving ECUs: Dancer
      Internal type: Float
      Start bit: 40
      Length: 32 bits
      Byte order: little_endian
      Is signed: False
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        args = Args('tests/files/arxml/system-4.2.arxml')
        args.items = [ "Message3" ]

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
Message3:
  Bus: Pch0
  Sending ECUs: Dancer
  Frame ID: 0x64 (100)
  Size: 6 bytes
  Is extended frame: False
  Is CAN-FD frame: False
  Is network management frame: False
  End-to-end properties:
    Category: Profile5
    Data IDs: [321]
    Protected size: 4 bytes
  Is secured: True
  Security properties:
    Authentication algorithm: KnockKnock
    Freshness algorithm: SmellyCheese
    Data ID: 1337
    Authentication transmit bits: 10
    Freshness counter size: 32 bits
    Freshness counter transmit size: 6 bits
    Secured size: 4 bytes
  Signal tree:

    -- {root}
       +-- message3_CRC
       +-- message3_SeqCounter
       +-- Message3_Freshness
       +-- Message3_Authenticator

  Signal details:
    message3_CRC:
      Receiving ECUs: DJ
      Internal type: Integer
      Start bit: 0
      Length: 8 bits
      Byte order: little_endian
      Is signed: False
    message3_SeqCounter:
      Receiving ECUs: DJ
      Internal type: Integer
      Start bit: 8
      Length: 4 bits
      Byte order: little_endian
      Is signed: False
    Message3_Freshness:
      Comment[FOR-ALL]: Truncated freshness value for 'Message3'
      Receiving ECUs: DJ
      Internal type: Integer
      Start bit: 39
      Length: 6 bits
      Byte order: big_endian
      Is signed: False
    Message3_Authenticator:
      Comment[FOR-ALL]: Truncated authenticator value for 'Message3'
      Receiving ECUs: DJ
      Internal type: Integer
      Start bit: 33
      Length: 10 bits
      Byte order: big_endian
      Is signed: False
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        args = Args('tests/files/arxml/system-4.2.arxml')
        args.print_buses = True

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
Pch0:
  Comment[FOR-ALL]: The great CAN cluster
  Baudrate: 500000
  CAN-FD enabled: True
  FD Baudrate: 2000000
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)


    def test_kcd(self):
        # Prepare mocks.
        args = Args('tests/files/kcd/dump.kcd')
        args.exclude_extended = True
        args.print_all = True

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
Message1:
  Bus: Bus
  Sending ECUs: Node1
  Frame ID: 0x1 (1)
  Size: 5 bytes
  Is extended frame: False
  Is CAN-FD frame: False
  Signal tree:

    -- {root}
       +-- Signal1
       +-- Signal2

  Signal details:
    Signal1:
      Internal type: Integer
      Start bit: 0
      Length: 1 bits
      Byte order: little_endian
      Is signed: False
    Signal2:
      Receiving ECUs: Node2, Node3
      Internal type: Float
      Start bit: 8
      Length: 32 bits
      Byte order: little_endian
      Is signed: False
      Named values:
        0: label1
        1: label2
Message2:
  Comment[None]: Note message 2.
  Bus: Bus
  Sending ECUs: Node2, Node3
  Frame ID: 0x2 (2)
  Size: 4 bytes
  Is extended frame: False
  Is CAN-FD frame: False
  Cycle time: 100 ms
  Signal tree:

    -- {root}
       +-- Mux1
       |   +-- 0
       |   |   +-- Signal1
       |   |   +-- Signal2
       |   +-- 1
       |       +-- Signal3
       |       +-- Signal4
       +-- Mux2
       |   +-- 0
       |       +-- Signal5
       +-- Signal6

  Signal details:
    Signal1:
      Internal type: Integer
      Selector signal: Mux1
      Selector values: 0
      Start bit: 0
      Length: 8 bits
      Byte order: little_endian
      Is signed: False
    Signal3:
      Internal type: Integer
      Selector signal: Mux1
      Selector values: 1
      Start bit: 0
      Length: 8 bits
      Byte order: little_endian
      Is signed: False
    Signal2:
      Internal type: Integer
      Selector signal: Mux1
      Selector values: 0
      Start bit: 8
      Length: 8 bits
      Byte order: little_endian
      Is signed: False
    Signal4:
      Internal type: Integer
      Selector signal: Mux1
      Selector values: 1
      Start bit: 8
      Length: 8 bits
      Byte order: little_endian
      Is signed: False
    Mux1:
      Internal type: Multiplex Selector
      Start bit: 16
      Length: 2 bits
      Byte order: little_endian
      Is signed: False
    Mux2:
      Internal type: Multiplex Selector
      Start bit: 18
      Length: 1 bits
      Byte order: little_endian
      Is signed: False
    Signal5:
      Internal type: Integer
      Selector signal: Mux2
      Selector values: 0
      Start bit: 19
      Length: 1 bits
      Byte order: little_endian
      Is signed: False
    Signal6:
      Comment[None]: Note signal 6.
      Receiving ECUs: Node1
      Internal type: Integer
      Start bit: 20
      Length: 12 bits
      Byte order: little_endian
      Unit: Cel
      Is signed: True
      Minimum: 0 Cel
      Maximum: 100 Cel
      Offset: -40 Cel
      Scaling factor: 0.05 Cel
      Named values:
        0: init
Message4:
  Bus: Bus
  Frame ID: 0x4 (4)
  Size: 5 bytes
  Is extended frame: False
  Is CAN-FD frame: False
  Signal tree:

    -- {root}
       +-- Signal1
       +-- Signal2

  Signal details:
    Signal1:
      Internal type: Integer
      Start bit: 7
      Length: 1 bits
      Byte order: big_endian
      Is signed: False
    Signal2:
      Internal type: Integer
      Start bit: 8
      Length: 12 bits
      Byte order: big_endian
      Is signed: False
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        # Prepare mocks.
        args = Args('tests/files/kcd/dump.kcd')
        args.exclude_normal = True
        args.print_all = True

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = """\
Message3:
  Bus: Bus
  Frame ID: 0x3 (3)
  Size: 8 bytes
  Is extended frame: True
  Is CAN-FD frame: False
  Signal tree:

    -- {root}
       +-- Signal1

  Signal details:
    Signal1:
      Internal type: Float
      Start bit: 0
      Length: 64 bits
      Byte order: little_endian
      Is signed: False
"""

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

        # Prepare mocks.
        args = Args('tests/files/kcd/dump.kcd')
        args.exclude_normal = True
        args.exclude_extended = True
        args.print_all = True

        stdout = StringIO()
        with patch('sys.stdout', stdout):
            # Run the main function of the subparser
            list_module._do_list(args)

            # check make sure it behaves as expected
            expected_output = ''

            actual_output = stdout.getvalue()
            self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()
