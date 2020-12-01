from Client import Client
import json

client = Client("localhost", 10000)


# client connection to server
def clientConnect():
    client.connect()
    server_msg = client.receive_message()
    print(f"""[CLI] SRV -> {server_msg}""")
    return True


def client_sendMsg():
    client_runs = True
    while client_runs:
        msg = input("Message to send: ")
        client.send_message(msg)
        server_msg = client.receive_message()
        print(f"""[CLI] SRV-> {server_msg}""")

        # user will be back to 2nd menu - still connected to server
        if msg == "Disconnect" or msg == "Quit":
            print("Logged out.")
            client_runs = False


if __name__ == "__main__":
    # printing the whole menu
    menuList = "----MENU----\n" \
               "1 | Connect to server\n" \
               "2 | Login\n" \
               "3 | Send message\n" \
               "4 | Print received message\n" \
               "5 | Disconnect\n"
    print(menuList)

    userMenu = input("Please enter your choice: ")
    userMenu = int(userMenu)
    clientMain = True
    while clientMain:
        if userMenu == 1:
            clientConnect()
            cc = True
            while cc:  # menu when client is connected to server
                menuList = "----MENU----\n" \
                           "2 | Login\n" \
                           "3 | Send message\n" \
                           "4 | Print received message\n" \
                           "5 | Disconnect\n"
                print(menuList)
                user1 = input("Please the number of your choice: ")
                user1 = int(user1)

                if user1 == 1:
                    print("Please choose the right option.")

                if user1 == 5:
                    client_login = False
                    cc = False
                    clientMain = False

                elif user1 == 2:
                    client_login = True
                    while client_login:

                        # opens json file
                        # filePath = "C:/Users/mario/Desktop/New folder/PA2Try/src/userlist.json"
                        with open("userlist.json", "r") as openfile:
                            jsonFile = json.load(openfile)
                            jUser = jsonFile["user"]
                            jPass = jsonFile["password"]

                        userName = input("Enter username: ")
                        userPass = input("Enter password: ")

                        if userName in jUser and userPass in jPass:
                            print("\n[%s] is logged in!\n" % userName.upper())

                            # menu when user is logged in
                            menuList = "----MENU----\n" \
                                       "3 | Send message\n" \
                                       "4 | Print received message\n" \
                                       "5 | Disconnect\n"
                            print(menuList)
                            user2 = input("Please type the number of your choice: ")
                            user2 = int(user2)

                            if user2 == 3:
                                client_sendMsg()

                            # TODO - do #4

                            if user2 == 5:
                                client_login = False
                                cc = False
                                clientMain = False

                            elif user2 > 5 or user2 < 2:
                                print("Enter the right option")

                            # if user doesn't want to login
                            # TODO: test if this works
                            if userName == "x" or "X" or userPass == "x" or "X":
                                client_login = False

                        else:
                            print("\nUsername or Password is incorrect!\n")

                else:
                    print("Please log in")

        # will disconnect client from server
        if userMenu == 5:
            client_login = False
            cc = False
            clientMain = False

        elif 1 < userMenu < 5:
            print("Please connect to server")

        elif 1 > userMenu > 5:
            print("Please choose the right option")
