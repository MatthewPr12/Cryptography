import socket
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
        self.public, self.secret = rsa.generate_keypairs(13, 17)
        info = self.username + " " + str(self.public)
        print(f"SENDING {info} TO SERVER")
        # print(f"ENCODED {info.encode()}")
        # print(f"DECODED {info.encode().decode()}")
        self.s.send(info.encode())

        # exchange public keys
        # self.s.send(str(self.public).encode())

        # receive the encrypted secret key
        # others_public = self.s.recv(2048).decode()

        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self):
        while True:
            message = self.s.recv(1024).decode()

            # decrypt message with the secrete key
            decrypted = rsa.decrypt(self.secret, message)
            # ...

            print(decrypted)

    def write_handler(self):
        while True:
            message = input()

            # encrypt message with the secrete key
            # ...

            self.s.send(message.encode())


if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "user")
    cl.init_connection()
