import socket
import select
from threading import Thread

socket_list = []

def send_message(msg: str, client_socket: socket):
    print(f"""[SRV] SEND >> {msg}""")
    client_socket.send(msg.encode("UTF-16"))
    pass

def receive_message(client_socket: socket, max_length: int = 1024):
    """ # For some weird reason, the try block causes errors with receiving the message
    try:
        message_header = client_socket.recv(10)
        if not len(message_header):
            return False

        message_length = int(message_header.decode("UTF-8").strip())
        if message_length < 1025:
            return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False
    """
    msg = client_socket.recv(max_length).decode("UTF-16")
    print(f"""[SRV] RCV >> {msg}""")
    return msg

# 1. Start a Multi-threaded Server
# 2. While True, attempt to accept a client connection
# 3. If connection is received = Create a ClientWorker
# 4.

class Server(Thread):
    def __init__(self, ip: str, port: int, backlog: int):
        super().__init__()
        self.__ip = ip
        self.__port = port
        self.__backlog = backlog
        self.__keep_running = True

    # Server = Main Thread that's always listening for clients
    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.__ip, self.__port))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(self.__backlog)

        while self.__keep_running:
            print(f"""[SRV] Waiting for Client""")
            client_socket, client_address = server_socket.accept()

            # IF CLIENT CONNECTION RECEIVED
            # Create a new thread to clientWorker one for sending

            print(f"""[SRV] Got a Connection from {client_address}""")

            send_message("Connected to Python Echo Server", client_socket)

            client_runs = True
            while client_runs:

                client_message = str(receive_message(client_socket))
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

    """
    def start_service_menu(self, client_socket:socket):
        service_menu =  "1. Load data from file.\n" \
                        "2. Start the messenger service\n" \
                        "3. Stop the messenger service\n" \
                        "4. Save data to file\n"
        print(service_menu)
        displayStart = True
        while displayStart:
            # 1st we want to keep displaying the Start Menu to the User
            client_socket.send(service_menu.encode("UTF-16"))
            client_message = str(receive_message(client_socket))
            # END OF RECEIVE MESSAGE


            if client_message == 1:
                # READ THAT FILE
                print("Inside option 1")            # Test Filler - May delete
            elif client_message == 2:
                # BETTER START THAT MESSENGER
                # MAYBE FOR RIGHT HERE, WE WANT:
                #       1. MAYBE TO CREATE A NEW MESSENGING SYSTEM OBJECT IF ONE WASN'T LOADED IN
                #       2. CALL FUNCTION TO OPEN THE NEXT MENU - USER LOGIN
                print("Inside option 2")            # Test Filler - May delete
            elif client_message == 3:
                # BETTER STOP THAT MESSENGER
                print("Inside option 3")            # Test Filler - May delete
            elif client_message == 4:
                # SAVE THE FILE
                print("Inside option 4")            # Test Filler - May delete
            else:
                # DONE GOOF NOW - ERROR
                print("Error: Invalid menu selection")
    """

    def sign_up(self, messengerApp, username, password):
        # We want to access the messengerApp's current list of Users
        # 1. Check if the username/email exists in our list of registered users?
            # If so, success = Create an account, call User Constructor
            # If not, display error
        return # WE DON'T NEED THIS - MAY DELETE LATER

    def sign_in(self, messengerApp, username, password):
        # We want to access the messengerApp's current list of Users
        # 1. Does the username/email in our list of registered users?
        # 2. Is the password correct?
        # If so, success = Create a thread for Client
        # If not, display error
        return # WE DON'T NEED THIS - MAY DELETE LATER


