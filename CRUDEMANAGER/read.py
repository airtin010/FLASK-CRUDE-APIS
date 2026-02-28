import psycopg2
from psycopg2 import Error


class readuser:
    def __init__(self, user_id, table):
        self.user_id = user_id
        self.table = table

    def read(self, connection):
        try:
            cursor = connection.cursor()
            select_query = f"SELECT id, name, email FROM {self.table} WHERE id = %s"
            cursor.execute(select_query, (self.user_id,))
            user = cursor.fetchone()
            if user:
                print("ID: %s, Name: %s, Email: %s" % (user[0], user[1], user[2]))
            else:
                print("Usuário não encontrado.")
        except (Exception, Error) as error:
            print("Error while reading user", error)

