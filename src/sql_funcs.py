import sqlite3

def safeInsert(
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