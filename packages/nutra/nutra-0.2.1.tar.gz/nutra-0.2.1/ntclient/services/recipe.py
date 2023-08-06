#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:14:00 2020

@author: shane
"""

from tabulate import tabulate

from ntclient.persistence.sql.nt.funcs import (
    sql_analyze_recipe,
    sql_recipe,
    sql_recipes,
)
from ntclient.persistence.sql.usda.funcs import (
    sql_analyze_foods,
    sql_food_details,
    sql_nutrients_overview,
)
from ntclient.utils.nutprogbar import nutprogbar


def recipes_overview():
    """Shows overview for all recipes"""
    recipes = sql_recipes()[1]

    results = []
    for recipe in recipes:
        result = {
            "id": recipe[0],
            "name": recipe[2],
            "tagname": recipe[1],
            "n_foods": recipe[3],
            "weight": recipe[4],
        }
        results.append(result)

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)
    return results


def recipe_overview(recipe_id):
    """Shows single recipe overview"""
    recipe = sql_analyze_recipe(recipe_id)
    name = recipe[0][1]
    print(name)

    food_ids = {x[2]: x[3] for x in recipe}
    food_names = {x[0]: x[3] for x in sql_food_details(food_ids.keys())}
    food_analyses = sql_analyze_foods(food_ids.keys())

    table = tabulate(
        [[food_names[food_id], grams] for food_id, grams in food_ids.items()],
        headers=["food", "g"],
    )
    print(table)
    # tabulate nutrient RDA %s
    nutrients = sql_nutrients_overview()
    # rdas = {x[0]: x[1] for x in nutrients.values()}
    progbars = nutprogbar(food_ids, food_analyses, nutrients)
    print(progbars)

    return recipe


def recipe_add(name, food_amts):
    """Add a recipe to SQL database"""
    print()
    print("New recipe: " + name + "\n")

    food_names = {x[0]: x[2] for x in sql_food_details(food_amts.keys())}

    results = []
    for food_id, grams in food_amts.items():
        results.append([food_id, food_names[food_id], grams])

    table = tabulate(results, headers=["id", "food_name", "grams"], tablefmt="presto")
    print(table)

    confirm = input("\nCreate recipe? [Y/n] ")

    if confirm.lower() == "y":
        print("not implemented ;]")


def recipe_edit(recipe_id):
    """Edit recipe in SQL database"""
    recipe = sql_recipe(recipe_id)[0]

    # TODO: use Row dict? con.row_factory = sqlite3.Row
    print(recipe[4])
    confirm = input("Do you wish to edit? [Y/n] ")

    if confirm.lower() == "y":
        print("not implemented ;]")


def recipe_delete(recipe_id):
    """Deletes recipe by ID, along with any FK constraints"""
    recipe = sql_recipe(recipe_id)[0]

    print(recipe[4])
    confirm = input("Do you wish to delete? [Y/n] ")

    if confirm.lower() == "y":
        print("not implemented ;]")
