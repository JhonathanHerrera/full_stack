from db import get_connection

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
        """)
        conn.commit()
        print("Table created!")

def insert_user(conn, name, email):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s);",
            (name, email)
        )
        conn.commit()
        print(f" Added user: {name}")

def show_users(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users;")
        rows = cur.fetchall()
        print("\n👥 All users:")
        for row in rows:
            print(row)

def update_user(conn, user_id, new_name):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE users SET name = %s WHERE id = %s;",
            (new_name, user_id)
        )
        conn.commit()
        print(f"Updated user ID {user_id} → {new_name}")

def delete_user(conn, user_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        print(f" Deleted user ID {user_id}")

def main():
    conn = get_connection()
    print(" Connected to PostgreSQL!")
    create_table(conn)

    insert_user(conn, "Jhonathan", "jhonatah@example.com")
    insert_user(conn, "Meow Meow", "meow@example.com")

    show_users(conn)

    update_user(conn, 1, "Aaron")

    delete_user(conn, 2)

    show_users(conn)

    conn.close()

if __name__ == "__main__":
    main()
