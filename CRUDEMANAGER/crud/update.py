import psycopg2
from psycopg2 import Error

class edituser:
    def __init__(self, user_id, action, new_edition, table):
        self.user_id = user_id
        self.action = action
        self.new_edition = new_edition
        self.table = table


    def edit(self, connection):
        try:
            cursor = connection.cursor()
            update_query = f"UPDATE {self.table} SET {self.action} = %s WHERE id = %s"
            cursor.execute(update_query, (self.new_edition, self.user_id))
            connection.commit()
            print("Usuário editado com sucesso!")
        except (Exception, Error) as error:
            print("Error while editing user", error)
