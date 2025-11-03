# File: Swasthify/backend/db.py

import psycopg2
import psycopg2.extras
import os

# --- SET YOUR DATABASE CONNECTION DETAILS HERE ---
DB_HOST = "localhost"
DB_NAME = "swasthify"
DB_USER = "swasthify_admin"
DB_PASS = "kholna"
# --------------------------------------------------

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_dict_cursor(conn):
    """Returns a dictionary cursor to fetch rows as dicts."""
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)