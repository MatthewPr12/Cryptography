import re
import socket
import threading

import rsa


class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        # generate keys ...

        while True:
            c, addr = self.s.accept()
            client_info = c.recv(2048).decode()
            username, client_public = client_info.split("(")
            client_public = tuple(map(lambda x: int(x), re.findall(r"(\d+)", client_public)))
            print(f"RECEIVED {client_info}")
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = [username, client_public]
            self.clients.append(c)

            # send public key to the client

            # ...

            # encrypt the secret with the clients public key

            # ...

            # send the encrypted secret to a client

            # ...

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:
            # encrypt the message
            en = self.username_lookup[client][-1]
            encrypted = rsa.encrypt(en, msg)
            # ...

            client.send(str(encrypted).encode())

    def handle_client(self, c: socket, addr):
        while True:
            msg = c.recv(1024)

            for client in self.clients:
                if client != c:
                    en = self.username_lookup[client][-1]
                    encrypted = rsa.encrypt(en, msg)
                    client.send(encrypted)


if __name__ == "__main__":
    s = Server(9001)
    s.start()