# region Client

import socket
import time
from serverworker import ServerWorker

class Client:
    def __init__(self, ip: str = None, port: int = None):
        self.__ip = ip
        self.__port = port
        self.__client_socket = None
        self.__server_worker = None
        self.__is_connected = False
        self.__is_logged_in = False
        self.__username_of_user = None

    # region Getters and Setters

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip: str):
        self.__ip = ip

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port: int):
        self.__port = port

    @property
    def username_of_user(self):
        return self.__username_of_user

    # endregion

    # region Methods

    def connect(self):
        # Connect to the server
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_socket.connect((self.__ip, self.__port))
        self.__is_connected = True

        # ------------------------- POSSIBLE CHANGES HERE FOR LATER -------------------------
        # LET'S CHANGE THIS LATER TO GENERATE A RANDOM NUMBER BETWEEN 10,000 - 60,000 for port #
        port = int(input("Please enter a unused port # for the server to connect to: "))
        # ------------------------- POSSIBLE CHANGES HERE FOR LATER -------------------------

        self.__server_worker = ServerWorker(port)
        self.__server_worker.start()
        self.send_message(f"""PORT|{str(port)}""")

    def disconnect(self):
        self.send_message("OUT|DISCONNECTED")
        response = self.receive_message()
        arguments = response.split("|")
        if arguments[0] == "0":
            print(f"\n{arguments[0]}|{arguments[1]}")
        elif arguments[0] == "1":
            print(arguments[1])
        try:
            self.__client_socket.close()
        # Error Handling - In case socket can't be closed
        except socket.error as se:
            print(f"0|{se}")

        self.__is_connected = False
        self.__is_logged_in = False

    def send_message(self, msg: str):
        self.__client_socket.send(msg.encode("UTF-8"))

    def receive_message(self):
        return self.__client_socket.recv(1024).decode("UTF-8")

    def print_received(self):
        if self.__server_worker.incoming_messages:
            for message in self.__server_worker.incoming_messages:
                print(message + "\n")
        else:
            print("No new messages.")

    def sign_in_user(self):
        if self.__is_connected:
            sign_in_username = input("Username: ")
            sign_in_password = input("Password: ")

            self.send_message(f"LOG|{sign_in_username}|{sign_in_password}")
            response = self.receive_message()
            arguments = response.split("|")
            if arguments[0] == "0":
                print("Signed in successfully.")
                self.__is_logged_in = True
                self.__username_of_user = sign_in_username
            elif arguments[0] == "1":
                print("Invalid credentials. Please try again")
            elif arguments[0] == "2":
                print("User is already signed in.")
        else:
            print("The client is not connected to a server!")

    def sign_up_user(self):
        if self.__is_connected:
            sign_up_username = input("Input username: ")
            sign_up_password = input("Input password: ")
            sign_up_phone = input("Input phone number: ")
            self.send_message(f"USR|{sign_up_username}|{sign_up_password}|{sign_up_phone}")
            response = self.receive_message()
            arguments = response.split("|")

            if arguments[0] == "0":
                print("SUCCESS: User added to system")
                self.__is_logged_in = True
            elif arguments[0] == "1":
                print(f"{arguments[1]}")

        # Error Handling - In case if user tries to sign in prior to connecting to the server
        else:
            print("ERROR: Client not connected to server. Please connect before attempting to sign in.")

    def send_message_to_user(self):
        if self.__is_connected and self.__is_logged_in:
            username_to_send = input("Recipient username: ")
            message = input("Message: ")
            self.send_message(f"MSG|{self.username_of_user}|{username_to_send}|{message}")
            response = self.receive_message()
            arguments = response.split("|")

            if arguments[0] == "0":
                print(f"Message {arguments[1]} sent successfully.")
            elif arguments[0] == "1":
                print("Error: User isn't signed in or doesn't exist")
            elif arguments[0] == "2":
                print("Error: Recipient either doesn't exist or user isn't signed in")

    def display_menu(self):
        cMenu = "----- Client Main Menu -----\n" \
                "1. Connect to server\n" \
                "2. Login\n" \
                "3. Send Message\n" \
                "4. Print Received Messages\n" \
                "5. Disconnect\n" \
                "Please select an option: "
        return int(input(cMenu))

    # endregion


# endregion

# region ClientApp

if __name__ == "__main__":
    keep_running = True
    client = Client()

    while keep_running:
        # Sleeping delay so that BG_ClientWorker can send messages prior to the next display of menu
        time.sleep(1)

        try:
            option = client.display_menu()
            # Option 1 = Connect to Server
            if option == 1:
                client.ip = "localhost"
                client.port = 10000
                # In successful connection, system will prompt user for a unique port # to
                # Want to change prompting the user for a unique port # and just randomly generating it instead
                client.connect()
                print(client.receive_message())

            # Option 2 - Login to Messenger App
            elif option == 2:
                login_menu = "1. Login existing user.\n" \
                             "2. Sign up new user.\n" \
                             "Please enter an option: "
                login_option = int(input(login_menu))
                # SubOption 1 = Login an existing user
                if login_option == 1:
                    client.sign_in_user()
                # SubOption 2 = Sign up a new user
                elif login_option == 2:
                    client.sign_up_user()

            # Option 3 - Send a Message
            elif option == 3:
                client.send_message_to_user()

            # Option 4 - Check for Received Messages
            elif option == 4:
                client.print_received()

            # Option 5 - Disconnect Client
            elif option == 5:
                client.disconnect()
                keep_running = False

            else:
                print("Invalid option, try again \n\n")

        # In case user-input at menu options is not an integer
        # This will stop the server from crashing unexpectedly
        except ValueError:
            print("Error: Invalid Input - Data Type")

# endregion