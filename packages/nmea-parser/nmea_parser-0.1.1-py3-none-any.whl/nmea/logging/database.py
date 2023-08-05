""" Module for logging GPS data to a database
"""

import sqlite3
from typing import Union
from pathlib import Path
import sys


class GenericDBConnection:
    """ Generic Database connection
    """

    _cnx = None
    _crs = None

    def __init__(self, connection):
        """ Constructor

        :param connection: Instance of a database connection. Either mysql connector or sqlite3

        """

        self._cnx = connection
        self._crs = self._cnx.cursor(buffered=True) if isinstance(self._cnx, sqlite3.Connection) else self._cnx.cursor()

        self._create_schema()

    def _create_schema(self):
        """ Create tables and indices
        """

        self.safe_execute(SCHEMA_DDL_FRAME)
        self.safe_execute(SCHEMA_DDL_SV_OBS)

    def safe_execute(self, stmt: str):
        """ Safely execute an SQL insert statement

        :param stmt: Statement to execute

        """

        assert isinstance(stmt, str)

        stmt = stmt.replace("None", "NULL")

        try:
            self._crs.execute(stmt)
        except Exception as e:
            print("Error executing query %s:" % stmt, str(e), file=sys.stderr)


class SQLiteConnection(GenericDBConnection):
    """ Wrap an SQLite database connection
    """

    def __init__(self, cnx: sqlite3.Connection):
        """ Constructor

        :param path: SQLite3 database connection

        """

        GenericDBConnection.__init__(self, cnx)

    def __repr__(self):
        return '<SQLite 3 connection>'

    @classmethod
    def from_path(cls, path: Union[Path, str]):
        """ Open an SQLite connection at a path

        :param path: Path to database. Either string or pathlib.Path
        :return: New instance of SQlite connection

        """

        if not isinstance(path, str) and not isinstance(path, Path):
            raise TypeError('Path parameter must be `str` or `pathlib.Path`')

        cnx = sqlite3.connect(str(path))
        return SQLiteConnection(cnx)

    def safe_execute(self, stmt: str):
        """ Safely execute a database statement. Commit afterwards.

        :param stmt: Statement to execute

        """

        GenericDBConnection.safe_execute(self, stmt)
        self._cnx.commit()


class MYSQLConnection (GenericDBConnection):
    """ Wrap a mySQL database connection
    """

    def __init__(self, cnx):
        GenericDBConnection.__init__(self, cnx)

    def __repr__(self):
        return "<mySQL Database connection>"


SCHEMA_DDL_FRAME = "CREATE TABLE IF NOT EXISTS data_frame (gpst datetime, fix_lat real default null, " \
                         "fix_lon real default null, quality integer, sv_in_sol integer, alt real, alt_unit char," \
                         "fix_dims integer, rmc_fix_date date, rmc_time time, rmc_lat real default null, rmc_lon real,"\
                         "rmc_spd_kts real default null, rmc_track_deg real default null," \
                         "mag_variation real default null, gll_lat real default null, gll_lon real default null," \
                         "gll_fix_time time, vtg_true_track float default null, vtg_mag_track real default null," \
                         "vtg_gs_kts real default null);"

SCHEMA_DDL_SV_OBS = "CREATE TABLE IF NOT EXISTS sv_observation (gpst datetime, prn int, elevation real, azimuth real," \
                    "snr real);"
