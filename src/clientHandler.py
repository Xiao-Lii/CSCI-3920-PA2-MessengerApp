from Client import Client

userList = {"username": "rin",
            "password": "Lel"}

if __name__ == "__main__":
    client = Client("localhost", 10000)

    client.connect()

    server_message = client.receive_message()
    print(f"""[CLI] SRV -> {server_message}""")
    print(userList)

    # checks if the user credentials is good
    # if not, user can try again over and over
    client_login = True
    while client_login:
        userInput = input("Enter username: ")
        userPass = input("Enter password: ")

        # if user is in out dictionary it will allow user to send msg to server
        if userInput and userPass in userList.values():
            client_runs = True
            while client_runs:
                msg = input("Message to send: ")
                client.send_message(msg)
                server_message = client.receive_message()
                print(f"""[CLI] SRV -> {server_message}""")

                if msg == "QUIT" or msg == "TERMINATE":
                    client_runs = False

        else:
            print("Error! Try again?")
