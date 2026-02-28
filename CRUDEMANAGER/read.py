import psycopg2
from psycopg2 import Error


class readuser:
    def __init__(self, user_id):
        self.user_id = user_id

    def read(self, connection):
        try:
            cursor = connection.cursor()
            select_query = "SELECT id, name, email FROM users WHERE id = %s"
            cursor.execute(select_query, (self.user_id,))
            user = cursor.fetchone()
            if user:
                print("ID: %s, Name: %s, Email: %s" % (user[0], user[1], user[2]))
            else:
                print("Usuário não encontrado.")
        except (Exception, Error) as error:
            print("Error while reading user", error)

