import psycopg2
from psycopg2 import Error

class UserDelete:
    def __init__(self, user_id, table):
        self.user_id = user_id
        self.table = table

    def delete(self, connection):
        try:
            cursor = connection.cursor()
            delete_query = f"DELETE FROM {self.table} WHERE id = %s"
            cursor.execute(delete_query, (self.user_id,))
            connection.commit()
            print("User deleted successfully!")
        except (Exception, Error) as error:
            print("Error while deleting user:", error)