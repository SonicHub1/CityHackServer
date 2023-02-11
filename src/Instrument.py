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

    def __init__(self, name:str, proficiency:Proficiency, performer:bool = False, teacher:bool = False, student:bool = False):
        self._name:str = name
        self._proficiency:Proficiency = proficiency
        self._teacher:bool = teacher
        self._student:bool = student
        self.is_performer:bool = performer

    @property
    def name(self) -> str:
        """Get the name of the instrument"""
        return self._name

    @property
    def proficiency(self) -> Proficiency:
        """Get the proficiency of the instrument"""
        return self._proficiency

    @property
    def is_teacher(self) -> bool:
        """Get whether the instrument is a teacher"""
        return self._teacher
    
    @is_teacher.setter
    def is_teacher(self, value:bool):
        """Set whether the instrument is a teacher"""
        self._teacher = value
        if self._teacher is True:
            self._student = False

    @property
    def is_student(self) -> bool:
        """Get whether the instrument is a student"""
        return self._student
    
    @is_student.setter
    def is_student(self, value:bool):
        """Set whether the instrument is a student"""
        self._student = value
        if self._student is True:
            self._teacher = False
    

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