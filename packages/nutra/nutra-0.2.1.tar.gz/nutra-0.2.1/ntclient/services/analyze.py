# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 23:57:03 2018

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

import csv
import shutil
from collections import OrderedDict

from colorama import Fore, Style
from tabulate import tabulate

from ntclient.persistence.sql.usda.funcs import (
    sql_analyze_foods,
    sql_food_details,
    sql_nutrients_overview,
    sql_servings,
)
from ntclient.utils import (
    COLOR_CRIT,
    COLOR_DEFAULT,
    COLOR_OVER,
    COLOR_WARN,
    NUTR_ID_CARBS,
    NUTR_ID_FAT_TOT,
    NUTR_ID_FIBER,
    NUTR_ID_KCAL,
    NUTR_ID_PROTEIN,
    THRESH_CRIT,
    THRESH_OVER,
    THRESH_WARN,
)


def foods_analyze(food_ids, grams=None):
    """Analyze a list of food_ids against stock RDA values"""
    # TODO: from ntclient.utils.nutprogbar import nutprogbar
    # Get analysis
    raw_analyses = sql_analyze_foods(food_ids)
    analyses = {}
    for analysis in raw_analyses:
        food_id = analysis[0]
        if grams is not None:
            anl = (analysis[1], round(analysis[2] * grams / 100, 2))
        else:
            anl = (analysis[1], analysis[2])
        if food_id not in analyses:
            analyses[food_id] = [anl]
        else:
            analyses[food_id].append(anl)
    # serving = servings()[1]
    serving = sql_servings(food_ids)
    food_des = sql_food_details(food_ids)
    food_des = {x[0]: x for x in food_des}
    nutrients = sql_nutrients_overview()
    rdas = {x[0]: x[1] for x in nutrients.values()}

    # --------------------------------------
    # Food-by-food analysis (w/ servings)
    # --------------------------------------
    servings_tables = []
    nutrients_tables = []
    for food_id in analyses:
        food_name = food_des[food_id][2]
        # food_name = food["long_desc"]
        print(
            "\n======================================\n"
            + "==> {0} ({1})\n".format(food_name, food_id)
            + "======================================\n"
        )
        print("\n=========================\nSERVINGS\n=========================\n")

        ###############
        # Serving table
        headers = ["msre_id", "msre_desc", "grams"]
        # Copy obj with dict(x)
        rows = [(x[1], x[2], x[3]) for x in serving if x[0] == food_id]
        # for r in rows:
        #     r.pop("food_id")
        # Print table
        servings_table = tabulate(rows, headers=headers, tablefmt="presto")
        print(servings_table)
        servings_tables.append(servings_table)

        refuse = next(
            ((x[7], x[8]) for x in food_des.values() if x[0] == food_id and x[7]), None
        )
        if refuse:
            print("\n=========================\nREFUSE\n=========================\n")
            print(refuse[0])
            print("    ({0}%, by mass)".format(refuse[1]))

        print("\n=========================\nNUTRITION\n=========================\n")

        ################
        # Nutrient table
        headers = ["id", "nutrient", "rda", "amount", "units"]
        rows = []
        # food_nutes = {x["nutr_id"]: x for x in food["nutrients"]}
        # for id, nute in food_nutes.items():
        for food_id_2, amount in analyses[food_id]:
            # Skip zero values
            # amount = food_nutes[id]["nutr_val"]
            if not amount:
                continue

            nutr_desc = (
                nutrients[food_id_2][4]
                if nutrients[food_id_2][4]
                else nutrients[food_id_2][3]
            )
            unit = nutrients[food_id_2][2]

            # Insert RDA % into row
            if rdas[food_id_2]:
                rda_perc = str(round(amount / rdas[food_id_2] * 100, 1)) + "%"
            else:
                # print(rdas[id])
                rda_perc = None
            row = [food_id_2, nutr_desc, rda_perc, round(amount, 2), unit]

            rows.append(row)

        # Print table
        table = tabulate(rows, headers=headers, tablefmt="presto")
        print(table)
        nutrients_tables.append(table)

    return nutrients_tables, servings_tables


