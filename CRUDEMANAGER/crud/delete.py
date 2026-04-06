from psycopg2 import Error, sql


class UserDelete:
    def __init__(self, user_id, table):
        self.user_id = user_id
        self.table = table

    def delete(self, connection):
        if not connection:
            return

        try:
            query = sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(self.table))

            with connection.cursor() as cursor:
                cursor.execute(query, (self.user_id,))

            connection.commit()
            print("User deleted successfully!")
        except (Exception, Error) as error:
            connection.rollback()
            print("Error while deleting user:", error)
