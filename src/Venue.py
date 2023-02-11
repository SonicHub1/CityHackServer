class Venue:
    def __init__(self, name, address, city, state, zip_code, phone, website, capacity):
        self._name = name
        self._address = address
        self._city = city
        self._state = state
        self._zip_code = zip_code
        self._phone = phone
        self._website = website
        self._capacity = capacity

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name