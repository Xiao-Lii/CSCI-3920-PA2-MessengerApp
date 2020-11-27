import socket
import select
from threading import Thread

socket_list = []


def send_message(msg: str, client_socket: socket):
    print(f"""[SRV] SEND >> {msg}""")
    client_socket.send(msg.encode("UTF-16"))
    pass


def receive_message(client_socket: socket, max_length: int = 1024):
    try:
        message_header = client_socket.recv(10)
        if not len(message_header):
            return False

        message_length = int(message_header.decode("UTF-8"))
        if message_length < 1025:
            return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False

    msg = client_socket.recv(max_length).decode("UTF-16")
    print(f"""[SRV] RCV >> {msg}""")
    return msg


class Server(Thread):
    def __init__(self, ip: str, port: int, backlog: int):
        super().__init__()
        self.__ip = ip
        self.__port = port
        self.__backlog = backlog
        self.__keep_running = True

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.__ip, self.__port))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(self.__backlog)

        while self.__keep_running:
            print(f"""[SRV] Waiting for Client""")
            client_socket, client_address = server_socket.accept()
            print(f"""[SRV] Got a Connection from {client_address}""")

            send_message("Connected to Python Echo Server", client_socket)

            client_runs = True
            while client_runs:
                client_message = receive_message(client_socket)
                if client_message == "QUIT":
                    client_runs = False
                    send_message("OK", client_socket)
                elif client_message == "TERMINATE":
                    client_runs = False
                    self.__keep_running = False
                    send_message("OK", client_socket)
                else:
                    send_message(client_message.upper(), client_socket)

            client_socket.close()

        server_socket.close()
