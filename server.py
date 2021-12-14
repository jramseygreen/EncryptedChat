import json
import socket
import threading

from crypto import CryptoWrapper


class Server:
    def __init__(self, host="localhost", port=9876):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__port = port
        self.__clients = {"admin": "password"}
        self.__running = False

    def start(self):
        self.__running = True
        self.__sock.bind((self.__host, self.__port))
        self.__listen()

    def stop(self):
        self.__running = False

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
                if username in self.__clients:
                    if not crypto:
                        crypto = CryptoWrapper(self.__clients[username])
                    msg = crypto.decrypt(msg)
                    data = json.loads(msg)
                    if data["command"] == "PRIVMSG":
                        if data["username"] in self.__clients:
                            crypto.set_password(self.__clients[data["username"]])
                            data["username"] = username
                            self.__sock.sendall(crypto.encrypt(json.dumps(data)).encode())
                            crypto.set_password(self.__clients[username])

                else:
                    data = json.loads(msg)
                    if data["command"] == "username":
                        username = data["username"]
        except:
            conn.close()