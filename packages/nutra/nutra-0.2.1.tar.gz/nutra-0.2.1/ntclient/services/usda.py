# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 20:28:06 2018

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

import shutil

from tabulate import tabulate

from ntclient.persistence.sql.usda.funcs import (
    _sql,
    sql_analyze_foods,
    sql_nutrients_details,
    sql_nutrients_overview,
    sql_sort_foods,
    sql_sort_foods_by_kcal,
)
from ntclient.utils import (
    FOOD_NAME_TRUNC,
    NUTR_ID_KCAL,
    NUTR_IDS_AMINOS,
    NUTR_IDS_FLAVONES,
    SEARCH_LIMIT,
)


def list_nutrients():
    """Lists out nutrients with basic details"""
    headers, nutrients = sql_nutrients_details()
    # TODO: include in SQL table cache?
    headers.append("avg_rda")
    nutrients = [list(x) for x in nutrients]
    for nutrient in nutrients:
        rda = nutrient[1]
        val = nutrient[6]
        if rda:
            nutrient.append(round(100 * val / rda, 1))
        else:
            nutrient.append(None)

    table = tabulate(nutrients, headers=headers, tablefmt="simple")
    print(table)
    return nutrients


# -------------------------
# Sort
# -------------------------
def truncate_results(results):
    """Returns truncated list for multiple functions"""
    return [list(x) for x in results][:SEARCH_LIMIT]


def print_results(results, nutrient_id):
    """Prints truncated list for sort"""
    nutrients = sql_nutrients_overview()
    nutrient = nutrients[nutrient_id]
    unit = nutrient[2]

    headers = ["food", "fdgrp", "val (%s)" % unit, "kcal", "long_desc"]

    table = tabulate(results, headers=headers, tablefmt="simple")
    print(table)
    return results


def sort_foods_by_nutrient_id(nutrient_id, by_kcal):
    """Sort, by nutrient, either (amount / 100 g) or (amount / 200 kcal)"""
    # TODO: sub shrt_desc for long if available, and support config.FOOD_NAME_TRUNC
    if by_kcal:
        results = truncate_results(sql_sort_foods_by_kcal(nutrient_id))
    else:
        results = truncate_results(sql_sort_foods(nutrient_id))
    return print_results(results, nutrient_id)


# -------------------------
# Search
# -------------------------
def search(words):
    """Searches foods for input"""
    from fuzzywuzzy import fuzz  # pylint: disable=import-outside-toplevel

    food_des = _sql("SELECT * FROM food_des;")

    query = " ".join(words)
    scores = {f[0]: fuzz.token_set_ratio(query, f[2]) for f in food_des}
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:SEARCH_LIMIT]

    food_ids = [s[0] for s in scores]
    nut_data = sql_analyze_foods(food_ids)

    # Tally foods
    foods_nutrients = {}
    for food_id, nutr_id, nutr_val in nut_data:
        if food_id not in foods_nutrients:
            foods_nutrients[food_id] = {nutr_id: nutr_val}  # init dict
        else:
            foods_nutrients[food_id][nutr_id] = nutr_val

    def search_results(_scores):
        """Generates search results, consumable by tabulate"""
        _results = []
        for score in _scores:
            _food_id = score[0]
            score = score[1]

            food = food_des[_food_id]
            fdgrp_id = food[1]
            long_desc = food[2]
            shrt_desc = food[3]

            nutrients = foods_nutrients[_food_id]
            result = {
                "food_id": _food_id,
                "fdgrp_id": fdgrp_id,
                # TODO: get more details from another function, maybe enhance food_details() ?
                # "fdgrp_desc": cache.fdgrp[fdgrp_id]["fdgrp_desc"],
                # "data_src": cache.data_src[data_src_id]["name"],
                "long_desc": shrt_desc if shrt_desc else long_desc,
                "score": score,
                "nutrients": nutrients,
            }
            _results.append(result)
        return _results

    # TODO: include C/F/P macro ratios as column?
    food_des = {f[0]: f for f in food_des}
    results = search_results(scores)

    tabulate_search(results)


def tabulate_search(results):
    """Makes search results more readable"""
    # Current terminal size
    # TODO: display "nonzero/total" report nutrients, aminos, and flavones..
    #  sometimes zero values are not useful
    # TODO: macros, ANDI score, and other metrics on preview
    # bufferwidth = shutil.get_terminal_size()[0]
    bufferheight = shutil.get_terminal_size()[1]

    headers = [
        "food",
        "fdgrp",
        "kcal",
        "food_name",
        "Nutr",
        "Amino",
        "Flav",
    ]
    rows = []
    for i, result in enumerate(results):
        if i == bufferheight - 4:
            break
        food_id = result["food_id"]
        # TODO: dynamic buffer
        # food_name = r["long_desc"][:45]
        # food_name = r["long_desc"][:bufferwidth]
        food_name = result["long_desc"][:FOOD_NAME_TRUNC]
        # TODO: decide on food group description?
        # fdgrp_desc = r["fdgrp_desc"]
        fdgrp = result["fdgrp_id"]

        nutrients = result["nutrients"]
        kcal = nutrients.get(NUTR_ID_KCAL)
        len_aminos = len(
            [nutrients[n_id] for n_id in nutrients if int(n_id) in NUTR_IDS_AMINOS]
        )
        len_flavones = len(
            [nutrients[n_id] for n_id in nutrients if int(n_id) in NUTR_IDS_FLAVONES]
        )

        row = [
            food_id,
            fdgrp,
            kcal,
            food_name,
            len(nutrients),
            len_aminos,
            len_flavones,
        ]
        rows.append(row)
        # avail_buffer = bufferwidth - len(food_id) - 15
        # if len(food_name) > avail_buffer:
        #     rows.append([food_id, food_name[:avail_buffer] + "..."])
        # else:
        #     rows.append([food_id, food_name])
    table = tabulate(rows, headers=headers, tablefmt="simple")
    print(table)
    return rows
