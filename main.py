from client import Client
from server import Server


def show_menu():
    for item in menu:
        print(item)
    print("")


menu = ["[1] Create chat server", "[2] Connect to chat server"]
server = None
client = None

while True:
    show_menu()
    choice = input("select -> ")
    while not choice.isnumeric() and int(choice) <= len(menu) and int(choice) > 0:
        print("Invalid selection!")
        choice = input("select -> ")
    if choice == "1":
        server = Server(input("Enter host: "), int(input("Enter port: ")))
        if len(menu) == 2:
            menu.append("[" + str(len(menu) + 1) + "] Add User to server")
            menu.append("[" + str(len(menu) + 1) + "] Remove User from server")
            menu.append("[" + str(len(menu) + 1) + "] Start")
    elif choice == "2":
        host = input("Enter ip address or hostname to connect to: ")
        client = Client(input("Enter username: "), input("Enter password: "), host)
        if len(menu) == 2:
            menu.append("[" + str(len(menu) + 1) + "] Start")
    elif choice == "3":
        server.add_account(input("username: "), input("password: "))
    elif choice == "4":
        server.del_account(input("Enter username of the account to delete: "))
    elif choice == "5":
        if server:
            server.start()
        if client:
            client.start()
        break
