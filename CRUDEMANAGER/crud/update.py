from psycopg2 import Error, sql
from werkzeug.security import generate_password_hash


class UserEdit:
    def __init__(self, user_id, column_name, new_value, table):
        self.user_id = user_id
        self.column_name = column_name
        self.new_value = new_value
        self.table = table

    def update(self, connection):
        if not connection:
            return

        if self.column_name == "password":
            self.new_value = generate_password_hash(self.new_value)

        try:
            query = sql.SQL("UPDATE {} SET {} = %s WHERE id = %s").format(
                sql.Identifier(self.table),
                sql.Identifier(self.column_name),
            )

            with connection.cursor() as cursor:
                cursor.execute(query, (self.new_value, self.user_id))

            connection.commit()
            print("User updated successfully!")
        except (Exception, Error) as error:
            connection.rollback()
            print("Error while updating user:", error)
