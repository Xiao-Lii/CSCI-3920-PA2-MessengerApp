class User:
    def __init__(self, email: str, password: str, username : str):
        self.__email = email
        self.__password = password
        self.__username = username

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    def username(self, username: str):
        self.__username = username

    def email(self, email: str):
        self.__email = email

    def __str__(self):
        return f'USERNAME: {self.username}|PASSWORD: {self.password}|EMAIL: {self.email}'

    def __repr__(self):
        return f'USERNAME: {self.username}|PASSWORD: {self.password}|EMAIL: {self.email}'

    def __eq__(self, other):
        return self.username is other.username
