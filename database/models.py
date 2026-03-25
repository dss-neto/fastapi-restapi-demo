# models is the file where tables are created

from database.db import get_connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_list (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        title TEXT NOT NULL,
        description TEXT,
        is_checked INTEGER NOT NULL DEFAULT 0
    )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_database (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        hashed_password TEXT NOT NULL
    )""")

    cursor.execute("""
        ALTER TABLE task_list
        ADD owner_user_id INTEGER 
        """)

    connection.commit()
    connection.close()
