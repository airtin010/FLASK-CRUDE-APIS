from maindefs import connect, create_table, delete_table, show_tables, get_table_content, choose_table
from crud.create import UserAdd
from crud.update import UserEdit
from crud.delete import UserDelete
from crud.read import UserRead

EDITABLE_FIELDS = {"name", "email", "password"}


def show_menu():
    print("\n--- CRUDEMANAGER System ---")
    print("1. Create Table")
    print("2. Delete Table")
    print("3. List All Tables")
    print("4. View Table Content")
    print("5. Add User")
    print("6. Edit User")
    print("7. Delete User")
    print("8. Read User (by Email)")
    print("s. Exit")


def handle_create_table(connection):
    name = input("Enter table name to create (or 's' to cancel): ").strip()
    if name and name != "s":
        create_table(connection, name)


def handle_delete_table(connection):
    table = choose_table(connection)
    if table:
        delete_table(connection, table)


def handle_show_table_content(connection):
    table = choose_table(connection)
    if table:
        get_table_content(connection, table)


def handle_add_user(connection):
    table = choose_table(connection)
    if not table:
        return

    name = input("User Name: ").strip()
    email = input("User Email: ").strip()
    password = input("User Password: ")
    UserAdd(name, email, password, table).add(connection)


def handle_edit_user(connection):
    table = choose_table(connection)
    if not table:
        return

    user_id = input("User ID to edit: ").strip()
    while True:
        column = input("Field to edit (name, email, or password): ").strip().lower()
        if column in EDITABLE_FIELDS:
            value = input(f"Enter new {column}: ")
            UserEdit(user_id, column, value, table).update(connection)
            return
        print("Invalid field. Use 'name', 'email', or 'password'.")


def handle_delete_user(connection):
    table = choose_table(connection)
    if not table:
        return

    try:
        user_id = int(input("User ID to delete: "))
        UserDelete(user_id, table).delete(connection)
    except ValueError:
        print("Error: ID must be a number.")


def handle_read_user(connection):
    table = choose_table(connection)
    if not table:
        return

    email = input("Enter email to search: ").strip()
    user = UserRead(email, table).read(connection)
    if user:
        print(f"User Data: {user}")
    else:
        print("User not found.")


def main():
    connection = connect()
    if not connection:
        print("Failed to establish database connection. Exiting...")
        return

    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip().lower()

        if choice == "1":
            handle_create_table(connection)
        elif choice == "2":
            handle_delete_table(connection)
        elif choice == "3":
            show_tables(connection)
        elif choice == "4":
            handle_show_table_content(connection)
        elif choice == "5":
            handle_add_user(connection)
        elif choice == "6":
            handle_edit_user(connection)
        elif choice == "7":
            handle_delete_user(connection)
        elif choice == "8":
            handle_read_user(connection)
        elif choice == "s":
            connection.close()
            print("Connection closed. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
