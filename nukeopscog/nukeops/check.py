import sqlite3
import os

def create_db(database_file):
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
CREATE TABLE IF NOT EXISTS nicknames(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discord_name text NOT NULL,
    warframe_name text NOT NULL,
    affiliation text NOT NULL);""")

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
