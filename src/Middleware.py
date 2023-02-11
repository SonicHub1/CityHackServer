from DBMS import Database
from User import User
from Venue import Venue
import Proficiency
from Proficiency import Proficiency
import Instrument
from Instrument import Instrument

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
            users.add_single_record(username, user_obj, overwrite=True)
        return True
    else:
        return False

def get_venue(venue_id:str) -> Venue:
    if venue_id in venues:
        return venues[venue_id]
    else:
        return None