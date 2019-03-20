import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE_PORT = 5433
DATABASE_NAME = "postgres"
USERNAME = "postgres"
PASSWORD = "postgres"
TABLE_NAME = "tracking"

TIMESTAMP = "timestamp"
UUID = "uuid"
TYPE = "type"
VALUE = "value"


cursor = None


def open_connection(host):
    global cursor
    try:
        conn = psycopg2.connect(host=host, dbname=DATABASE_NAME, user=USERNAME, password=PASSWORD)
        print "Connected to the database successfully."
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return True
    except:
        print "Unable to open connection to database. Retrying..."
        return False


def create_table_if_not_exits():
    cursor.execute("CREATE TABLE IF NOT EXISTS tracking ("
                   "uuid                   varchar(100) PRIMARY KEY, "                   
                   "timestamp              TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, "
                   "type                   VARCHAR(30) NOT NULL, "
                   "value                  TEXT);") # thinking about JSON


def insert_data(data_array):
    for data in data_array:
        print "Data: " + str(data)

        uuid = data[UUID]
        timestamp = data[TIMESTAMP]
        type = data[TYPE]
        value = data[VALUE]

        cursor.execute("INSERT INTO {0} ({1}, {2}, {3}, {4}) VALUES ('{5}', '{6}', '{7}', '{8}');"
                    .format(TABLE_NAME, UUID, TIMESTAMP, TYPE, VALUE, uuid, timestamp, type, value))


def get_data_array():
    cursor.execute("SELECT * FROM {}".format(TABLE_NAME))
    return cursor.fetchall()

