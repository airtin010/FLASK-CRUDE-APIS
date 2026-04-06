import re
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import Error, sql

load_dotenv()

# Database Configuration from Environment Variables
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")
DB_USER = os.getenv("DB_USER")

def connect():
    try:
        return psycopg2.connect(
            user=DB_USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE
        )
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None


def create_table(connection, table_name):
    if not connection or not table_name:
        return

    try:
        with connection.cursor() as cursor:
            query = sql.SQL(
                """
                CREATE TABLE IF NOT EXISTS {} (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    verified BOOLEAN DEFAULT FALSE,
                    verification_token TEXT
                );
                """
            ).format(sql.Identifier(table_name))
            cursor.execute(query)
        connection.commit()
        print(f"Table '{table_name}' verified/created successfully.")
    except (Exception, Error) as error:
        connection.rollback()
        print("Error while creating table:", error)


def delete_table(connection, table_name):
    if not connection or not table_name:
        return

    try:
        with connection.cursor() as cursor:
            query = sql.SQL("DROP TABLE IF EXISTS {};").format(sql.Identifier(table_name))
            cursor.execute(query)
        connection.commit()
        print(f"Table '{table_name}' deleted successfully.")
    except (Exception, Error) as error:
        connection.rollback()
        print("Error while deleting table:", error)


def show_tables(connection):
    if not connection:
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
            )
            tables = cursor.fetchall()

        print("\nTables in database:")
        for table in tables:
            print(f"- {table[0]}")
        return tables
    except (Exception, Error) as error:
        print("Error while fetching tables:", error)
        return []


def get_table_content(connection, table_name):
    if not connection or not table_name:
        return

    try:
        with connection.cursor() as cursor:
            query = sql.SQL("SELECT * FROM {};").format(sql.Identifier(table_name))
            cursor.execute(query)
            rows = cursor.fetchall()

        print(f"\nContent of table '{table_name}':")
        for row in rows:
            print(row)
    except (Exception, Error) as error:
        print("Error while fetching table content:", error)


def choose_table(connection):
    try:
        tables = show_tables(connection)
        if not tables:
            print("No tables found.")
            return None

        print("\nSelect a table:")
        for i, table in enumerate(tables, start=1):
            print(f"{i} → {table[0]}")
        print("0 → Cancel")

        choice = input("Selection: ")
        option = int(choice)

        if option == 0:
            return None
        if 1 <= option <= len(tables):
            return tables[option - 1][0]
        
        print("Invalid selection.")
        return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def is_password_strong(password):
    checks = (
        (len(password) >= 12, "Password must be at least 12 characters long."),
        (bool(re.search(r"[A-Z]", password)), "Password must contain at least one uppercase letter."),
        (bool(re.search(r"[a-z]", password)), "Password must contain at least one lowercase letter."),
        (bool(re.search(r"\d", password)), "Password must contain at least one number."),
        (
            bool(re.search(r"[ !@#$%^&*(),.?\":{}|<>]", password)),
            "Password must contain at least one special character.",
        ),
    )

    for is_valid, error_message in checks:
        if not is_valid:
            return False, error_message

    return True, "Strong password."
