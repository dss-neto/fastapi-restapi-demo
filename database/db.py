from sqlite3 import connect


def get_connection():
    connection = connect("./database/main_database.db", check_same_thread=False)
    return connection
