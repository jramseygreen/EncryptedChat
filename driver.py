from client import Client
from server import Server

server = Server()
client = Client()
server.add_account("user1", "password1")
server.add_account("user2", "password2")
server.add_account("user3", "password3")

server.start()
client.start()