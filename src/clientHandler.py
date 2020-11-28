from Client import Client
import json

if __name__ == "__main__":
    client = Client("localhost", 10000)

    menu = "1. Connect to server\n" \
           "2. Login\n" \
           "3. Send message\n" \
           "4. Print received message\n" \
           "5. Disconnect\n"
    print(menu)
    userChoice = input("Enter choice: ")
    userChoice = int(userChoice)

    # TODO need to figure out how to create a menu and work the functions
    menuOption = True
    while menuOption:
        if userChoice == 1:
            client.connect()

            server_message = client.receive_message()
            print(f"""[CLI] SRV -> {server_message}""")

            # TODO need to figure out how to properly read file and find elements in file
            with open("userlist.json", "r") as openfile:
                jsonFile = json.load(openfile)
                client_login = True
                while client_login:
                    userInput = input("Enter username: ")
                    userPass = input("Enter password: ")

                    # if user is in out dictionary it will allow user to send msg to server
                    if userInput and userPass in jsonFile:
                        print(userInput, "logged in") # prints a message that the user is logged in
                        # TODO:
                        #   #3 sends message to server
                        client_runs = True
                        while client_runs:
                            msg = input("Message to send: ")
                            client.send_message(msg)

                            # TODO:
                            #   prints received messages saved in servers json file
                            #   once the saved message was received by client, the message
                            #   sent must be removed in server
                            server_message = client.receive_message()
                            print(f"""[CLI] SRV -> {server_message}""")

                            # TODO:
                            #   this is #5
                            if msg == "QUIT" or msg == "TERMINATE":
                                client_runs = False
                    else:
                        print("Error! Try again?")

                # TODO:
                #   need to create a background thread. this thread receives the messages of the server and stores it
                #   in the list??? then this thread will be connected to the server 
