from Client import Client
import json

client = Client("localhost", 10000)


def clientConnect():
    client.connect()
    server_msg = client.receive_message()
    print(f"""[CLI] SRV -> {server_msg}""")
    return True


def updatedMenu():
    cc = True
    while cc:  # menu when client is connected to server
        menu = "\n----MENU----\n" \
               "1 | Send message\n" \
               "2 | Print received message\n" \
               "3 | Disconnect\n"
        print(menu)
        user1 = input("Please the number of your choice: ")
        user1 = int(user1)
        if user1 == 1:
            client_sendMsg()

        if user1 == 3:
            cc = False
            clientLogIn()

        elif user1 == 2:
            print("I'll come back to fix this"
                  "\n CREATE A FUNCTION THAT RECEIVES MESSAGES")  # TODO: fix this please

        elif 1 > user1 > 3:
            print("Choose from the options above")


def clientLogIn():
    menuList = input("\n----MENU----\n" \
                     "1 | Login\n" \
                     "2 | Send message\n" \
                     "3 | Print received message\n" \
                     "4 | Disconnect\n"
                     "\nPlease enter your choice: ")

    menuList = int(menuList)

    clientMain = True
    while clientMain:
        if menuList == 4:
            # will disconnect client from server
            # client_login = False
            msg = "Terminate"
            clientMain = False
            # client.send_message(msg)
            return False

        if menuList == 1:
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
                    clientConnect()
                    updatedMenu()
                else:
                    print("\nUsername or password is incorrect!\n")

        elif 1 < menuList < 4:
            print("Log in to connect to server")

        elif 1 > menuList > 4:
            print("Please choose the right option")


def client_sendMsg():
    client_runs = True
    while client_runs:
        msg = input("Message to send: ")
        client.send_message(msg)
        server_msg = client.receive_message()
        print(f"""[CLI] SRV-> {server_msg}""")
        # user will be back to 2nd menu - still connected to server
        if msg == "Disconnect" or msg == "Quit":
            print("\nYou are now logged out!\n")
            client_runs = False
            clientLogIn()
            if not clientLogIn():# take the user back to the main menu
                client.send_message("Terminate")


# def mainMenu():
#     menuList = input("\n----MENU----\n" \
#                      "1 | Login\n" \
#                      "2 | Send message\n" \
#                      "3 | Print received message\n" \
#                      "4 | Disconnect\n"
#                      "\nPlease enter your choice: ")
#
#     menuList = int(menuList)
#
#     clientMain = True
#     while clientMain:
#         if menuList == 4:
#             if server is still connected ->close it first else
#             # will disconnect client from server
#             # client_login = False
#             client.disconnect()
#             clientMain = False
#
#         if menuList == 1:
#             clientLogIn()
#
#         elif 1 < menuList < 4:
#             print("Log in to connect to server")
#
#         elif 1 > menuList > 4:
#             print("Please choose the right option")


if __name__ == "__main__":
    clientLogIn()
    # Todo: make sure that the program truly exits
    #   maybe add a return statement on one of the menu???