import socket
import re
import threading
import rsa


class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        # create key pairs
        n, e, d = rsa.create_keys()
        self.public = (e, n)
        self.secret = (d, n)
        info = self.username + str(self.public)
        # print(f"SENDING {info} TO SERVER")
        # print(f"ENCODED {info.encode()}")
        # print(f"DECODED {info.encode().decode()}")
        server_public = self.s.recv(2048).decode()
        # print(f"SERVER's PUBLIC KEYS {server_public}")
        server_public = tuple(map(lambda x: int(x), re.findall(r"(\d+)", server_public)))
        self.s.send(info.encode())

        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=server_public)
        input_handler.start()

    def read_handler(self):
        while True:
            message = self.s.recv(1024).decode()

            # decrypt message with the secrete key
            # print(f"[CLIENT] received {message}")
            decrypted = rsa.decrypt(message, self.secret)
            # print(f"[CLIENT] decrypted")

            print(decrypted)

    def write_handler(self, e, n):
        server_public = (e, n)
        while True:
            message = input()

            # print(f"[CLIENT] SENDING {message}")
            encrypted = rsa.encrypt(message, server_public)
            # print(f"[CLIENT] sending encrypted to server {encrypted}")
            self.s.send(encrypted.encode())


if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "user")
    cl.init_connection()