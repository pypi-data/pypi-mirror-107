"""Nutratracker DB specific sqlite module"""
import os
import sqlite3

from ntclient import NT_DB_NAME, NUTRA_DIR, __db_target_nt__
from ntclient.persistence.sql import close_con_and_cur, sql_entries
from ntclient.utils.exceptions import SqlConnectError, SqlInvalidVersionError


def nt_sqlite_connect(version_check=True):
    """Connects to the nt.sqlite file, or throws an exception"""
    db_path = os.path.join(NUTRA_DIR, NT_DB_NAME)
    if os.path.isfile(db_path):
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row

        # Verify version
        if version_check and nt_ver() != __db_target_nt__:
            raise SqlInvalidVersionError(
                "ERROR: nt target [{0}] mismatch actual [{1}] ".format(
                    __db_target_nt__, nt_ver()
                )
                + "upgrades not supported, please remove '~/.nutra/nt.sqlite' and run 'nutra init'"
            )
        return con

    # Else it's not on disk
    raise SqlConnectError("ERROR: nt database doesn't exist, please run `nutra init`")


def nt_ver():
    """Gets version string for nt.sqlite database"""
    con = nt_sqlite_connect(version_check=False)
    cur = con.cursor()
    result = cur.execute("SELECT * FROM version;").fetchall()
    close_con_and_cur(con, cur, commit=False)
    return result[-1][1]


def _sql(query, values=None, headers=False):
    """Executes a SQL command to nt.sqlite"""
    from ntclient import DEBUG  # pylint: disable=import-outside-toplevel

    con = nt_sqlite_connect()
    cur = con.cursor()
    # TODO: format parameterized debug queries
    if DEBUG:
        # sqlite3.enable_callback_tracebacks(True)
        print("nt.sqlite: " + query)
    # TODO: separate `entry` & `entries` entity for single vs. bulk insert?
    if values:
        if isinstance(values, list):
            rows = cur.executemany(query, values)
        else:  # tuple
            rows = cur.execute(query, values)
    else:
        rows = cur.execute(query)
    result = sql_entries(rows, headers=headers)
    close_con_and_cur(con, cur)
    return result
