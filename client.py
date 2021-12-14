import json
import socket
import threading

from crypto import CryptoWrapper

class Client:
    def __init__(self, username="", password="", host="localhost", port=9876):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__crypto = CryptoWrapper(password)
        self.__running = False
        self.__current_user = ""

    def start(self):
        self.__sock.connect((self.__host, self.__port))
        self.__running = True
        self.__listen()
        if not self.__username:
            self.__username = input("Username: ")
        if not self.__password:
            self.__password = input("Password: ")
            self.__crypto = CryptoWrapper(self.__password)
        self.__sock.sendall(json.dumps({"command": "authenticate", "username": self.__username, "password": self.__crypto.encrypt(self.__password)}).encode())
        self.__input_loop()

    def stop(self):
        self.__running = False

    def send_message(self, username, message):
        self.__sock.sendall(self.__crypto.encrypt(json.dumps({"command": "PRIVMSG", "username": username, "message": message})).encode())

    def __listen(self, running=False):
        if not running:
            threading.Thread(target=self.__listen, args=(True,)).start()
        else:
            while self.__running:
                msg = self.__sock.recv(2046).decode()
                if msg.strip():
                    if msg == "authenticate":
                        print("Username or Password incorrect!")
                        self.stop()
                        exit(0)
                    data = json.loads(self.__crypto.decrypt(msg))
                    if data["command"] == "PRIVMSG":
                        print("\n" + data["username"] + " sent: " + data["message"])

    def __input_loop(self, running=False):
        if not running:
            x = threading.Thread(target=self.__input_loop, args=(True,))
            x.setDaemon(True)
            x.start()
        else:
            while self.__running:
                msg = input(self.__current_user + ": ")
                attr = msg.split(" ", 2)
                if attr[0] == "!user" and len(attr) > 1:
                    self.__current_user = attr[1]
                elif self.__current_user:
                    self.send_message(self.__current_user, msg)
