import json
import random
import string

from Instrument import Instrument
from Proficiency import Proficiency
from Genre import Genre

N = 100
emails = [''.join(random.choices(string.ascii_letters, k=32)) for _ in range(N)]
passwords = [''.join(random.choices(string.ascii_letters, k=32)) for _ in range(N)]
names = [''.join(random.choices(string.ascii_letters, k=12)) for _ in range(N)]
instrus = Instrument.get_all_instruments()
total_instrus = len(instrus)
instrument_count = [random.randint(1, total_instrus) for _ in range(N)]
instrument_names = [random.sample(instrus, k=instrument_count[i]) for i in range(N)]
profics = Proficiency.get_all_proficiencies()
proficiency_names = [[random.choice(profics) for _ in range(instrument_count[i])] for i in range(N)]
performers = [[random.choice([True, False]) for _ in range(instrument_count[i])] for i in range(N)]
genre = Genre.get_all_genres()
genre_len = len(genre)
genre_nums = [random.randint(1, genre_len) for _ in range(N)]
genre_names = [random.sample(genre, k=genre_nums[i]) for i in range(N)]

fin_store = {'users': []}

for seed_user in zip(emails, passwords, names, instrument_names, proficiency_names, performers, genre_names, strict=True):
    fin_store['users'].append({
        'email': seed_user[0],
        'password': seed_user[1],
        'name': seed_user[2],
        'instruments': seed_user[3],
        'proficiencies': seed_user[4],
        'performers': seed_user[5],
        'genres': seed_user[6],
    })
    
with open('seed_data.json', 'w', encoding='utf-8') as f:
    json.dump(fin_store, f, indent=4)



