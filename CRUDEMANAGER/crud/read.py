from multiprocessing.dummy import connection

import psycopg2
from psycopg2 import Error


class readuser:
    def __init__(self, user_email, table):
        self.user_email = user_email
        self.table = table

    def readpassword(self, connection):
        try:
            cursor = connection.cursor()
            select_query = f"SELECT password FROM {self.table} WHERE email = %s"
            cursor.execute(select_query, (self.user_email,))
            user = cursor.fetchone()
            if user:
                return user[0]
            else:
                return None
        except (Exception, Error) as error:
            print("Error while reading user", error)
            return None

    def reademail(self, connection):
        try:
            cursor = connection.cursor()
            select_query = f"SELECT email FROM {self.table} WHERE email = %s"
            cursor.execute(select_query, (self.user_email,))
            user = cursor.fetchone()
            if user:
                return user[0]
            else:
                return None
        except (Exception, Error) as error:
            print("Error while reading user", error)
            return None

    def read(self, connection):
        try:
            cursor = connection.cursor()
            select_query = f"SELECT id, name, email FROM {self.table} WHERE email = %s"
            cursor.execute(select_query, (self.user_email,))
            user = cursor.fetchone()
            if user:
                print("ID: %s, Name: %s, Email: %s" % (user[0], user[1], user[2]))
            else:
                print("Usuário não encontrado.")
        except (Exception, Error) as error:
            print("Error while reading user", error)