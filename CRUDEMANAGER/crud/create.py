import psycopg2
from psycopg2 import Error
from werkzeug.security import generate_password_hash

class UserAdd:
    def __init__(self, name, email, password, table):
        self.name = name
        self.email = email
        self.password = password
        self.table = table

    def add(self, connection):
        try:
            cursor = connection.cursor()
            hashed_password = generate_password_hash(self.password)
            insert_query = f"INSERT INTO {self.table} (name, email, password, verification_token) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (self.name, self.email, hashed_password, 'not_verified'))
            connection.commit()
            print("User added successfully!")
        except (Exception, Error) as error:
            print("Error while adding user:", error)