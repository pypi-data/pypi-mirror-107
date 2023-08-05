""" Module containing a generic input stream
"""
import abc
from typing import Union, TextIO
from pathlib import Path, PosixPath

import serial

__author__ = "Brendan Kristiansen"
__copyright__ = "Copyright 2021, Brendan Kristiansen"
__credits__ = ["Brendan Kristiansen"]
__license__ = "MPL 2.0"
__maintainer__ = "Brendan Kristiansen"
__email__ = "b@bek.sh"


class GenericInputStream:
    """ Generic input stream
    """

    @staticmethod
    def open_stream(path: Union[str, Path], baud=4800):
        """ Input stream factory

        :param path: Path to stream (file or serial port)
        :param baud: Baud rate of serial port. Ignored if file

        :return: Input stream instance

        """

        if not isinstance(path, str) and not isinstance(path, Path):
            raise TypeError("Path must be a string or pathlib.Path")
        if not isinstance(baud, int):
            raise TypeError("Baud rate must be an integer")

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError("Specified GNSS source does not exist.")

        if path.is_char_device():
            return SerialPort(path, baud=baud)

        return InputFileStream(path)

    def __del__(self):
        self.ensure_closed()

    def __enter__(self):
        self.ensure_open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ensure_closed()

    def get_line(self) -> bytes:
        """ Receive a single line from the input stream

        :return: Encoded line (bytes)

        """

        raise NotImplementedError

    def ensure_open(self):
        """ Ensure stream is open
        """

        raise NotImplementedError

    def ensure_closed(self):
        """ Ensure stream is closed
        """

        raise NotImplementedError


class InputFileStream (GenericInputStream):
    """ Read GPS data from a file
    """

    _fp = Union[TextIO, None]

    _path: Path

    def __init__(self, path: Union[Path, str]):
        """ Constructor

        :param path: Path to input file

        """

        if not isinstance(path, str) and not isinstance(path, Path):
            raise TypeError("Path must be a string or pathlib.Path")

        self._path = Path(path)
        if not self._path.exists():
            raise FileNotFoundError("Specified file %s does not exist." % str(self._path))

        self._fp = None

    def get_line(self) -> bytes:
        self.ensure_open()
        return self._fp.readline()

    def ensure_open(self):
        if self._fp is None:
            self._fp = open(self._path, "rb")

    def ensure_closed(self):
        if self._fp is not None:
            self._fp.close()
        self._fp = None


class SerialPort (GenericInputStream):
    """ Read NMEA stream from a serial port
    """

    _port: Union[serial.Serial, None]

    _port: Path
    _baud: int

    def __init__(self, path: Union[str, Path], baud: int = 4800):

        if not isinstance(path, str) and not isinstance(path, Path):
            raise TypeError("Path must be a string or pathlib.Path")
        if not isinstance(baud, int):
            raise TypeError("Baud rate must be an integer")

        self._port = Path(path)
        self._baud = baud

        self._port = None

    def get_line(self) -> bytes:
        self.ensure_open()
        return self._port.readline()

    def ensure_open(self):
        if self._port is None:
            self._port = serial.Serial(port=str(self._port), baudrate=self._baud)
        if not self._port.is_open:
            self._port.open()

    def ensure_closed(self):

        if self._port.is_open:
            self._port.close()
