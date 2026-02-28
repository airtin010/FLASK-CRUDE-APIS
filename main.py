import os 
import psycopg2
from dotenv import load_dotenv
from psycopg2 import Error

from add import useradd
from edit import edituser
from delet import userdelete

load_dotenv()   

PASSWORD = os.getenv("PASSWORD")

def conectar():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password=PASSWORD,
            host="localhost",
            port="5432",
            database="postgres"
        )

        print("Conexão com PostgreSQL bem-sucedida!")
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None

def createtable(connection):
    try:
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        );
        '''
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabela 'users' criada com sucesso!")
    except (Exception, Error) as error:
        print("Error while creating table", error)

def showtables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()
        print("Tabelas no banco de dados:")
        for table in tables:
            print(table[0])
    except (Exception, Error) as error:
        print("Error while fetching tables", error)

def usertableconteudo(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        print("Conteúdo da tabela 'users':")
        for user in users:
            print(user)
    except (Exception, Error) as error:
        print("Error while fetching users", error)

if __name__ == "__main__":
    connection = conectar()
    if connection:
        createtable(connection)
        usertableconteudo(connection)