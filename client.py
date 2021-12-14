import json
import socket
import threading

from crypto import CryptoWrapper

class Client:
    def __init__(self, username, password, host="localhost", port=9876):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__crypto = CryptoWrapper(password)
        self.__running = False

    def start(self):
        self.__sock.connect((self.__host, self.__port))
        self.__running = True
        self.__listen()
        self.__sock.sendall(json.dumps({"command": "username", "username": self.__username}).encode())

    def stop(self):
        self.__running = False

    def send_message(self, username, message):
        self.__sock.sendall(self.__crypto.encrypt(json.dumps({"command": "PRIVMSG", "username": username, "message": message}).encode()))

    def __listen(self, running=False):
        if not running:
            threading.Thread(target=self.__listen, args=(True,)).start()
        else:
            while self.__running:
                msg = self.__sock.recv(2046).decode()
                data = json.loads(self.__crypto.decrypt(msg))
                if data["command"] == "PRIVMSG":
                    print(data["username"] + " sent: " + data["message"])