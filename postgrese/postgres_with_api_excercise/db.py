
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        cursor_factory=RealDictCursor
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id SERIAL PRIMARY KEY,
            site TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_password(site, username, password):
    print("Connected")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO passwords (site, username, password)
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (site, username, password))
    new_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    print("added")
    return new_id

def get_password(site):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM passwords WHERE site = %s;", (site,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def update_password(site, new_password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE passwords SET password = %s WHERE site = %s RETURNING *;
    """, (new_password, site))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return updated