def day_analyze(day_csv_paths, rda_csv_path=None, debug=False):
    """Analyze a day optionally with custom RDAs,
    e.g.  nutra day ~/.nutra/rocky.csv -r ~/.nutra/dog-rdas-18lbs.csv
    TODO: Should be a subset of foods_analyze
    """
    if rda_csv_path is not None:
        with open(rda_csv_path) as file_path:
            rda_csv_input = csv.DictReader(
                row for row in file_path if not row.startswith("#")
            )
            rdas = list(rda_csv_input)
    else:
        rdas = []

    logs = []
    food_ids = set()
    for day_csv_path in day_csv_paths:
        with open(day_csv_path) as file_path:
            rows = [row for row in file_path if not row.startswith("#")]
            day_csv_input = csv.DictReader(rows)
            log = list(day_csv_input)
        for entry in log:
            if entry["id"]:
                food_ids.add(int(entry["id"]))
        logs.append(log)

    # Inject user RDAs
    nutrients = [tuple(x) for x in sql_nutrients_overview().values()]
    for rda in rdas:
        nutrient_id = int(rda["id"])
        _rda = float(rda["rda"])
        for nutrient in nutrients:
            if nutrient[0] == nutrient_id:
                nutrient[1] = _rda
                if debug:
                    substr = "{0} {1}".format(_rda, nutrient[2]).ljust(12)
                    print("INJECT RDA: {0} -->  {1}".format(substr, nutrient[4]))
    nutrients = {x[0]: x for x in nutrients}

    # Analyze foods
    foods_analysis = {}
    for food in sql_analyze_foods(food_ids):
        food_id = food[0]
        anl = food[1], food[2]
        if food_id not in foods_analysis:
            foods_analysis[food_id] = [anl]
        else:
            foods_analysis[food_id].append(anl)

    # Compute totals
    nutrients_totals = []
    for log in logs:
        nutrient_totals = OrderedDict()
        for entry in log:
            if entry["id"]:
                food_id = int(entry["id"])
                grams = float(entry["grams"])
                for nutrient in foods_analysis[food_id]:
                    nutr_id = nutrient[0]
                    nutr_per_100g = nutrient[1]
                    nutr_val = grams / 100 * nutr_per_100g
                    if nutr_id not in nutrient_totals:
                        nutrient_totals[nutr_id] = nutr_val
                    else:
                        nutrient_totals[nutr_id] += nutr_val
        nutrients_totals.append(nutrient_totals)

    #######
    # Print
    term_width = shutil.get_terminal_size()[0]
    buffer = term_width - 4 if term_width > 4 else term_width
    for analysis in nutrients_totals:
        day_format(analysis, nutrients, buffer=buffer)
    return nutrients_totals


