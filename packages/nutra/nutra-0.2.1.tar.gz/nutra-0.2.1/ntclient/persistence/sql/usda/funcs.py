"""usda.sqlite functions module"""
from ntclient.persistence.sql.usda import _sql

# ----------------------
# USDA  functions
# ----------------------


def sql_fdgrp():
    """Shows food groups"""
    query = "SELECT * FROM fdgrp;"
    result = _sql(query)
    return {x[0]: x for x in result}


def sql_food_details(food_ids):
    """Readable human details for foods"""
    query = "SELECT * FROM food_des WHERE id IN (%s)"
    food_ids = ",".join(str(x) for x in set(food_ids))
    return _sql(query % food_ids)


def sql_nutrients_overview():
    """Shows nutrients overview"""
    query = "SELECT * FROM nutrients_overview;"
    result = _sql(query)
    return {x[0]: x for x in result}


def sql_nutrients_details():
    """Shows nutrients 'details'"""
    query = "SELECT * FROM nutrients_overview;"
    return _sql(query, headers=True)


def sql_servings(food_ids):
    """Food servings"""
    # TODO: apply connective logic from `sort_foods()` IS ('None') ?
    query = """
SELECT
  serv.food_id,
  serv.msre_id,
  serv_desc.msre_desc,
  serv.grams
FROM
  serving serv
  LEFT JOIN serv_desc ON serv.msre_id = serv_desc.id
WHERE
  serv.food_id IN (%s);
"""
    food_ids = ",".join(str(x) for x in set(food_ids))
    return _sql(query % food_ids)


def sql_analyze_foods(food_ids):
    """Nutrient analysis for foods"""
    query = """
SELECT
  id,
  nutr_id,
  nutr_val
FROM
  food_des
  INNER JOIN nut_data ON food_des.id = nut_data.food_id
WHERE
  food_des.id IN (%s);
"""
    food_ids = ",".join(str(x) for x in set(food_ids))
    return _sql(query % food_ids)


def sql_sort_foods(nutr_id):
    """Sort foods by nutr_id per 100 g"""
    query = """
SELECT
  nut_data.food_id,
  fdgrp_id,
  nut_data.nutr_val,
  kcal.nutr_val AS kcal,
  long_desc
FROM
  nut_data
  INNER JOIN food_des food ON food.id = nut_data.food_id
  INNER JOIN nutr_def ndef ON ndef.id = nut_data.nutr_id
  INNER JOIN fdgrp ON fdgrp.id = fdgrp_id
  LEFT JOIN nut_data kcal ON food.id = kcal.food_id
    AND kcal.nutr_id = 208
WHERE
  nut_data.nutr_id = %s
ORDER BY
  nut_data.nutr_val DESC;
"""
    return _sql(query % nutr_id)


def sql_sort_foods_by_kcal(nutr_id):
    """Sort foods by nutr_id per 200 kcal"""
    query = """
SELECT
  nut_data.food_id,
  fdgrp_id,
  ROUND((nut_data.nutr_val * 200 / kcal.nutr_val), 2) AS nutr_val,
  kcal.nutr_val AS kcal,
  long_desc
FROM
  nut_data
  INNER JOIN food_des food ON food.id = nut_data.food_id
  INNER JOIN nutr_def ndef ON ndef.id = nut_data.nutr_id
  INNER JOIN fdgrp ON fdgrp.id = fdgrp_id
  -- filter out NULL kcal
  INNER JOIN nut_data kcal ON food.id = kcal.food_id
    AND kcal.nutr_id = 208
    AND kcal.nutr_val > 0
WHERE
  nut_data.nutr_id = %s
ORDER BY
  (nut_data.nutr_val / kcal.nutr_val) DESC;
"""
    return _sql(query % nutr_id)
