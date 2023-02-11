"""Instrument module, definng base module class and subclasses"""

from abc import ABC
from Proficiency import Proficiency

class Instrument(ABC):
    """Instrument class"""

    _obj = None

    def __new__(cls, *args, **kwargs):
        if cls._obj is None:
            cls._obj = super().__new__(cls, *args, **kwargs)
        return cls._obj

    def __init__(self, name:str, proficiency:Proficiency):
        self._name:str = name
        self._proficiency:Proficiency = proficiency

    @property
    def name(self) -> str:
        """Get the name of the instrument"""
        return self._name

    @property
    def proficiency(self) -> Proficiency:
        """Get the proficiency of the instrument"""
        return self._proficiency

    @classmethod
    def get_all_instruments(cls):
        """Get all instruments"""
        return tuple(x() for x in Instrument.__subclasses__())

class Piano(Instrument):
    """Piano class"""

    def __init__(self, proficiency:Proficiency):
        super().__init__("Piano", proficiency)

class Guitar(Instrument):
    """Guitar class"""

    def __init__(self, proficiency:Proficiency):
        super().__init__("Guitar", proficiency)

class Drums(Instrument):
    """Drums class"""

    def __init__(self, proficiency:Proficiency):
        super().__init__("Drums", proficiency)