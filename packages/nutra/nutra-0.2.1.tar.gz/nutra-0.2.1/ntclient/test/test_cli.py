# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:19:53 2020

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutrient analysis and composition application.
Copyright (C) 2018-2021  Shane Jaroch

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pytest

from ntclient import __db_target_nt__, __db_target_usda__
from ntclient.persistence.sql.nt import funcs as nt_funcs, nt_ver
from ntclient.persistence.sql.usda import funcs as usda_funcs, usda_ver
from ntclient.services import init


# TODO: integration tests.. create user, recipe, log.. analyze & compare


def test_0_init():
    """Tests the SQL/persistence init in real time"""
    result = init()
    assert result


def test_1_usda_sql_funcs():
    """Performs cursory inspection (sanity checks) of usda.sqlite image"""
    version = usda_ver()
    assert version == __db_target_usda__
    result = usda_funcs.sql_nutrients_details()
    assert len(result[1]) == 186

    result = usda_funcs.sql_servings([9050, 9052])
    assert len(result) == 3

    result = usda_funcs.sql_analyze_foods([23567, 23293])
    assert len(result) == 188

    result = usda_funcs.sql_sort_foods(789)
    assert len(result) == 415
    # result = usda_funcs.sql_sort_foods(789, fdgrp_ids=[100])
    # assert len(result) == 1

    result = usda_funcs.sql_sort_foods_by_kcal(789)
    assert len(result) == 246
    # result = usda_funcs.sql_sort_foods_by_kcal(789, fdgrp_ids=[1100])
    # assert len(result) == 127


def test_2_nt_sql_funcs():
    """Performs cursory inspection (sanity check) of nt.sqlite image"""
    version = nt_ver()
    assert version == __db_target_nt__

    headers, rows = nt_funcs.sql_biometrics()
    assert headers == ["id", "created", "updated", "name", "unit"]
    assert len(rows) == 29


def main():
    """Main method callable from outside package (test.py in main folder)"""
    pytest.main(args=["-s", "-v"])
