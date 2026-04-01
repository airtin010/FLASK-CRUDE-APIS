import psycopg2
from psycopg2 import Error
from werkzeug.security import generate_password_hash

class edituser:
    def __init__(self, user_id, action, new_edition, table):
        self.user_id = user_id
        self.action = action
        self.new_edition = new_edition
        self.table = table


    def edit(self, connection):
        if self.action == "password":
            self.new_edition = generate_password_hash(self.new_edition) # Faz o hash da nova senha para segurança
        try:
            cursor = connection.cursor()
            update_query = f"UPDATE {self.table} SET {self.action} = %s WHERE id = %s"
            cursor.execute(update_query, (self.new_edition, self.user_id))
            connection.commit()
            print("Usuário editado com sucesso!")
        except (Exception, Error) as error:
            print("Error while editing user", error)
