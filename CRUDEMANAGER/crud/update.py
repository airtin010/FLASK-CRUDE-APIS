import psycopg2
from psycopg2 import Error
from werkzeug.security import generate_password_hash

class UserEdit:
    def __init__(self, user_id, column_name, new_value, table):
        self.user_id = user_id
        self.column_name = column_name
        self.new_value = new_value
        self.table = table

    def update(self, connection):
        if self.column_name == "password":
            self.new_value = generate_password_hash(self.new_value)
            
        try:
            cursor = connection.cursor()
            update_query = f"UPDATE {self.table} SET {self.column_name} = %s WHERE id = %s"
            cursor.execute(update_query, (self.new_value, self.user_id))
            connection.commit()
            print("User updated successfully!")
        except (Exception, Error) as error:
            print("Error while updating user:", error)