class Venue:
    _all_venues = []
    def __init__(self, name, address, city, state, zip_code, phone, website, capacity):
        self._name = name
        self._address = address
        self._city = city
        self._state = state
        self._zip_code = zip_code
        self._phone = phone
        self._website = website
        self._capacity = capacity
        Venue._all_venues.append(self)
        self._id = str(len(Venue._all_venues)+1)

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    @property
    def id(self):
        return self._id