import psycopg2
from psycopg2 import Error

class userdelete:
    def __init__(self, user_id, table):
        self.user_id = user_id
        self.table = table

    def delete(self, connection):
        try:
            cursor = connection.cursor()
            delete_query = "DELETE FROM %s WHERE id = %s"
            cursor.execute(delete_query, (self.table, self.user_id,))
            connection.commit()
            print("Usuário deletado com sucesso!")
        except (Exception, Error) as error:
            print("Error while deleting user", error)