def day_format(analysis, nutrients, buffer=None):
    """Formats day analysis for printing to console"""

    def print_header(header):
        print(Fore.CYAN, end="")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("--> %s" % header)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(Style.RESET_ALL)

    def print_macro_bar(fat, net_carb, pro, kcals_max, buffer=None):
        kcals = fat * 9 + net_carb * 4 + pro * 4

        p_fat = (fat * 9) / kcals
        p_carb = (net_carb * 4) / kcals
        p_pro = (pro * 4) / kcals

        # TODO: handle rounding cases, tack on to, or trim off FROM LONGEST ?
        mult = kcals / kcals_max
        n_fat = round(p_fat * buffer * mult)
        n_carb = round(p_carb * buffer * mult)
        n_pro = round(p_pro * buffer * mult)

        # Headers
        f_buf = " " * (n_fat // 2) + "Fat" + " " * (n_fat - n_fat // 2 - 3)
        c_buf = " " * (n_carb // 2) + "Carbs" + " " * (n_carb - n_carb // 2 - 5)
        p_buf = " " * (n_pro // 2) + "Pro" + " " * (n_pro - n_pro // 2 - 3)
        print(
            "  "
            + Fore.YELLOW
            + f_buf
            + Fore.BLUE
            + c_buf
            + Fore.RED
            + p_buf
            + Style.RESET_ALL
        )

        # Bars
        print(" <", end="")
        print(Fore.YELLOW + "=" * n_fat, end="")
        print(Fore.BLUE + "=" * n_carb, end="")
        print(Fore.RED + "=" * n_pro, end="")
        print(Style.RESET_ALL + ">")

        # Calorie footers
        k_fat = str(round(fat * 9))
        k_carb = str(round(net_carb * 4))
        k_pro = str(round(pro * 4))
        f_buf = " " * (n_fat // 2) + k_fat + " " * (n_fat - n_fat // 2 - len(k_fat))
        c_buf = (
            " " * (n_carb // 2) + k_carb + " " * (n_carb - n_carb // 2 - len(k_carb))
        )
        p_buf = " " * (n_pro // 2) + k_pro + " " * (n_pro - n_pro // 2 - len(k_pro))
        print(
            "  "
            + Fore.YELLOW
            + f_buf
            + Fore.BLUE
            + c_buf
            + Fore.RED
            + p_buf
            + Style.RESET_ALL
        )

    def print_nute_bar(n_id, amount, nutrients):
        nutrient = nutrients[n_id]
        rda = nutrient[1]
        tag = nutrient[3]
        unit = nutrient[2]
        # anti = nutrient[5]

        if not rda:
            return False, nutrient
        attain = amount / rda
        perc = round(100 * attain, 1)

        if attain >= THRESH_OVER:
            color = COLOR_OVER
        elif attain <= THRESH_CRIT:
            color = COLOR_CRIT
        elif attain <= THRESH_WARN:
            color = COLOR_WARN
        else:
            color = COLOR_DEFAULT

        # Print
        detail_amount = "{0}/{1} {2}".format(round(amount, 1), rda, unit).ljust(18)
        detail_amount = "{0} -- {1}".format(detail_amount, tag)
        left_index = 20
        left_pos = round(left_index * attain) if attain < 1 else left_index
        print(" {0}<".format(color), end="")
        print("=" * left_pos + " " * (left_index - left_pos) + ">", end="")
        print(" {0}%\t[{1}]".format(perc, detail_amount), end="")
        print(Style.RESET_ALL)

        return True, perc

    # Actual values
    kcals = round(analysis[NUTR_ID_KCAL])
    pro = analysis[NUTR_ID_PROTEIN]
    net_carb = analysis[NUTR_ID_CARBS] - analysis[NUTR_ID_FIBER]
    fat = analysis[NUTR_ID_FAT_TOT]
    kcals_449 = round(4 * pro + 4 * net_carb + 9 * fat)

    # Desired values
    kcals_rda = round(nutrients[NUTR_ID_KCAL][1])
    pro_rda = nutrients[NUTR_ID_PROTEIN][1]
    net_carb_rda = nutrients[NUTR_ID_CARBS][1] - nutrients[NUTR_ID_FIBER][1]
    fat_rda = nutrients[NUTR_ID_FAT_TOT][1]

    # Print calories and macronutrient bars
    print_header("Macronutrients")
    kcals_max = max(kcals, kcals_rda)
    rda_perc = round(kcals * 100 / kcals_rda, 1)
    print(
        "Actual:    {0} kcal ({1}% RDA), {2} by 4-4-9".format(
            kcals, rda_perc, kcals_449
        )
    )
    print_macro_bar(fat, net_carb, pro, kcals_max, buffer=buffer)
    print(
        "\nDesired:   {0} kcal ({1} kcal)".format(
            kcals_rda, "%+d" % (kcals - kcals_rda)
        )
    )
    print_macro_bar(
        fat_rda,
        net_carb_rda,
        pro_rda,
        kcals_max,
        buffer=buffer,
    )

    # Nutrition detail report
    print_header("Nutrition detail report")
    for n_id in analysis:
        print_nute_bar(n_id, analysis[n_id], nutrients)
    # TODO: below
    print(
        "work in progress...some minor fields with negligible data, they are not shown here"
    )
