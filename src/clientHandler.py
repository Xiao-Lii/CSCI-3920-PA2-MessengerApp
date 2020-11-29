from Client import Client
import json


# TODO: I want to put the code in these functions but I'm getting this error..
#   ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host
#   I'll come back to this later
# def client_login():
# def client_message():
# def client_printReceiveMsg():
def menu():
    menuList = "1 | Connect to server\n" \
               "2 | Login\n" \
               "3 | Send message\n" \
               "4 | Print received message\n" \
               "5 | Disconnect\n"
    print(menuList)


if __name__ == "__main__":
    client = Client("localhost", 10000)

    menu()
    userChoice = input("Enter choice: ")
    userChoice = int(userChoice)

    menuOption = True
    while menuOption:
        if userChoice == 1:
            client.connect()

            server_message = client.receive_message()
            print(f"""[CLI] SRV -> {server_message}""")
            menu()  # to remind user of the menu list :|
            option = input("Enter thy choice: ")
            option = int(option)
            if option == 2:
                # when client chooses 1 it will connect to the server

                client_login = True
                while client_login:
                    with open("userlist.json", "r") as openfile:
                        jsonFile = json.load(openfile)

                    userName = input("Enter username: ")
                    userPass = input("Enter password: ")
                    if userName in jsonFile["user"] and userPass in jsonFile["password"]:
                        print("\n[%s] is logged in!\n" % userName.upper())
                        menu()
                        option = input("Enter thy choice: ")
                        option = int(option)

                        client_runs = True
                        while client_runs:
                            if option == 3:
                                msg = input("Message to send: ")
                                client.send_message(msg)

                                # TODO:
                                #   still need to do #4 and I don't know what to do with 3
                                #   prints received messages saved in servers json file
                                #   once the saved message was received by client, the message
                                #   sent must be removed in server
                                server_message = client.receive_message()
                                print(f"""[CLI] SRV -> {server_message}""")

                                if msg == "TERMINATE" or msg == "QUIT":
                                    client_runs = False
                            elif option == 5:
                                client_runs = False

                    else:
                        print("username and/or password is incorrect!"
                              "\nPlease try again!")



                # TODO:
                #   need to create a background thread. this thread receives the messages of the server and stores it
                #   in the list??? then this thread will be connected to the server
