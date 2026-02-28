import psycopg2
from psycopg2 import Error

class useradd:
    def __init__(self, name, email, password,table):
        self.name = name
        self.email = email
        self.password = password
        self.table = table

    def add(self, connection):
        try:
            cursor = connection.cursor()
            insert_query = f"INSERT INTO {self.table} (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (self.name, self.email, self.password))
            connection.commit()
            print("Usuário adicionado com sucesso!")
        except (Exception, Error) as error:
            print("Error while adding user", error) 