from abc import ABC

class User(ABC):
    def __init__(self, name, email):
        self._name:str = name
        self._email:str = email

    @property
    def name(self) -> str:
        """Get the name of the user"""
        return self._name

    @property
    def email(self):
        """Get the email of the user"""
        return self._email
    


    def __str__(self):
        return f"Name: {self._name}, Email: {self._email}"