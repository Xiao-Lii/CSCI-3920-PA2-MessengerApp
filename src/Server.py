import socket
import select
from threading import Thread

socket_list = []
clients = {}


def send_message(msg: str, client_socket: socket):
    print(f"""[SRV] SEND >> {msg}""")
    client_socket.send(msg.encode("UTF-8"))
    pass


def receive_message(client_socket: socket, max_length: int = 1024):
    try:
        message_header = client_socket.recv(10)
        if not len(message_header):
            return False

        message_length = int(message_header.decode("UTF-8").strip())
        if message_length < 1025:
            return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False

    msg = client_socket.recv(max_length).decode("UTF-8")
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
        socket_list.append(server_socket)

        while self.__keep_running:
            print(f"""[SRV] Waiting for Client""")
            client_socket, client_address = server_socket.accept()
            print(f"""[SRV] Got a Connection from {client_address}""")

            read_sockets, _, exception_sockets, = select.select(socket_list, [], socket_list)

            for notified_socket in read_sockets:
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()
                    user = receive_message(client_socket)
                    if user is False:
                        continue

                    socket_list.append(client_socket)
                    clients[client_socket] = user
                    print(f"Accepted new connection from {client_address[0]}:{client_address[1]}"
                          f"username:{user['data'].decode('UTF-8')}")
                else:
                    message = receive_message(notified_socket)
                    if message is False:
                        print(f"Closed connection from {clients[notified_socket]['data'].decode('UTF-8')}")
                        socket_list.remove(notified_socket)
                        del clients[notified_socket]
                        continue

                    user = clients[notified_socket]
                    print(f"Received message from {user['data'].decode('UTF-8')}: "
                          f"{message['data'].decode('UTF-8')}")

                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

            for notified_socket in exception_sockets:
                socket_list.remove(notified_socket)
                del clients[notified_socket]

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

    def start_service_menu(self):
        service_menu =  "1. Load data from file.\n" \
                        "2. Start the messenger service\n" \
                        "3. Stop the messenger service\n" \
                        "4. Save data to file\n"
        print(service_menu)
        option = input(int())

        if option == 1:
            # READ THAT FILE
            print("Inside option 1")            # Test Filler - May delete
        elif option == 2:
            # BETTER START THAT MESSENGER
            # MAYBE FOR RIGHT HERE, WE WANT:
            #       1. MAYBE TO CREATE A NEW MESSENGING SYSTEM OBJECT IF ONE WASN'T LOADED IN
            #       2. CALL FUNCTION TO OPEN THE NEXT MENU - USER LOGIN
            print("Inside option 2")            # Test Filler - May delete
        elif option == 3:
            # BETTER STOP THAT MESSENGER
            print("Inside option 3")            # Test Filler - May delete
        elif option == 4:
            # SAVE THE FILE
            print("Inside option 4")            # Test Filler - May delete
        else:
            # DONE GOOF NOW - ERROR
            print("Error: Invalid menu selection")

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


