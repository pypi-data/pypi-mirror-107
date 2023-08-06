"""Main SQL persistence module, need to rethink circular imports and shared code"""


def sql_entries(sql_result, headers=False):
    """Formats and returns an sql_result for console digestion and output"""
    rows = sql_result.fetchall()
    if headers:
        headers = [x[0] for x in sql_result.description]
        return headers, rows
    return rows


def close_con_and_cur(con, cur, commit=True):
    """Cleans up after a command is run"""
    cur.close()
    if commit:
        con.commit()
    con.close()
