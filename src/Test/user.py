# region User

class User:
    """Stores user data"""

    def __init__(self, username: str, password: str, phone: str):
        self.__username = username
        self.__password = password
        self.__phone = phone

    # region Getters and Setters

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username: str):
        self.__username = username

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone: str):
        self.__phone = phone

    @property
    def password(self):
        return self.__password

    # endregion

    def __str__(self):
        return f'USERNAME: {self.username}|PASSWORD: {self.password}|PHONE: {self.phone}'

    def __repr__(self):
        return f'USERNAME: {self.username}|PASSWORD: {self.password}|PHONE: {self.phone}'

    def __eq__(self, other):
        return self.username is other.username

# endregion