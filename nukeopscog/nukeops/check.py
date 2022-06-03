import sqlite3
import os


def database_exist(database_file):
    # Check if database exist,
    # if it's not, make one
    if os.path.exists(database_file):
        return True
    try:
        with sqlite3.connect(database_file) as conn:
            conn.execute("""
CREATE TABLE IF NOT EXISTS nicknames(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discord_name text NOT NULL,
    warframe_name text NOT NULL,
    affiliation text NOT NULL);""")
        return False
    except Exception as Error:
        print(Error)


def user_exist(name):
    # ctx.author
    db_file = 'warframe.db'
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                            SELECT * FROM nicknames
                            WHERE discord_name = '{name}' OR
                                 warframe_name = '{name}'
                            """)
            user = cursor.fetchall()
        if user:
            return True
        else: return False
    except sqlite3.OperationalError as Error:
        print(Error)
        return False


def user(name):
    db_file = 'warframe.db'
    # output = list()
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
                        SELECT * FROM nicknames
                        WHERE discord_name = '{name}' OR
                             warframe_name = '{name}'
                        """)
        output = [x for x in cursor.fetchall()]
    return output


def database(db):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name from sqlite_master where type= \"table\"")
        print("tables:\n", cursor.fetchall())
        cursor.execute("SELECT * FROM nicknames")
        print("columns:\n", "id | warframe | discord | aff")
        for row in cursor.fetchall():
            print(row)
