from threading import Thread
from Database import Database
from User import User
from bg_clientWorker import BackgroundClientWorker
from Message import Message
import socket
import json
import queue
import time


class Server(Thread):
    """Server - Our Main Thread for Starting the Messenger App"""

    def __init__(self, ip: str, port: int, backlog: int):
        super().__init__()
        self.__ip = ip
        self.__port = port
        self.__backlog = backlog
        self.__server_socket = None
        self.__client_socket = None
        self.__keep_running = True
        self.__keep_running_client = True
        self.__database = Database()
        self.__list_of_connected_clients = []
        self.__connected_users = []
        self.__connection_count = 0

    @property
    def database(self):
        return self.__database

    @property
    def list_of_connected_clients(self):
        return self.__list_of_connected_clients

    def connected_users(self):
        return self.__connected_users

    @property
    def keep_running(self):
        return self.__keep_running

    @keep_running.setter
    def keep_running(self, status: bool):
        self.__keep_running = status

    def terminate_server(self):
        self.__keep_running = False
        self.__server_socket.close()

    def run(self):
        """For starting and running the server, establishes port and continuously waits for a new client connections"""

        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__ip, self.__port))
        self.__server_socket.listen()

        while self.__keep_running:
            print(f"""[SRV] Waiting for a client connection""")
            try:
                self.__client_socket, client_address = self.__server_socket.accept()
                self.__connection_count += 1
                print(f"""[SRV] Got a connection from {client_address}""")
                cw = ClientWorker(self.__connection_count, self.__client_socket, self.__database, self)
                self.__list_of_connected_clients.append(cw)
                cw.start()
            except Exception as e:
                print(e)

        cw: ClientWorker
        for cw in self.__list_of_connected_clients:
            cw.terminate_connection()
            cw.join()

    def load_from_file(self):
        """Reads in a database that are a .json file type and loads in:
                1st List = List of User Info
                2nd List = List of Messages to Send
                3rd List = List of Banners to display received msgs"""

        filename = input("Filename w/o file type extension (.json files only): ")
        try:
            with open(f"{filename}.json", "r") as database_file:
                database_list = json.load(database_file)
                print("SUCCESS: Data uploaded successfully")
        except FileNotFoundError as fe:
            print(fe)
            return

        #
        users_list = []
        for user_info in database_list["user_list"]:
            # Loading up Users for Database
            user = User(user_info.get("_User__username"), user_info.get("_User__password"),
                        user_info.get("_User__email"))
            users_list.append(user)

        msg_list = queue.Queue
        for message_in_queue in database_list["message_list"]:
            # Loading up Messages for Sender and Receivers
            sending_user_msgs = message_in_queue["_Message__user_from"]
            receiving_user_msgs = message_in_queue["_Message__user_to"]

            # Retrieving Sender and Receiver's Data
            sender = User(sending_user_msgs.get("_User__username"), sending_user_msgs.get("_User__password"),
                          sending_user_msgs.get("_User__email"))
            recipient = User(receiving_user_msgs.get("_User__username"), receiving_user_msgs.get("_User__password"),
                             receiving_user_msgs.get("_User__email"))

            # Assembling Message to be sent with data collected
            message_to_put = Message(sender, recipient, message_in_queue.get("_Message__content"))
            msg_list.put(message_to_put)

        banner_list = queue.Queue
        for notification_list in database_list["notification_list"]:
            # Loading up Notications for Messages for Sender and Receivers
            sending_user_msgs = notification_list["_Message__user_from"]
            receiving_user_msgs = notification_list["_Message__user_to"]

            # Retrieving Sender and Receiver's Data
            sender = User(sending_user_msgs.get("_User__username"), sending_user_msgs.get("_User__password"),
                          sending_user_msgs.get("_User__email"))
            recipient = User(receiving_user_msgs.get("_User__username"), receiving_user_msgs.get("_User__password"),
                             receiving_user_msgs.get("_User__email"))

            # Assembling Notification Message to be sent with data collected
            message_to_put = Message(sender, recipient, notification_list.get("_Message__content"))
            msg_list.put(message_to_put)

        self.__database = Database(users_list, msg_list, banner_list)

    def save_to_file(self):
        database_list = {"user_list": [], "message_list": [], "notification_list": []}

        # Iterates through all users to append to our database
        for user in self.__database.users:
            serialized_user = user.__dict__
            database_list["user_list"].append(serialized_user)

        # Iterates through all messages to append to our database
        for message in list(self.__database.outgoing_messages.queue):
            serialized_message = {"id": message.id, "user_to": {message.user_to.__dict__},
                                  "user_from": {message.user_from.__dict__}, "content": message.content}
            database_list["message_list"].append(serialized_message)

        # Iterates through all notifications to append to our database
        for notification in list(self.__database.outgoing_banners.queue):
            serialized_notification = {"id": notification.id, "user_to": {notification.user_to.__dict__},
                                       "user_from": {notification.user_from.__dict__}, "content": notification.content}
            database_list["message_list"].append(serialized_notification)

        # Prompts the user for the filename to save/write into
        file = input("Filename w/o file type extension (.json files only): ")
        try:
            with open(f'{file}.json', 'w') as database_file:
                json.dump(database_list, database_file)

        # Error Handling: Issues with Writing/Saving to File
        except Exception as error:
            print(error)

    def display_menu(self):
        """Displays the main menu of server options"""
        service_menu = "----- Server Main Menu -----\n" \
                       "1. Load data from file.\n" \
                       "2. Start the messenger service\n" \
                       "3. Stop the messenger service\n" \
                       "4. Save data to file\n" \
                       "Please select an option: \n"
        return int(input(service_menu))


