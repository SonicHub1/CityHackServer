"""Module defining proficiency classes, and respective subclasses"""
from abc import ABC

class Proficiency(ABC):
    """Class defining base for proficiency"""

    _obj = None

    def __new__(cls, *args, **kwargs):
        if cls._obj is None:
            cls._obj = super().__new__(cls, *args, **kwargs)
        return cls._obj

    def __init__(self, name:str):
        self._name:str = name

    @property
    def name(self) -> str:
        """Get the name of the proficiency"""
        return self._name

    def __str__(self):
        return f"Name: {self._name}"

    @classmethod
    def get_all_proficiencies(cls):
        """Get all proficiencies"""
        return tuple(x.__name__ for x in Proficiency.__subclasses__())

class Easy(Proficiency):
    """Class defining easy proficiency"""

    def __init__(self):
        super().__init__("Easy")

class Intermediate(Proficiency):
    """Class defining medium proficiency"""

    def __init__(self):
        super().__init__("Intermediate")

class Advanced(Proficiency):
    """Class defining advanced proficiency"""
    
    def __init__(self):
        
        super().__init__("Advanced")

