from Server import Server

if __name__ == "__main__":
    menu = "1. Load data from file.\n" \
           "2. Start the messenger service\n" \
           "3. Stop the messenger service\n" \
           "4. Save data to file\n"
    server = Server("localhost", 10000, 5)

    print(menu)
    userOption = int(input())

    displayStart = True
    while displayStart:
        # 1st we want to keep displaying the Start Menu to the User
        # END OF RECEIVE MESSAGE

        if userOption == 1:
            # READ THAT FILE
            print("Inside option 1")  # Test Filler - May delete
        elif userOption == 2:
            # BETTER START THAT MESSENGER
            # MAYBE FOR RIGHT HERE, WE WANT:
            #       1. MAYBE TO CREATE A NEW MESSENGING SYSTEM OBJECT IF ONE WASN'T LOADED IN
            #       2. CALL FUNCTION TO OPEN THE NEXT MENU - USER LOGIN
            server.run()
            print("Inside option 2")  # Test Filler - May delete
        elif userOption == 3:
            # BETTER STOP THAT MESSENGER
            print("Inside option 3")  # Test Filler - May delete
            server.close()
        elif userOption == 4:
            # SAVE THE FILE
            print("Inside option 4")  # Test Filler - May delete
        else:
            # DONE GOOF NOW - ERROR
            print("Error: Invalid menu selection")


class messengerApp:
    def __init__(self, listOfUsers:dict, listOfMessages:dict):
        self.__listOfUsers = listOfUsers
        self.__listOfMesseges = listOfMessages




