from Server import Server

if __name__ == "__main__":
    server = Server("localhost", 10000, 5)

    server.run()


class MessengerApp:
    def __init__(self, listOfUsers: dict, listOfMessages: dict):
        self.__listOfUsers = listOfUsers
        self.__listOfMesseges = listOfMessages
