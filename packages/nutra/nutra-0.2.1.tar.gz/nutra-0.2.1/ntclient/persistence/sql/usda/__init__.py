"""USDA DB specific sqlite module"""
import os
import sqlite3
import tarfile
import urllib.request

from ntclient import NUTRA_DIR, USDA_DB_NAME, __db_target_usda__
from ntclient.persistence.sql import close_con_and_cur, sql_entries
from ntclient.utils.exceptions import SqlConnectError, SqlInvalidVersionError


def usda_init(yes=False):
    """On-boarding function. Downloads tarball and unpacks usda.sqlite file"""

    def input_agree():
        return input("\nAgree to USDA download, may take minutes? [Y/n] ")

    # TODO: handle resource moved on Bitbucket or version mismatch due to manual overwrite?
    url = (
        "https://bitbucket.org/dasheenster/nutra-utils/downloads/{0}-{1}.tar.xz".format(
            USDA_DB_NAME, __db_target_usda__
        )
    )

    if USDA_DB_NAME not in os.listdir(NUTRA_DIR):
        if yes or input_agree().lower() == "y":
            # TODO: save with version in filename? Don't re-download tarball, just extract?
            save_path = os.path.join(NUTRA_DIR, "%s.tar.xz" % USDA_DB_NAME)

            # Download usda.sqlite.tar.xz
            print("curl -L {url} -o %s.tar.xz" % USDA_DB_NAME)
            urllib.request.urlretrieve(url, save_path)

            # Extract the archive
            with tarfile.open(save_path, mode="r:xz") as usda_sqlite_file:
                print("\ntar xvf %s.tar.xz" % USDA_DB_NAME)
                usda_sqlite_file.extractall(NUTRA_DIR)

            print("==> done downloading %s" % USDA_DB_NAME)

    if usda_ver() != __db_target_usda__:
        raise SqlInvalidVersionError(
            "ERROR: usda target [{0}] mismatch actual [{1}], ".format(
                __db_target_usda__, usda_ver()
            )
            + "please contact support or try again"
        )


def usda_sqlite_connect(verify_version=True):
    """Connects to the usda.sqlite file, or throws an exception"""
    # TODO: support as customizable env var ?
    db_path = os.path.join(NUTRA_DIR, USDA_DB_NAME)
    if os.path.isfile(db_path):
        con = sqlite3.connect(db_path)
        # con.row_factory = sqlite3.Row  # see: https://chrisostrouchov.com/post/python_sqlite/

        # Verify version
        if verify_version and usda_ver() != __db_target_usda__:
            raise SqlInvalidVersionError(
                "ERROR: usda target [{0}] mismatch actual [{1}], ".format(
                    __db_target_usda__, usda_ver()
                )
                + "remove '~/.nutra/usda.sqlite' and run 'nutra init'"
            )
        return con

    # Else it's not on disk
    raise SqlConnectError("ERROR: usda database doesn't exist, please run `nutra init`")


def usda_ver():
    """Gets version string for usda.sqlite database"""
    con = usda_sqlite_connect(verify_version=False)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM version;").fetchall()
    close_con_and_cur(con, cur, commit=False)
    return rows[-1][1]


def _sql(query, headers=False):
    """Executes a SQL command to usda.sqlite"""
    from ntclient import DEBUG  # pylint: disable=import-outside-toplevel

    con = usda_sqlite_connect()
    cur = con.cursor()
    if DEBUG:
        print("usda.sqlite: " + query)
    rows = cur.execute(query)
    result = sql_entries(rows, headers=headers)
    close_con_and_cur(con, cur)
    return result
