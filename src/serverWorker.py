import socket
from threading import Thread


class ServerWorker(Thread):
    def __init__(self, port_to_listen:int):
        super().__init__()
        self.__port = port_to_listen
        self.__server_socket = None
        self.__client_socket = None
        self.__incoming_messages = []
        self.__keep_running = True

    @property
    def server_socket(self):
        return self.__server_socket

    @server_socket.setter
    def server_socket(self, server_socket: socket):
        self.__server_socket = server_socket

    @property
    def incoming_messages(self):
        return self.__incoming_messages

    def send_message(self, msg: str):
        self.display_message(f"""[BG.CW] {msg}""")
        self.__client_socket.send(msg.encode("UTF-8"))

    def receive_message(self, max_length: int = 1024):
        return self.__client_socket.recv(max_length).decode("UTF-8")

    def display_message(self, msg: str):
        print(f"""[BG.CLIENT] {msg}""")

    def process_server_request(self):
        """Processes server requests by the client"""
        server_message = self.receive_message()
        self.display_message(f"""[SERVER NOTIFICATION] {server_message}""")

        arguments = server_message.split("|")
        response = ""

        try:
            if arguments[0] == "R":
                response = f"0|{arguments[2]}"
                message = arguments[3]
                self.__incoming_messages.append(f"[{arguments[1]}]: {message}")
            elif arguments[0] == "OK":
                response = "0|OK"
                self.display_message(f"Message {arguments[3]} successfully received by {arguments[2]}.")
            elif arguments[0] == "OUT":
                self.terminate_connection()
            else:
                response = "1|ERR"
        except ValueError as ve:
            response = "ERR|" + str(ve)

        self.send_message(response)

    def run(self):
        """This will run evertime our client establishes a connection with the server, so that others can connect to
        the client by sending messages"""
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind(("localhost", self.__port))

        # Standby for incoming Connections
        self.display_message("[STANDBY] Listening for connections")

        self.__server_socket.listen(1)
        self.__client_socket, client_address = self.__server_socket.accept()
        self.display_message(f"""Received connection from {client_address}""")

        while self.__keep_running:
            self.process_server_request()

        self.__client_socket.close()

    def terminate_connection(self):
        self.__keep_running = False
