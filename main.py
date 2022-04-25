from client import Client
from server import Server
import time


def show_menu():
    print("Server active:", bool(server))
    for item in menu:
        print("[" + str(list(menu.keys()).index(item)) + "] " + item)
    print("")

def add_user():
    global server
    server.add_account(input("Username: "), input("Password: "))

def del_user():
    global server
    server.del_account(input("Username: "))

def create_chat_server():
    global server
    if server:
        server.stop()
    server = Server(input("Hostname or IP address: "), int(input("Port: ")))
    server.start()
    menu["Add user"] = add_user
    menu["Remove user"] = del_user

def connect_chat_server():
    global client
    host = input("Enter hostname or IP address to connect to: ")
    port = int(input("Port: "))
    client = Client(input("Username: "), input("Password: "), host, port)
    client.start()
    while client.is_running():
        time.sleep(1)
    client = None

menu = {"Create chat server": create_chat_server,
        "Connect to chat server": connect_chat_server}
server = None
client = None

while True:
    show_menu()
    menu[list(menu.keys())[int(input("Selection -> "))]]()
