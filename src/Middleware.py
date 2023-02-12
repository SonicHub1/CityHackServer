import Genre
import Instrument
import Proficiency

from flask import Flask

from DBMS import Database
from Genre import *
from Instrument import *
from Proficiency import *
from User import User
from Venue import Venue
from FeedPost import FeedPost

app = Flask(__name__)


auth_DB = Database("auth")
users = Database("users")
venues = Database("venues")
feed_DB = Database("feed")

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
    return eval(f"{proficiency}()")


def _create_instrument_obj(instrument:str, proficiency:str, performer:bool, teacher:bool, student:bool) -> Instrument:
    proficiency = _create_proficiency_obj(proficiency)
    return eval(f"{instrument}(proficiency, performer, teacher, student)")


# instruments = [("Guitar", "Beginner", True, False, False), ("Piano", "Intermediate", False, True, False)]
def add_instruments(username:str, instruments:list[str]) -> bool:
    if username in users:
        user_obj = users[username]
        for instrument in instruments:
            user_obj.add_instrument(_create_instrument_obj(instrument=instrument[0], proficiency=instrument[1], performer=instrument[2], teacher=instrument[3], student=instrument[4]))
        users.update_single_record(obj_id=username, obj=user_obj)
        return True
    else:
        return False


def _create_genre_obj(genre:str) -> Genre:
    return eval(f"{genre}()")


def add_genres(username:str, genres:list) -> bool:
    if username in users:
        user_obj = users[username]
        for genre in genres:
            user_obj.add_genre(_create_genre_obj(genre))
        users.update_single_record(obj_id=username, obj=user_obj)
        return True
    else:
        return False


def _get_all_performers() -> list:
    for user in users.values():
        if user.is_performer:
            yield user

def get_all_performers() -> tuple:
    return tuple(_get_all_performers())


def _get_all_teachers() -> list:
    for user in users.values():
        if user.is_teacher:
            yield user

def get_all_teachers() -> tuple:
    return tuple(_get_all_teachers())


def _get_all_students() -> list:
    for user in users.values():
        if user.is_student:
            yield user

def get_all_students() -> tuple:
    return tuple(_get_all_students())


def _get_all_performers_by_genre(genre:str) -> list:
    for user in _get_all_performers():
        if user.has_genre(genre):
            yield user

def get_all_performers_by_genre(genre:str) -> tuple:
    return tuple(_get_all_performers_by_genre(genre))


def _get_all_teachers_by_genre(genre:str) -> list:
    for user in _get_all_teachers():
        if user.has_genre(genre):
            yield user

def get_all_teachers_by_genre(genre:str) -> tuple:
    return tuple(_get_all_teachers_by_genre(genre))


def _get_all_students_by_genre(genre:str) -> list:
    for user in _get_all_students():
        if user.has_genre(genre):
            yield user

def get_all_students_by_genre(genre:str) -> tuple:
    return tuple(_get_all_students_by_genre(genre))

def _get_all_performers_by_instrument(instrument:str) -> list:
    for user in _get_all_performers():
        if user.plays_instrument(instrument):
            yield user

def get_all_performers_by_instrument(instrument:str) -> tuple:
    return tuple(_get_all_performers_by_instrument(instrument))

def _get_all_teachers_by_instrument(instrument:str) -> list:
    for user in _get_all_teachers():
        if user.plays_instrument(instrument):
            yield user

def get_all_teachers_by_instrument(instrument:str) -> tuple:
    return tuple(_get_all_teachers_by_instrument(instrument))

def _get_all_students_by_instrument(instrument:str) -> list:
    for user in _get_all_students():
        if user.plays_instrument(instrument):
            yield user


def get_all_students_by_instrument(instrument:str) -> tuple:
    return tuple(_get_all_students_by_instrument(instrument))


def get_venue(venue_id:str) -> Venue:
    if venue_id in venues:
        return venues[venue_id]
    else:
        return None

def create_venue(name:str, address:str, city:str, state:str, zipcode:int, phone:str, website:str, capacity:int) -> bool:
    new_venue = Venue(name=name, address=address, city=city, state=state, zip_code=zipcode, phone=phone, website=website, capacity=capacity)
    venues[new_venue.id] = new_venue
    return True

def create_feedPost(username:str, title:str, content:str, link:str) -> bool:
    if username in users:
        feed_post = FeedPost(username=username, title=title, summary=content, link=link)
        feed_DB[feed_post.id] = feed_post
        return True
    else:
        return False

@app.route("/feed")
def get_all_feedPosts() -> tuple:
    return list(map(lambda x: x.__dict__, feed_DB.values()))

app.run()