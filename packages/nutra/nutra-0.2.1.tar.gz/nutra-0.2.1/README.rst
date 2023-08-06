**************
 nutratracker
**************

.. image:: https://badgen.net/pypi/v/nutra
    :target: https://pypi.org/project/nutra/
    :alt: Latest version unknown|
.. image:: https://api.travis-ci.com/nutratech/cli.svg?branch=master
    :target: https://travis-ci.com/nutratech/cli
    :alt: Build status unknown|
.. image:: https://pepy.tech/badge/nutra/month
    :target: https://pepy.tech/project/nutra
    :alt: Monthly downloads unknown|
.. image:: https://img.shields.io/pypi/pyversions/nutra.svg
    :alt: Python3 (3.6 - 3.9)|
.. image:: https://badgen.net/badge/code%20style/black/000
    :target: https://github.com/ambv/black
    :alt: Code style: black|
.. image:: https://badgen.net/pypi/license/nutra
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License GPL-3

Extensible command-line tools for nutrient analysis.

*Requires:*

- Python 3.6.5 or later
- Package manager (pip3)
- Internet connection


See database: https://github.com/gamesguru/ntdb

See server:   https://github.com/gamesguru/nutra-server

Notes
=====

On macOS and Linux, you may need to add the following line to
your `.profile` file:

.. code-block:: bash

    export $PATH=$PATH:/usr/local/bin

On Windows you should check the box during the Python installer
to include `Scripts` directory in your `PATH`.  This can be done
manually after installation too.

Install PyPi release (from pip)
===============================
:code:`pip install nutra`

(**Note:** use :code:`pip3` on Linux/macOS)

**Update to latest**

:code:`pip install -U nutra`

**Subscribe to the development release**

:code:`pip install --pre -U nutra`

Using the source-code directly
##############################
.. code-block:: bash

    git clone git@github.com:nutratech/cli.git
    cd nutra
    pip3 install -r requirements.txt
    ./nutra init

or,

.. code-block:: bash

    git clone git@github.com:nutratech/cli.git
    cd nutra
    pip install .
    nutra init

When building the PyPi release use the commands:

.. code-block:: bash

    python3 setup.py sdist
    twine upload dist/nutra-X.X.X.tar.gz

Argcomplete (tab completion on Linux/macOS)
===========================================

After installing nutra, argcomplete package should also be installed,

Simply run:

.. code-block:: bash

    activate-global-python-argcomplete

Then you can press tab to fill in or list subcommands and argument flags.

Currently Supported Data
========================

**USDA Stock database**

- Standard reference database (SR28)  [7794 foods]


**Relative USDA Extensions**

- Flavonoid, Isoflavonoids, and Proanthocyanidins  [1352 foods]

Usage
=====

Requires internet connection to download initial data.

Run the :code:`nutra` script to output usage.

Usage: :code:`nutra <command>`


Commands
########

::

    usage: nutra [-h] [-v] [--debug] {init,nt,search,sort,anl,day,recipe,bio} ...

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      --debug               enable detailed error messages

    nutra subcommands:
      {init,nt,search,sort,anl,day,recipe,bio}
        init                setup profiles, USDA and NT database
        nt                  list out nutrients and their info
        search              search foods by name, list overview info
        sort                sort foods by nutrient ID
        anl                 analyze food(s)
        day                 analyze a DAY.csv file, RDAs optional
        recipe              list and analyze recipes
        bio                 view, add, remove biometric logs

