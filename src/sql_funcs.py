import sqlite3

def safe_insert(
    cursor: sqlite3.Cursor,
    table: str,
    data_dict: dict
) -> None:

    # in the future delete old question if question is already inside

    # execute insert query
    cursor.execute(
    f"""
    INSERT INTO {table} ({', '.join(data_dict.keys())}) 
    VALUES ({', '.join("?" for itm in data_dict)});
    """, tuple(data_dict.values()))

def safe_select(
    cursor: sqlite3.Cursor,
    table: str,
    select_dict: dict
) -> list:

    # execute select query
    cursor.execute(
    f"""
    SELECT * FROM {table} WHERE {' AND '.join(f'{itm} = ?' for itm in select_dict)}
    """, tuple(select_dict.values())
    )

    # get rows
    rows = cursor.fetchall()

    return rows