import os 
import psycopg2
from dotenv import load_dotenv
from psycopg2 import Error

load_dotenv()   

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
        print("PostgreSQL connection successful!")
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None
    
connection = connect()

def create_table(connection, table_name):
    try:
        cursor = connection.cursor()
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password TEXT NOT NULL,
            verification_token TEXT
        );
        '''
        cursor.execute(create_table_query)
        cursor.execute(f"ALTER TABLE {table_name} ALTER COLUMN password TYPE TEXT;")
        connection.commit()
        print(f"Table '{table_name}' created successfully!")
    except (Exception, Error) as error:
        print("Error while creating table:", error)

def delete_table(connection, table_name):
    try:
        cursor = connection.cursor()
        delete_table_query = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(delete_table_query)
        connection.commit()
        print(f"Table '{table_name}' deleted successfully!")
    except (Exception, Error) as error:
        print("Error while deleting table:", error)

def show_tables(connection, verbose=0):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()
        if verbose == 1:
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        return tables
    except (Exception, Error) as error:
        print("Error while fetching tables:", error)
        return []

def get_table_content(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        print(f"Content of table '{table_name}':")
        for row in rows:
            print(row)
    except (Exception, Error) as error:
        print("Error while fetching table content:", error)

def choose_table():
    while True:
        print("\nChoose a table:")
        tables = show_tables(connection)

        for i, table in enumerate(tables, start=1):
            print(f"{i} → {table[0]}")
        print("0 → Exit")

        choice = input("Enter the table number (or 0 to exit): ")

        try:
            option = int(choice)

            if option == 0:
                return None
            if 1 <= option <= len(tables):
                return tables[option - 1][0]
            else:
                print("Invalid number. Please try again.\n")
        except ValueError:
            print("Please enter numbers only!\n")