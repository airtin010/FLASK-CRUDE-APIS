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


def conectar():
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE
        )

        print("Conexão com PostgreSQL bem-sucedida!")
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None
    
connection = conectar()

def createtable(connection, tablename):
    try:
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS %s (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        );
        '''
        cursor.execute(create_table_query % tablename)
        connection.commit()
        print("Tabela '%s' criada com sucesso!" % tablename )
    except (Exception, Error) as error:
        print("Error while creating table", error)

def deletetable(connection, tablename):
    try:
        cursor = connection.cursor()
        delete_table_query = "DROP TABLE IF EXISTS %s;"
        cursor.execute(delete_table_query % tablename)
        connection.commit()
        print("Tabela '%s' deletada com sucesso!" % tablename)
    except (Exception, Error) as error:
        print("Error while deleting table", error)

def showtables(connection, x=0):
    if x == 1:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            tables = cursor.fetchall()
            print("Tabelas no banco de dados:")
            for table in tables:
                print(table[0])
            return tables
        except (Exception, Error) as error:
            print("Error while fetching tables", error)
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            tables = cursor.fetchall()
            return tables
        except (Exception, Error) as error:
            print("Error while fetching tables", error)


def tablecontent(connection, tablename):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s;" % tablename)
        table = cursor.fetchall()
        print("Conteúdo da tabela '%s':" % tablename)
        for content in table:
            print(content)
    except (Exception, Error) as error:
        print("Error while fetching table content", error)


def chosetable():
    print("Escolha uma tabela:")
    n = 1 
    for x in showtables(connection):
        print(f"digite {n} para tabela {x[0]}")
        n += 1
    inp = input("s para sair")
    if inp != "s":
        try:
            ta = showtables(connection)
            c = ta[(int(inp)-1)][0]
            return c
        except Error:
            print(Error)
    else:
        print("saindo...")

