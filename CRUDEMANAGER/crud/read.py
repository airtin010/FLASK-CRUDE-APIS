import psycopg2
from psycopg2 import Error

class UserRead:
    def __init__(self, user_email, table):
        self.user_email = user_email
        self.table = table

    def read_password(self, connection):
        try:
            cursor = connection.cursor()
            select_query = f"SELECT password FROM {self.table} WHERE email = %s"
            cursor.execute(select_query, (self.user_email,))
            user = cursor.fetchone()
            return user[0] if user else None
        except (Exception, Error) as error:
            print("Error while reading user password:", error)
            return None

    def read_email(self, connection):
        try:
            cursor = connection.cursor()
            select_query = f"SELECT email FROM {self.table} WHERE email = %s"
            cursor.execute(select_query, (self.user_email,))
            user = cursor.fetchone()
            return user[0] if user else None
        except (Exception, Error) as error:
            print("Error while reading user email:", error)
            return None
        
    def read_id(self, connection):
        try:
            cursor = connection.cursor()
            select_query = f"SELECT id FROM {self.table} WHERE email = %s"
            cursor.execute(select_query, (self.user_email,))
            user = cursor.fetchone()
            return user[0] if user else None
        except (Exception, Error) as error:
            print("Error while reading user ID:", error)
            return None
        
    def is_verified(self, connection):
        try:
            cursor = connection.cursor()
            select_query = f"SELECT verification_token FROM {self.table} WHERE email = %s"
            cursor.execute(select_query, (self.user_email,))
            user = cursor.fetchone()
            return True if user and user[0] == 'verified' else False
        except (Exception, Error) as error:
            print("Error while checking verification status:", error)
            return False

    def read_profile(self, connection):
        try:
            cursor = connection.cursor()
            select_query = f"SELECT id, name, email FROM {self.table} WHERE email = %s"
            cursor.execute(select_query, (self.user_email,))
            user = cursor.fetchone()
            if user:
                print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
            else:
                print("User not found.")
        except (Exception, Error) as error:
            print("Error while reading user profile:", error)