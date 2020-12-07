"""Store user's account information: username, password, and email"""
class User:
    def __init__(self, username:str, password:str, email:str):
        self.__username = username
        self.__password = password
        self.__email = email

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username: str):
        self.__username = username

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email: str):
        self.__email = email

    @property
    def password(self):
        return self.__password


    def __str__(self):
        return f'USERNAME: {self.username}|PASSWORD: {self.password}|EMAIL: {self.email}'

    def __repr__(self):
        return f'USERNAME: {self.username}|PASSWORD: {self.password}|EMAIL: {self.email}'

    def __eq__(self, other):
        return self.username is other.username

