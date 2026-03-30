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
        table = chosetable()
        name = input("Digite o nome do usuário: ")
        email = input("Digite o email do usuário: ")
        password = input("Digite a senha do usuário: ")
        useradd(name, email, password, table).add(connection)




    elif choice == '6':
        table = chosetable()
        user_id = input("Digite o ID do usuário a ser editado: ")

        while True:
            action = input("oq vc vai editar?(digite nome, email ou senha)")
            match action:
                case "email":
                    new_edition = input("digite o novo email")
                    break
                case "nome":
                    new_edition = input("digite o novo nome")  
                    action = "name"
                    break
                case "senha":
                    action = "password"
                    new_edition = input("digite a nova senha")
                    break
                case _:
                    print("digite somente nome, senha ou email")
        edituser(user_id, action, new_edition,table).edit(connection)



    elif choice == '7':
        table = chosetable()
        user_id = int(input("Digite o ID do usuário a ser deletado: "))
        userdelete(user_id, table).delete(connection)

    elif choice == '8':
        table = chosetable()
        user_email = input("Digite o email do usuário a ser lido: ")
        readuser(user_email, table).read(connection)

    elif choice == 's':
        connection.close()
        print("Conexão fechada. Saindo...")
        break

    else:
        print("Opção inválida. Tente novamente.")
