from abc import ABC
from typing import Iterator

from Genre import Genre
from Instrument import Instrument


class User(ABC):
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

    def add_genre(self, genre):
        """Add a genre to the user"""
        self._genre_list.append(genre)

    def add_genres(self, genres:Iterator[Genre]):
        """Add a genre to the user"""
        for genre in genres:
            self.add_genre(genre)
    
    def add_instrument(self, instrument:Instrument):
        """Add an instrument to the user"""
        self._instrument_list.append(instrument)

    def add_instruments(self, instruments:Iterator[Instrument]):
        """Add an instrument to the user"""
        for instrument in instruments:
            self.add_instrument(instrument)
