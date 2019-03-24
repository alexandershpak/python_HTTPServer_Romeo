import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    global conn
    try:
        conn = sqlite3.connect(db_file)
        print("created connection to db")
        print("sqlite version " + sqlite3.version)
        return True
    except Error as e:
        print(e)
        return False
    finally:
        conn.close()


# if __name__ == '__main__':
#     create_connection("/root/sqlite/db/pythonsqlite.db")