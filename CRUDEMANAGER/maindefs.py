import os 
import psycopg2
from dotenv import load_dotenv
from psycopg2 import Error
import re

load_dotenv()   

# Database Configuration from Environment Variables
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")
DB_USER = os.getenv("DB_USER")

def connect():
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE
        )
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None

def create_table(connection, table_name):
    try:
        cursor = connection.cursor()
        # Added 'verified' column for compatibility with the Flask App
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password TEXT NOT NULL,
            verified BOOLEAN DEFAULT FALSE,
            verification_token TEXT
        );
        '''
        cursor.execute(query)
        connection.commit()
        print(f"Table '{table_name}' verified/created successfully.")
    except (Exception, Error) as error:
        print("Error while creating table:", error)

def delete_table(connection, table_name):
    if not table_name: return
    try:
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        connection.commit()
        print(f"Table '{table_name}' deleted successfully.")
    except (Exception, Error) as error:
        print("Error while deleting table:", error)

def show_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()
        print("\nTables in database:")
        for table in tables:
            print(f"- {table[0]}")
        return tables
    except (Exception, Error) as error:
        print("Error while fetching tables:", error)
        return []

def get_table_content(connection, table_name):
    if not table_name: return
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
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
    if len(password) < 12:
        return False, "Password must be at least 12 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[ !@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, "Strong password."