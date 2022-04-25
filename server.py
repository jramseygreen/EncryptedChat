import json
import socket
import threading

from crypto import CryptoWrapper


class Server:
    def __init__(self, host="localhost", port=9876):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__port = port
        self.__accounts = {}
        self.__clients = {}
        self.__running = False
        self.__mailbox = {}

    def start(self):
        self.__running = True
        self.__sock.bind((self.__host, self.__port))
        self.__sock.listen()
        self.__listen()

    def stop(self):
        self.__running = False
        self.__sock.close()

    def add_account(self, username, password):
        if username not in self.__accounts:
            self.__accounts[username] = password
            self.__mailbox[username] = []

    def del_account(self, username):
        if username in self.__accounts:
            del self.__accounts[username]

    def __listen(self, running=False):
        if not running:
            threading.Thread(target=self.__listen, args=(True,)).start()
        else:
            while self.__running:
                conn, addr = self.__sock.accept()
                x = threading.Thread(target=self.__client_thread, args=(conn,))
                x.setDaemon(True)
                x.start()

    def __client_thread(self, conn):
        username = ""
        crypto = None
        try:
            while True:
                msg = conn.recv(2046).decode()
                if username in self.__accounts:
                    if not crypto:
                        crypto = CryptoWrapper(self.__accounts[username])
                    msg = crypto.decrypt(msg)
                    data = json.loads(msg)
                    if "command" in data and data["command"] == "PRIVMSG":
                        if data["username"] in self.__accounts:
                            crypto.set_password(self.__accounts[data["username"]])
                            if data["username"] in self.__clients:
                                client = self.__clients[data["username"]]
                                data["username"] = username
                                client.sendall(crypto.encrypt(json.dumps(data)).encode())
                            else:
                                self.__mailbox[data["username"]].append(username + " sent: " + data["message"])
                            crypto.set_password(self.__accounts[username])

                else:
                    data = json.loads(msg)
                    if data["command"] == "authenticate":
                        username = data["username"]
                        if username in self.__accounts:
                            crypto = CryptoWrapper(self.__accounts[username])
                            if crypto.decrypt(data["password"]) == self.__accounts[username]:
                                self.__clients[data["username"]] = conn
                                conn.sendall(crypto.encrypt(json.dumps({"command": "PRIVMSG", "username": "Server", "message": "Welcome to the chat server!\nCurrently online: " + ", ".join(list(self.__clients.keys()))})).encode())
                                conn.sendall(crypto.encrypt(json.dumps({"command": "PRIVMSG", "username": "Server", "message": "The following messages were in your mailbox:\n" + "\n".join(self.__mailbox[data["username"]])})).encode())
                                self.__mailbox[data["username"]] = []
                            else:
                                conn.sendall("authenticate".encode())
                        else:
                            conn.sendall("authenticate".encode())
        except:
            conn.close()
            if username in self.__clients:
                del self.__clients[username]
