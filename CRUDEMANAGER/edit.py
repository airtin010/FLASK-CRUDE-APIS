import psycopg2
from psycopg2 import Error

class edituser:
    def __init__(self, user_id, new_name, new_email, new_password):
        self.user_id = user_id
        self.new_name = new_name
        self.new_email = new_email
        self.new_password = new_password

    def edit(self, connection):
        try:
            cursor = connection.cursor()
            update_query = "UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s"
            cursor.execute(update_query, (self.new_name, self.new_email, self.new_password, self.user_id))
            connection.commit()
            print("Usuário editado com sucesso!")
        except (Exception, Error) as error:
            print("Error while editing user", error)
