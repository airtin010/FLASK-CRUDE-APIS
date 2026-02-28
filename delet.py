import psycopg2
from psycopg2 import Error

class userdelete:
    def __init__(self, user_id):
        self.user_id = user_id

    def delete(self, connection):
        try:
            cursor = connection.cursor()
            delete_query = "DELETE FROM users WHERE id = %s"
            cursor.execute(delete_query, (self.user_id,))
            connection.commit()
            print("Usuário deletado com sucesso!")
        except (Exception, Error) as error:
            print("Error while deleting user", error)