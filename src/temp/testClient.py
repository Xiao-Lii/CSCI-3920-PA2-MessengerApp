# region Client

from ServerHandler import ServerHandler
import socket

class Client:
    """The main client thread"""

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

    # endregion

    # region Methods

    def connect(self):
        #Connect to the server
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_socket.connect((self.__ip, self.__port))
        self.__is_connected = True

        #Generate a random port number and instatiate a background thread with a socket listening to the random port
        port = int(input("Please enter a port for the server to connect to>"))
        self.__server_worker = ServerHandler(port)
        self.__server_worker.start()
        self.send_message(f"""PORT|{str(port)}""")

    def disconnect(self):
        self.__client_socket.close()
        self.__server_worker.terminate_connection()
        self.__is_connected = False

    def send_message(self, msg: str):
        self.__client_socket.send(msg.encode("UTF-16"))

    def receive_message(self):
        return self.__client_socket.recv(1024).decode("UTF-16")

    def print_received(self):
        pass

    def sign_in_user(self):
        if self.__is_connected:
            sign_in_username = input("Username>")
            sign_in_password = input("Password>")

            self.send_message(f"LOG|{sign_in_username}|{sign_in_password}")
            response = self.receive_message()
            arguments = response.split("|")
            if arguments[0] == "0":
                print("Signed in successfully.")
                self.__is_logged_in = True
                self.__username_of_user = sign_in_username
            elif arguments[0] == "1":
                print("Invalid credentials.")
            elif arguments[0] == "2":
                print("Already Logged in.")
        else:
            print("The client is not connected to a server!")

    def sign_up_user(self):
        if self.__is_connected:
            sign_up_username = input("Input username>")
            sign_up_password = input("Input password>")
            sign_up_phone = input("Input phone number>")
            self.send_message(f"USR|{sign_up_username}|{sign_up_password}|{sign_up_phone}")
            response = self.receive_message()
            arguments = response.split("|")
            if arguments[0] == "0":
                print("User signed up successfully.")
                self.__is_logged_in = True
            elif arguments[0] == "1":
                print(f"{arguments[1]}")
        else:
            print("The client is not connected to a server!")

    def send_message_to_user(self):
        if self.__is_connected and self.__is_logged_in:
            username_to_send = input("Enter the username you want to send the message to>")
            message = input("Your message>")
            self.send_message(f"MSG|{self.__username_of_user}|{username_to_send}|{message}")
            response = self.receive_message()
            arguments = response.split("|")
            if arguments[0] == "0":
                print(f"Message {arguments[1]} sent successfully.")
            elif arguments[0] == "1":
                print("The user sending the message doesn't exist or is not the current user logged in.")
            elif arguments[0] == "2":
                print("The target user doesn't exist.")

    def display_menu(self):
        menu = "1. Connect to server\n"\
               "2. Login\n"\
               "3. Send a Message\n"\
               "4. View Received Messages\n"\
               "5. Disconnect\n"
        print(menu)
        return int(input("Select option [1-5/9]>"))

    # endregion


# endregion

# region ClientApp

if __name__ == "__main__":
    keep_running = True
    client = Client()

    while keep_running:
        option = client.display_menu()
        if option == 1:
            client.ip = input("IP Address>")
            client.port = int(input("Port>"))
            client.connect()
            print(client.receive_message())
        elif option == 2:
            print("1. Login existing user.")
            print("2. Sign up new user.")
            login_option = int(input("Select option [1-2]>"))
            if login_option == 1:
                client.sign_in_user()
            elif login_option == 2:
                client.sign_up_user()
        elif option == 3:
            client.send_message_to_user()
        else:
            print("Invalid option, try again \n\n")

# endregion