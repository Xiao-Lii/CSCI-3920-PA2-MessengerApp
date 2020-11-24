import socket


class Server:

    def __init__(self, ip: str, port: int, backlog: int):
        self.__ip = ip
        self.__port = port
        self.__backlog = backlog
        self.__keep_running = True

    def send_message(self, msg: str, client_socket: socket):
        print(f"""[SRV]{msg}""")
        client_socket.send(msg.encode("UTF-16"))
        pass

    def receive_message(self, client_socket: socket, max_length: int = 1024):
        msg = client_socket.recv(max_length).decode("UTF-16")
        print(f"""[SRV] RCV >>{msg}""")
        return msg

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.__ip, self.__port))
        server_socket.listen(self.__backlog)

        while self.__keep_running:
            print(f"""[SRV] Waiting for Client""")
            client_socket, client_address = server_socket.accept()
            print(f"""[SRV] Got a connections from {client_address}""")

            self.send_message('Connected to Python Echo Server', client_socket)

            client_runs = True
            while client_runs:
                client_message = self.receive_message(client_socket)
                if client_message == 'QUIT':
                    client_runs = False
                    self.send_message("OK", client_socket)
                elif client_message == 'TERMINATE':
                    client_runs = False
                    self.__keep_running = False
                    self.send_message("OK", client_socket)
                else:
                    self.send_message(client_message.upper(), client_socket)

            client_socket.close()

        server_socket.close()
