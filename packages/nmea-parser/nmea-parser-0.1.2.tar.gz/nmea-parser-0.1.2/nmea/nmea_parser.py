""" NMEA parser module
"""

import sys

from . import nmea_message

__author__ = "Brendan Kristiansen"
__copyright__ = "Copyright 2021, Brendan Kristiansen"
__credits__ = ["Brendan Kristiansen"]
__license__ = "MPL 2.0"
__version__ = "0.1.0"
__maintainer__ = "Brendan Kristiansen"
__email__ = "b@bek.sh"


class NMEAParser:

    @staticmethod
    def decode_message(msg: bytes):
        if NMEAParser.verify_checksum(msg):
            return nmea_message.NMEAMessage.load_message(msg)
        else:
            print("Bad checksum:", str(msg), file=sys.stderr)
            return None

    @staticmethod
    def verify_checksum(message: bytes) -> bool:
        """ Verify a NMEA message via checksum

        :param message: Bytes from NMEA stream

        :return: Boolean. True if valid

        """

        assert isinstance(message, bytes)

        xor = 0x00

        # message = str(message)

        try:

            start = message.find(ord('$'))+1
            end = message.find(ord('*'))

            for char in message[start:end]:
                xor = char ^ xor

            exp = str(message[end+1:end+3].decode()).upper()
            res = str(hex(xor))[2:].upper().zfill(2)

            return exp == res

        except:
            return False
