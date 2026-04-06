from psycopg2 import Error, sql
from werkzeug.security import generate_password_hash


class UserAdd:
    def __init__(self, name, email, password, table):
        self.name = name
        self.email = email
        self.password = password
        self.table = table

    def add(self, connection):
        if not connection:
            return

        try:
            hashed_password = generate_password_hash(self.password)

            query = sql.SQL(
                "INSERT INTO {} (name, email, password, verification_token) VALUES (%s, %s, %s, %s)"
            ).format(sql.Identifier(self.table))

            with connection.cursor() as cursor:
                cursor.execute(query, (self.name, self.email, hashed_password, "not_verified"))

            connection.commit()
            print("User added successfully!")
        except (Exception, Error) as error:
            connection.rollback()
            print("Error while adding user:", error)
