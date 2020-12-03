from Users import User

class Message:
    """Stores message content and the message id"""
    ID = 1
    def __init__(self, user_from: User, user_to: User, content: str):
        self.__id = str(Message.ID).zfill(6)
        self.__user_from = user_from
        self.__user_to = user_to
        self.__content = content
        Message.ID += 1

    # region Getters and Setters
    @property
    def id(self):
        return self.__id

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    @property
    def user_to(self):
        return self.__user_to

    @property
    def user_from(self):
        return self.__user_from

    # region Utility

    @classmethod
    def reset_id_numbering(cls):
        cls.ID = 1

    def __repr__(self):
        return f"""FROM: {self.__user_from.username}|TO: {self.__user_to.username}|MSG: {self.__content}"""
