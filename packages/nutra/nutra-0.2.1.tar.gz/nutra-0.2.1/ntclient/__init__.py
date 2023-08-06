"""Top level package"""
import os
import sys

from ntclient.ntsqlite.sql import NT_DB_NAME

# Package info
__title__ = "nutra"
__version__ = "0.2.1"
__author__ = "Shane Jaroch"
__license__ = "GPL v3"
__copyright__ = "Copyright 2018-2021 Shane Jaroch"

# Sqlite target versions
__db_target_nt__ = "0.0.3"
__db_target_usda__ = "0.0.8"

# Global variables
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
NUTRA_DIR = os.path.join(os.path.expanduser("~"), ".nutra")
USDA_DB_NAME = "usda.sqlite"
# NT_DB_NAME = "nt.sqlite"  # defined in ntclient.ntsqlite.sql
DEBUG = False

# Check Python version
PY_MIN_VER = (3, 4, 3)
PY_SYS_VER = sys.version_info[0:3]
if PY_SYS_VER < PY_MIN_VER:
    PY_MIN_STR = ".".join(str(x) for x in PY_MIN_VER)
    PY_SYS_STR = ".".join(str(x) for x in PY_SYS_VER)
    print("ERROR: nutra requires Python %s or later to run" % PY_MIN_STR)
    print("HINT:  You're running Python " + PY_SYS_STR)
    sys.exit(1)


# Setter functions
def set_debug(debug):
    """Sets DEBUG flag from main (after arg parse). Accessible throughout package"""
    global DEBUG  # pylint: disable=global-statement
    DEBUG = debug


# TODO:
#  display full food name in results?
#  display refuse
#  nested nutrient tree, like: http://www.whfoods.com/genpage.php?tname=nutrientprofile&dbid=132
#  attempt to record errors in failed try/catch block (bottom of main.py)
#  make use of argcomplete.warn(msg) ?