class ClientWorker(Thread):
    """ClientWorker will listen for Client Requests such as signing in, creating an account, sending messages,
    receiving message, displaying any received messages, and disconnecting the client from the server"""

    def __init__(self, client_id: int, client_socket: socket, database: Database, server: Server):
        super().__init__()
        self.__id = client_id
        self.__client_socket = client_socket
        self.__database = database
        self.__server = server
        self.__background_client_worker = BackgroundClientWorker()
        self.__keep_clientRunning = True
        self.__user = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, client_id: int):
        self.__id = client_id

    @property
    def client_socket(self):
        return self.__client_socket

    @client_socket.setter
    def client_socket(self, client_socket: socket):
        self.__client_socket = client_socket

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, database: Database):
        self.__database = database

    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, server: Server):
        self.__server = server

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user: User):
        self.__user = user

    @property
    def keep_client_running(self):
        return self.__keep_clientRunning

    @keep_client_running.setter
    def keep_client_running(self, state: bool):
        self.__keep_clientRunning = state

    def connect_to_bg_client(self, port):
        """This connects the client to their own background client worker"""
        self.__background_client_worker.client_socket = self.__client_socket
        self.__background_client_worker.database = self.__database
        self.__background_client_worker.port = port
        self.__background_client_worker.start()

    def terminate_connection(self):
        """Disconnects the user/client from the server"""
        self.__keep_clientRunning = False
        self.__background_client_worker.terminate_connection()
        return "0|OK"

    def send_message(self, msg: str):
        self.display_message(f"""[SRV] >> {msg}""")
        self.__client_socket.send(msg.encode("UTF-8"))

    def receive_message(self, max_length: int = 1024):
        msg = self.__client_socket.recv(max_length).decode("UTF-8")
        print(f"""[RECV] {msg}""")
        return msg

    def display_message(self, msg: str):
        print(f"""[CW] {msg}""")

    def sign_in_user(self, username: str, password: str):
        """Attempts to sign the user by checking if username/email exists within the database, returning errors if
        otherwise"""
        user: User
        signed_in = False
        cw: ClientWorker
        response = ""

        # Check if User is found in Database's list of Users
        for user in self.__database.users:
            # If found, check if username and password match per user
            if user.username == username and user.password == password:
                # If credentials match, need to verify that if user is already signed in or not

                # SERVER NOT DETECTING IF USER IS ALREADY SIGNED IN OR NOT WITH THE LIST BELOW
                # MAY NEED TO CHANGE IT TO CHECK WITH A LIST OF USERS THAT ARE CONNECTED
                # CLIENT RECEIVES AN ERROR OF '1|Invalid Credentials' INSTEAD OF ERROR 2
                for cw in self.__server.list_of_connected_clients:
                    if cw.user is user:
                        response = "2|Already signed in."
                        signed_in = True
                        break

                # Otherwise, if user is not in list of connected clients, proceed to sign in
                if not signed_in:
                    self.__user = user
                    self.__background_client_worker.user = user
                    self.display_message(f"Successfully signed in {self.__user.username}")
                    response = "0|OK"

            # if the user name matches but the password doesn't...
            elif user.username is username and password is not user.password:
                self.display_message("Incorrect password")
                response = "1|Invalid Credentials"
        # if the user isn't found...
        if not self.__user:
            self.display_message("That user doesn't exist")
            response = "1|That user doesn't exist."

        return response

    def sign_out_user(self):
        pass

    def run(self):
        """Our Run program for the client worker, this is responsible for maintaining the client connection unless
        otherwise requested"""
        self.display_message("SUCCESS: Connected to Client. Attempting connection to client background thread")
        for user in self.__database.users:
            print(user)
        while self.__keep_clientRunning:
            self.process_client_request()

        self.__client_socket.close()
        for client in self.__server.list_of_connected_clients:
            if client.id == self.__id:
                self.__server.list_of_connected_clients.remove(client)

    def process_client_request(self):
        """Delimits the client request and properly categorizes the request of the user into their desire parameters"""
        client_message = self.receive_message()
        self.display_message(f"""[CLIENT] {client_message}""")

        arguments = client_message.split("|")
        response = ""

        try:
            if arguments[0] == "PORT":
                self.connect_to_bg_client(int(arguments[1]))
                response = "OK"
            elif arguments[0] == "LOGIN":
                response = self.sign_in_user(arguments[1], arguments[2])
            elif arguments[0] == "ADD":
                response = self.database.sign_up_user(arguments[1], arguments[2], arguments[3])
            elif arguments[0] == "MSG":
                response = self.database.send_message(arguments[1], arguments[2], arguments[3])
            elif arguments[0] == "QUIT":
                response = self.terminate_connection()
            # Error Handling: In case if client request was unrecognizable
            else:
                response = "ERR|Unknown Command."
        except ValueError as ve:
            response = "ERR|" + str(ve)

        self.send_message(response)


if __name__ == "__main__":
    keep_running = True
    server = Server("localhost", 10000, 30)

    while keep_running:
        # Sometimes the menu displays before responses are displayed
        # One second delay to display menu after receiving server/worker responses
        time.sleep(1)
        option = server.display_menu()
        if option == 1:
            server.load_from_file()
        elif option == 2:
            server.start()
        elif option == 3:
            server.terminate_server()
            server.join()
            keep_running = False
        elif option == 4:
            server.save_to_file()
        else:
            print("Invalid option, try again \n\n")
