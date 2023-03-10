from typing import Iterator

from Genre import Genre
from Instrument import Instrument


class User:
    def __init__(self, name, email):
        self._name:str = name
        self._email:str = email
        self._genre_list: list[Genre] = []
        self._instrument_list: list[Instrument] = []


    def __str__(self):
        return f"Name: {self._name}, Email: {self._email}"

    @property
    def name(self) -> str:
        """Get the name of the user"""
        return self._name

    @property
    def email(self):
        """Get the email of the user"""
        return self._email

    @property
    def id(self):
        """Get the id of the user"""
        return self._email

    @property
    def is_performer(self) -> bool:
        """Get whether the user is a performer"""
        return any(x.is_performer for x in self._instrument_list)
    
    @property
    def is_teacher(self) -> bool:
        """Get whether the user is a teacher"""
        return any(x.is_teacher for x in self._instrument_list)

    @property
    def is_student(self) -> bool:
        """Get whether the user is a student"""
        return any(x.is_student for x in self._instrument_list)

    def add_genre(self, genre:Genre):
        """Add a genre to the user"""
        if genre.name not in map(str, self._genre_list):
            self._genre_list.append(genre)

    def add_genres(self, genres:Iterator[Genre]):
        """Add a genre to the user"""
        for genre in genres:
            self.add_genre(genre)

    def has_genre(self, genre) -> bool:
        """Check if the user likes a genre"""
        return genre in map(lambda x: x.name, self._genre_list)

    def remove_genre(self, genre):
        """Remove a genre from the user"""
        self._genre_list.remove(genre)
    
    def remove_genres(self, genres:Iterator[Genre]):
        """Remove a genre from the user"""
        for genre in genres:
            self.remove_genre(genre)
    
    def add_instrument(self, instrument:Instrument):
        """Add an instrument to the user"""
        if instrument.name not in map(str, self._instrument_list):
            self._instrument_list.append(instrument)

    def add_instruments(self, instruments:Iterator[Instrument]):
        """Add an instrument to the user"""
        for instrument in instruments:
            self.add_instrument(instrument)

    def remove_instrument(self, instrument:Instrument):
        """Remove an instrument from the user"""
        self._instrument_list.remove(instrument)

    def remove_instruments(self, instruments:Iterator[Instrument]):
        """Remove an instrument from the user"""
        for instrument in instruments:
            self.remove_instrument(instrument)

    def plays_instrument(self, instrument:str) -> bool:
        """Check if the user plays an instrument"""
        return instrument in map(lambda x: x.name, self._instrument_list)
