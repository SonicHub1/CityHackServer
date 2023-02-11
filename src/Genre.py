from abc import ABC

class Genre(ABC):
    """Class defining base for genre"""
    _obj = None

    def __new__(cls, *args, **kwargs):
        if cls._obj is None:
            cls._obj = super().__new__(cls, *args, **kwargs)
        return cls._obj

    def __init__(self, name:str):
        self._name:str = name

    @property
    def name(self) -> str:
        """Get the name of the genre"""
        return self._name

    def __str__(self):
        return f"Name: {self._name}"

    @classmethod
    def get_all_genres(cls):
        """Get all genres"""
        return tuple(x.__name__ for x in Genre.__subclasses__())

class Rock(Genre):
    """Class defining rock genre"""
    def __init__(self):
        super().__init__("Rock")

class Pop(Genre):
    """Class defining pop genre"""
    def __init__(self):
        super().__init__("Pop")

class Jazz(Genre):
    """Class defining jazz genre"""
    def __init__(self):
        super().__init__("Jazz")

class Classical(Genre):
    """Class defining classical genre"""
    def __init__(self):
        super().__init__("Classical")
