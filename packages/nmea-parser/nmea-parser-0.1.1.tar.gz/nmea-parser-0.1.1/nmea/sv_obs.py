""" Module containing data structures pertaining to NMEA observations
"""

__author__ = "Brendan Kristiansen"
__copyright__ = "Copyright 2021, Brendan Kristiansen"
__credits__ = ["Brendan Kristiansen"]
__license__ = "MPL 2.0"
__version__ = "0.1.0"
__maintainer__ = "Brendan Kristiansen"
__email__ = "b@bek.sh"


class SVObservation:

    _prn: int
    _elev: float
    _az: float
    _snr: float

    def __init__(self, prn: int, elev: float, azimuth: float, snr: float):

        self._prn = prn
        self._elev = elev
        self._az = azimuth
        self._snr = snr

    def __str__(self):
        return "Observation of SV %d: SNR %f" % (self._prn, self._snr)

    def generate_insert_statement(self, gpst) -> str:
        """ Generate an SQL insert statement to record this observation

        :return: Statement for database

        """

        stmt = "INSERT INTO sv_observation ("
        stmt += '"%s", ' % gpst
        stmt += str(self._prn) + ', '
        stmt += str(self._elev) + ', '
        stmt += str(self._az) + ', '
        stmt += str(self._snr) + ', '
        stmt += ');'

        return stmt

    @property
    def prn(self):
        return self._prn

    @property
    def elevation(self):
        return self._elev

    @property
    def azimuth(self):
        return self._az

    @property
    def snr(self):
        return self._snr
