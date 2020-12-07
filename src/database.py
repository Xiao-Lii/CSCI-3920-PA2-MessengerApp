from user import User
from message import Message
import queue


class Database:
    def __init__(self, users = None, outgoing_messages = None, outgoing_notifications = None):
        # Initializing if no users exists
        if users is None:
            self.__users = []
            # Initializing with an Admin & Basic User
            admin = User("admin", "pw", "admin")
            user = User("user", "pw", "user")
            self.__users.append(admin)
            self.__users.append(user)
        # Otherwise, Initializing with list of Users
        else:
            self.__users = users

        # Initializing / Preparing the Queue for Outgoing Messages
        if outgoing_messages is None:
            self.__outgoing_messages = queue.Queue()
        else:
            self.__outgoing_messages = outgoing_messages

        # Initializing / Preparing the Queue for Outgoing Notifications
        if outgoing_notifications is None:
            self.__outgoing_notifications = queue.Queue()
        else:
            self.__outgoing_notifications = outgoing_notifications

    @property
    def users(self):
        return self.__users

    @property
    def outgoing_messages(self):
        return self.__outgoing_messages

    @property
    def outgoing_notifications(self):
        return self.__outgoing_notifications


    # NEED TO DOUBLE CHECK THIS PART, DATABASE IS ALLOWING 2 USERS TO SIGN UP WITH THE SAME EMAIL / USERNAME
    def sign_up_user(self, username:str, password:str, email:str):
        success = True
        response = ""

        # Verify that User Email is not already in database
        for user in self.__users:
            #if username is user.username:
            if username == user.username or email == user.email:
                success = False
                response = "1|ERROR: A user with either this username or email already exists"
                break

        # If username and email weren't found as already used in database's list of users
        # Continue to add user to database
        if success:
            user_to_add = User(username, password, email)
            self.__users.append(user_to_add)
            response = "0|SUCCESS"

        print("Database List of Users:")
        for user in self.__users:
            print(user)
        return response

    def send_message(self, name_from:str, name_to:str, message:str):
        sender_found = False
        recipient_found = False
        sending_user = None
        receiving_user = None
        response = ''

        # Verify that sender exists in database
        for user in self.__users:
            if name_from == user.username:
                sender_found = True
                sending_user = user
                break
            else:
                response = f"""1|no source user"""
        # Verify that recipient exists in database
        for user in self.__users:
            if name_to == user.username:
                recipient_found = True
                receiving_user = user
                break
            else:
                response = f"""2|no target user"""

        # If Sender and recipient are valid, add message to message queue
        if recipient_found and sender_found:
            message_to_send = Message(sending_user, receiving_user, message)
            self.__outgoing_messages.put(message_to_send)
            response = f"""0|{message_to_send.id}"""

        return response

    def send_notification(self, user_from:User, user_to:User, message_id:str):
        success = 0
        response = ''

        # Verify that recipient exists in database
        if user_from not in self.__users:
            success = 1
            response = f"""{success}|ERROR: Recipient doesn't exist"""

        # Verify that sender exists in database
        elif user_to not in self.__users:
            success = 2
            response = f"""{success}|ERROR: Sender doesn't exist"""

        # If both are in database, add to our notification queue
        if success == 0:
            message_to_send = Message(user_from, user_to, message_id)
            self.__outgoing_notifications.put(message_to_send)
            response = f"""{success}|[NOTIFICATION] Sent to server"""

        return response