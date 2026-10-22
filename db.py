import streamlit as st
import psycopg2


def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"]
    )


def create_users_table():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        connection.commit()
        cursor.close()

    finally:
        connection.close()


def add_user(name, email, password_hash):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s);
            """,
            (name, email, password_hash)
        )

        connection.commit()
        return True

    except psycopg2.IntegrityError:
        connection.rollback()
        return False

    finally:
        connection.close()


def get_user(email):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, email, password_hash
            FROM users
            WHERE email = %s;
            """,
            (email,)
        )

        user = cursor.fetchone()
        cursor.close()

        return user

    finally:
        connection.close()