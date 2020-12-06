from threading import Thread
from database import Database
from user import User
from bg_clientWorker import BackgroundClientWorker
from message import Message
import socket
import json
import queue

"""Server main thread"""
class Server(Thread):
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
        self.__list_of_cw = []
        self.__connection_count = 0


    @property
    def database(self):
        return self.__database

    @property
    def list_of_cw(self):
        return self.__list_of_cw

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
                self.__list_of_cw.append(cw)
                cw.start()
            except Exception as e:
                print(e)

        cw: ClientWorker
        for cw in self.__list_of_cw:
            cw.terminate_connection()
            cw.join()

    def load_from_file(self):
        filename = input("Filename w/o file type extension (.json files only): ")
        try:
            with open(f"{filename}.json", "r") as database_file:
                database_dict = json.load(database_file)
                print("SUCCESS: Data uploaded successfully")
        except FileNotFoundError as fe:
            print(fe)
            return

        users_list = []
        for user_dict in database_dict["user_dict"]:
            user = User(user_dict.get("_User__username"), user_dict.get("_User__password"),
                        user_dict.get("_User__email"))
            users_list.append(user)

        messages_queue = queue.Queue
        for message_dict in database_dict["messages_dict"]:
            user_from_dict = message_dict["_Message__user_from"]
            user_to_dict = message_dict["_Message__user_to"]
            user_from = User(user_from_dict.get("_User__username"), user_from_dict.get("_User__password"),
                             user_from_dict.get("_User__email"))
            user_to = User(user_to_dict.get("_User__username"), user_to_dict.get("_User__password"),
                           user_to_dict.get("_User__email"))
            message_to_put = Message(user_from, user_to, message_dict.get("_Message__content"))
            messages_queue.put(message_to_put)

        notification_queue = queue.Queue
        for notification_dict in database_dict["notifications_dict"]:
            user_from_dict = notification_dict["_Message__user_from"]
            user_to_dict = notification_dict["_Message__user_to"]
            user_from = User(user_from_dict.get("_User__username"), user_from_dict.get("_User__password"),
                             user_from_dict.get("_User__email"))
            user_to = User(user_to_dict.get("_User__username"), user_to_dict.get("_User__password"),
                           user_to_dict.get("_User__email"))
            message_to_put = Message(user_from, user_to, notification_dict.get("_Message__content"))
            messages_queue.put(message_to_put)

        self.__database = Database(users_list, messages_queue, notification_queue)

    def save_to_file(self):
        database_dict = {"user_dict": [], "messages_dict": [], "notifications_dict": []}
        for user in self.__database.users:
            serialized_user = user.__dict__
            database_dict["user_dict"].append(serialized_user)
        for message in list(self.__database.outgoing_messages.queue):
            serialized_message = {"id": message.id, "user_to": {message.user_to.__dict__},
                                  "user_from": {message.user_from.__dict__}, "content": message.content}
            database_dict["messages_dict"].append(serialized_message)
        for notification in list(self.__database.outgoing_notifications.queue):
            serialized_notification = {"id": notification.id, "user_to": {notification.user_to.__dict__},
                                       "user_from": {notification.user_from.__dict__}, "content": notification.content}
            database_dict["messages_dict"].append(serialized_notification)

        filename = input("Filename w/o file type extension (.json files only): ")
        try:
            with open(f'{filename}.json', 'w') as database_file:
                json.dump(database_dict, database_file)
        except Exception as e:
            print(e)

    def display_menu(self):
        service_menu =  "--- Server Main Menu ---\n" \
                        "1. Load data from file.\n" \
                        "2. Start the messenger service\n" \
                        "3. Stop the messenger service\n" \
                        "4. Save data to file\n" \
                        "Please select an option: \n"
        return int(input(service_menu))


"""ClientWorker will listen for Client Requests"""
class ClientWorker(Thread):
    def __init__(self, client_id: int, client_socket: socket, database: Database, server: Server):
        super().__init__()
        self.__id = client_id
        self.__client_socket = client_socket
        self.__database = database
        self.__server = server
        self.__user = None
        self.__keep_clientRunning = True
        self.__background_client_worker = BackgroundClientWorker()

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

    def connect_to_client_background(self, port):
        self.__background_client_worker.client_socket = self.__client_socket
        self.__background_client_worker.database = self.__database
        self.__background_client_worker.port = port
        self.__background_client_worker.start()

    def terminate_connection(self):
        self.__keep_clientRunning = False
        self.__background_client_worker.terminate_connection()
        return "0|OK"


    def send_message(self, msg: str):
        self.display_message(f"""[SRV] >> {msg}""")
        self.__client_socket.send(msg.encode("UTF-8"))

    def receive_message(self, max_length: int = 1024):
        msg = self.__client_socket.recv(max_length).decode("UTF-8")
        print(f"""RECV>> {msg}""")
        return msg

    def display_message(self, msg: str):
        print(f"""CW >> {msg}""")

    def sign_in_user(self, username: str, password: str):
        user_to_sign_in = None
        response = ""
        user: User
        cw: ClientWorker
        signed_in = False
        # search for user where the username and password match
        for user in self.__database.users:
            if user.username == username and user.password == password:
                # then search thru the list of connected clients to make sure the user isn't already signed in
                for cw in self.__server.list_of_cw:
                    if cw.user is user:
                        response = "2|Already signed in."
                        signed_in = True
                        break
                # if the user isn't already signed in...
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
        self.display_message("Connected to Client. Attempting connection to client background thread")
        for user in self.__database.users:
            print(user)
        while self.__keep_clientRunning:
            self.process_client_request()

        self.__client_socket.close()
        for client in self.__server.list_of_cw:
            if client.id == self.__id:
                self.__server.list_of_cw.remove(client)


    def process_client_request(self):
        client_message = self.receive_message()
        self.display_message(f"""[CLIENT] {client_message}""")

        arguments = client_message.split("|")
        response = ""

        try:
            if arguments[0] == "PORT":
                # Need to figure out how to handle response here. The background clientworker may need to time out
                # after a certain number of tries.
                self.connect_to_client_background(int(arguments[1]))
                response = "OK"
            elif arguments[0] == "LOG":
                response = self.sign_in_user(arguments[1], arguments[2])
            elif arguments[0] == "USR":
                response = self.database.sign_up_user(arguments[1], arguments[2], arguments[3])
            elif arguments[0] == "MSG":
                response = self.database.send_message(arguments[1], arguments[2], arguments[3])
            elif arguments[0] == "OUT":
                response = self.terminate_connection()
            else:
                response = "ERR|Unknown Command."
        except ValueError as ve:
            response = "ERR|" + str(ve)

        self.send_message(response)



if __name__ == "__main__":
    keep_running = True
    server = Server("localhost", 10000, 20)

    while keep_running:
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
        elif option == 9:
            print(len(server.list_of_cw))
        else:
            print("Invalid option, try again \n\n")

