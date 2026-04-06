from psycopg2 import Error, sql


class UserRead:
    def __init__(self, user_email, table):
        self.user_email = user_email
        self.table = table

    def _fetchone(self, connection, query):
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (self.user_email,))
                return cursor.fetchone()
        except (Exception, Error) as error:
            print("Error while reading user data:", error)
            return None

    def read_password(self, connection):
        query = sql.SQL("SELECT password FROM {} WHERE email = %s").format(sql.Identifier(self.table))
        user = self._fetchone(connection, query)
        return user[0] if user else None

    def read_email(self, connection):
        query = sql.SQL("SELECT email FROM {} WHERE email = %s").format(sql.Identifier(self.table))
        user = self._fetchone(connection, query)
        return user[0] if user else None

    def read_id(self, connection):
        query = sql.SQL("SELECT id FROM {} WHERE email = %s").format(sql.Identifier(self.table))
        user = self._fetchone(connection, query)
        return user[0] if user else None

    def is_verified(self, connection):
        query = sql.SQL("SELECT verification_token FROM {} WHERE email = %s").format(
            sql.Identifier(self.table)
        )
        user = self._fetchone(connection, query)
        return bool(user and user[0] == "verified")

    def read(self, connection):
        query = sql.SQL("SELECT id, name, email FROM {} WHERE email = %s").format(sql.Identifier(self.table))
        return self._fetchone(connection, query)

    def read_profile(self, connection):
        user = self.read(connection)
        if user:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
        else:
            print("User not found.")
