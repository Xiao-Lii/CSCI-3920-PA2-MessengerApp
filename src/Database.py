from User import User
from Message import Message
import queue


class Database:
    """Our database which is responsible for holding our list of users, messages, and banners to display to the user"""
    def __init__(self, users=None, sending_messages=None, sending_banners=None):
        # Initializing if no users exists
        if users is None:
            self.__users = []
            # Initializing with an Admin & Basic User
            admin = User("admin", "pw", "admin")
            user = User("user", "pw", "user")
            user2 = User("user2", "pw", "user2")
            self.__users.append(admin)
            self.__users.append(user)
            self.__users.append(user2)
        # Otherwise, Initializing with list of Users
        else:
            self.__users = users

        # Initializing / Preparing the Queue for Outgoing Messages
        if sending_messages is None:
            self.__sending_messages = queue.Queue()
        else:
            self.__sending_messages = sending_messages

        # Initializing / Preparing the Queue for Outgoing Notifications
        if sending_banners is None:
            self.__sending_banners = queue.Queue()
        else:
            self.__sending_banners = sending_banners

    @property
    def users(self):
        return self.__users

    @property
    def outgoing_messages(self):
        return self.__sending_messages

    @property
    def outgoing_banners(self):
        return self.__sending_banners

    # NEED TO DOUBLE CHECK THIS PART, DATABASE IS ALLOWING 2 USERS TO SIGN UP WITH THE SAME EMAIL / USERNAME
    # ACTUALLY THIS PORTION MAY BE FIXED NOW - LEE
    def sign_up_user(self, username: str, password: str, email: str):
        """Creates and adds a user account to the database as long as the email or username hasn't already been
        created"""
        check = True
        response = ""

        # Verify that User Email is not already in database
        for user in self.__users:
            if username == user.username or email == user.email:
                check = False
                response = "1|ERROR: A user with either this username or email already exists"
                break

        # If username and email weren't found as already used in database's list of users
        # Continue to add user to database
        if check:
            user_to_add = User(username, password, email)
            self.__users.append(user_to_add)
            response = "0|SUCCESS"

        print("Database List of Users:")
        for user in self.__users:
            print(user)
        return response

    def send_message(self, name_from: str, name_to: str, message: str):
        """Processes and sends messages between users, requiring a user signed in as the sender to another existing
        account"""
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
                response = f"""1|Sender doesn't exist"""
        # Verify that recipient exists in database
        for user in self.__users:
            if name_to == user.username:
                recipient_found = True
                receiving_user = user
                break
            else:
                response = f"""2|Receiver doesn't exist"""

        # If Sender and recipient are valid, add message to message queue
        if recipient_found and sender_found:
            message_to_send = Message(sending_user, receiving_user, message)
            self.__sending_messages.put(message_to_send)
            response = f"""0|{message_to_send.id}"""

        return response

    def send_banner(self, user_from: User, user_to: User, message_id: str):
        """We want our users to know when they signed in if they've received a message while they were offline and
        should print/display at the top of their screen upon a successful sign in. This will verify the sender and
        receiver are valid users in the database"""
        check = 0
        response = ''

        # Verify that recipient exists in database
        if user_from not in self.__users:
            check = 1
            response = f"""{check}|ERROR: Recipient doesn't exist"""

        # Verify that sender exists in database
        elif user_to not in self.__users:
            check = 2
            response = f"""{check}|ERROR: Sender doesn't exist"""

        # If both are in database, add to our notification queue
        if check == 0:
            message_to_send = Message(user_from, user_to, message_id)
            self.__sending_banners.put(message_to_send)
            response = f"""{check}|[NOTIFICATION] Sent to server"""

        return response
