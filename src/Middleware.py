from DBMS import Database

auth_DB = Database("auth")
users = Database("users")
venues = Database("venues")

def authenticate_user(username, password) -> int:
    if username in auth_DB:
        