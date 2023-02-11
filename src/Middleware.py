import Genre
import Instrument
import Proficiency

from DBMS import Database
from Genre import Genre
from Instrument import Instrument
from Proficiency import Proficiency
from User import User
from Venue import Venue

auth_DB = Database("auth")
users = Database("users")
venues = Database("venues")

def authenticate_user(username:str, password:str) -> int:
    if username in auth_DB:
        if auth_DB[username] == password:
            return 1
        else:
            return 0
    else:
        return -1


def create_user(name:str, username:str, password:str) -> bool:
    if username not in auth_DB:
        auth_DB[username] = password
        new_user = User(name=name, email=username)
        users[username] = new_user
        return True
    else:
        return False


def get_user(username:str) -> User:
    if username in users:
        return users[username]
    else:
        return None


def get_proficiencies() -> list:
    return Proficiency.get_all_proficiencies()


def get_instruments() -> list:
    return Instrument.get_all_instruments()


def get_genres() -> list:
    return Genre.get_all_genres()


def _create_proficiency_obj(proficiency:str) -> Proficiency:
    return eval(f"Proficiency.{proficiency}()")


def _create_instrument_obj(instrument:str, proficiency:str, performer:bool, teacher:bool, student:bool) -> Instrument:
    proficiency = _create_proficiency_obj(proficiency)
    return eval(f"Instrument.{instrument}(proficiency, performer, teacher, student))")


# instruments = [("Guitar", "Beginner", True, False, False), ("Piano", "Intermediate", False, True, False)]
def add_instruments(username:str, instruments:list) -> bool:
    if username in users:
        user_obj = users[username]
        for instrument in instruments:
            user_obj.add_instrument(_create_instrument_obj(instrument=instrument[0], proficiency=instrument[1], performer=instrument[2], teacher=instrument[3], student=instrument[4]))
        users.update_single_record(obj_id=username, obj=user_obj)
        return True
    else:
        return False


def _create_genre_obj(genre:str) -> Genre:
    return eval(f"Genre.{genre}()")


def add_genres(username:str, genres:list) -> bool:
    if username in users:
        user_obj = users[username]
        for genre in genres:
            user_obj.add_genre(_create_genre_obj(genre))
        users.update_single_record(obj_id=username, obj=user_obj)
        return True
    else:
        return False


def get_all_performers() -> list:
    performers = []
    for user in users:
        if user.is_performer:
            performers.append(user)
    return performers


def get_all_teachers() -> list:
    teachers = []
    for user in users:
        if user.is_teacher:
            teachers.append(user)
    return teachers


def get_all_students() -> list:
    students = []
    for user in users:
        if user.is_student:
            students.append(user)
    return students


def get_all_performers_by_genre(genre:str) -> list:
    performers = []
    for user in users:
        if user.is_performer:
            if user.has_genre(genre):
                performers.append(user)
    return performers


def get_all_teachers_by_genre(genre:str) -> list:
    teachers = []
    for user in users:
        if user.is_teacher:
            if user.has_genre(genre):
                teachers.append(user)
    return teachers


def get_all_students_by_genre(genre:str) -> list:
    students = []
    for user in users:
        if user.is_student:
            if user.has_genre(genre):
                students.append(user)
    return students


def get_all_performers_by_instrument(instrument:str) -> list:
    performers = []
    for user in users:
        if user.is_performer:
            if user.plays_instrument(instrument):
                performers.append(user)
    return performers

def get_venue(venue_id:str) -> Venue:
    if venue_id in venues:
        return venues[venue_id]
    else:
        return None