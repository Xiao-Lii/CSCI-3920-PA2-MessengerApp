# region ServerWorker

import socket

from threading import Thread


class ServerWorker(Thread):
    """Background thread within the client that allows asynchronous sending and receiving of messages"""

    def __init__(self, port_to_listen: int):
        super().__init__()
        self.__port = port_to_listen
        self.__server_socket = None
        self.__client_socket = None
        self.__incoming_messages = []
        self.__keep_running = True

    # region Getters and Setters

    @property
    def server_socket(self):
        return self.__server_socket

    @server_socket.setter
    def server_socket(self, server_socket: socket):
        self.__server_socket = server_socket

    @property
    def incoming_messages(self):
        return self.__incoming_messages

    # endregion

    # region Methods
    def send_message(self, msg: str):
        self.display_message(f"""SEND>> {msg}""")
        self.__client_socket.send(msg.encode("UTF-8"))

    def receive_message(self, max_length: int = 1024):
        return self.__client_socket.recv(max_length).decode("UTF-8")

    def display_message(self, msg: str):
        print(f"""CLIENT (BG) >> {msg}""")

    def process_server_request(self):
        server_message = self.receive_message()
        self.display_message(f"""SERVER SAID >>>{server_message}""")

        arguments = server_message.split("|")
        response = ""

        try:
            if arguments[0] == "R":
                response = f"0|{arguments[2]}"
                message = arguments[3]
                self.__incoming_messages.append(f"{arguments[1]} said: {message}")
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
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind(("localhost", self.__port))
        self.display_message("Listening for connections...")
        self.__server_socket.listen(1)
        self.__client_socket, client_address = self.__server_socket.accept()
        self.display_message(f"""Got a connection from {client_address}""")

        while self.__keep_running:
            self.process_server_request()

        self.__client_socket.close()

    def terminate_connection(self):
        self.__keep_running = False

    # endregion

# endregion