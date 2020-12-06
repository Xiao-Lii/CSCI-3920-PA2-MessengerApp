class User:
    def __init__(self, email: str, password: str, username: str):
        self.email = email
        self.__username = username
        self.__password = password

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username: str):
        self.__username = username

    @property
    def phone(self):
        return self.__email

    @phone.setter
    def phone(self, phone: str):
        self.__email = email

    @property
    def password(self):
        return self.__password

    def __str__(self):
        return f'EMAIL: {self.email}|PASSWORD: {self.password}|USERNAME: {self.username}'

    # Leave in case __str__ method doesn't print correctly
    def __repr__(self):
        return f'EMAIL: {self.email}|PASSWORD: {self.password}|USERNAME: {self.username}'

    def __eq__(self, other):
        return self.username is other.username
