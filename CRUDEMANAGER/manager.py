from maindefs import connect, create_table, delete_table, show_tables, get_table_content, choose_table
from crud.create import UserAdd
from crud.update import UserEdit
from crud.delete import UserDelete
from crud.read import UserRead

connection = connect()

if not connection:
    print("Failed to establish database connection. Exiting...")
    exit()

while True:
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

    choice = input("\nSelect an option: ").lower()

    if choice == '1':
        name = input("Enter table name to create (or 's' to cancel): ")
        if name != 's':
            create_table(connection, name)

    elif choice == '2':
        table = choose_table(connection)
        if table:
            delete_table(connection, table)

    elif choice == '3':
        show_tables(connection)

    elif choice == '4':
        table = choose_table(connection)
        if table:
            get_table_content(connection, table)

    elif choice == '5':
        table = choose_table(connection)
        if table:
            name = input("User Name: ")
            email = input("User Email: ")
            pwd = input("User Password: ")
            UserAdd(name, email, pwd, table).add(connection)

    elif choice == '6':
        table = choose_table(connection)
        if table:
            uid = input("User ID to edit: ")
            while True:
                col = input("Field to edit (name, email, or password): ").lower()
                if col in ['name', 'email', 'password']:
                    val = input(f"Enter new {col}: ")
                    UserEdit(uid, col, val, table).update(connection)
                    break
                print("Invalid field. Use 'name', 'email', or 'password'.")

    elif choice == '7':
        table = choose_table(connection)
        if table:
            try:
                uid = int(input("User ID to delete: "))
                UserDelete(uid, table).delete(connection)
            except ValueError:
                print("Error: ID must be a number.")

    elif choice == '8':
        table = choose_table(connection)
        if table:
            email = input("Enter email to search: ")
            user = UserRead(email, table).read(connection)
            if user:
                print(f"User Data: {user}")
            else:
                print("User not found.")

    elif choice == 's':
        connection.close()
        print("Connection closed. Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")