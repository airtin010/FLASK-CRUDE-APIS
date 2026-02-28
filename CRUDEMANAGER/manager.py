from maindefs import conectar, createtable, deletetable, showtables,tablecontent, chosetable
from add import useradd
from edit import edituser
from delet import userdelete
from read import readuser


connection = conectar()


while True:
    print("\nMenu:")
    print("1. Criar tabela")
    print("2. Deletar tabela")
    print("3. Mostrar tabelas")
    print("4. Mostrar conteúdo da tabela")
    print("5. Adicionar usuário")
    print("6. Editar usuário")
    print("7. Deletar usuário")
    print("8. Ler usuário")
    print("s. Sair")

    choice = input("Escolha uma opção: ")

    if choice == '1':
        tablename = input("Digite o nome da tabela a ser criada: ou s para sair ")
        if tablename != "s":
            createtable(connection, tablename)


    elif choice == '2':
        deletetable(connection, chosetable())

    elif choice == '3':
        showtables(connection, 1)

    elif choice == '4':
        tablecontent(connection, chosetable())

    elif choice == '5':
        name = input("Digite o nome do usuário: ")
        email = input("Digite o email do usuário: ")
        password = input("Digite a senha do usuário: ")
        useradd(name, email, password).add(connection)
    elif choice == '6':
        user_id = int(input("Digite o ID do usuário a ser editado: "))
        new_name = input("Digite o novo nome do usuário: ")
        new_email = input("Digite o novo email do usuário: ")
        new_password = input("Digite a nova senha do usuário: ")
        edituser(user_id, new_name, new_email, new_password).edit(connection)
    elif choice == '7':
        
        user_id = int(input("Digite o ID do usuário a ser deletado: "))
        userdelete(user_id).delete(connection)
    elif choice == '8':
        user_id = int(input("Digite o ID do usuário a ser lido: "))
        readuser(user_id).read(connection)
    elif choice == 's':
        connection.close()
        print("Conexão fechada. Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")
