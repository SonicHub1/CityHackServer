import json
import random
import string

from Instrument import Instrument
from Proficiency import Proficiency
from Genre import Genre

from DBMS import Database

user_DB = Database("users")

N = 5_000
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

def teach_student()->tuple[bool, bool]:
    first_choice = random.choice((True, False))
    if first_choice is True:
        return (True, False)
    else:
        return (False, random.choice((True, False)))

student_teacher = [[teach_student() for _ in range(instrument_count[i])] for i in range(N)]

genre = Genre.get_all_genres()
genre_len = len(genre)
genre_nums = [random.randint(1, genre_len) for _ in range(N)]
genre_names = [random.sample(genre, k=genre_nums[i]) for i in range(N)]

fin_store = {'users': []}

for seed_user in zip(emails, passwords, names, instrument_names, proficiency_names, performers, student_teacher, genre_names, strict=True):
    fin_store['users'].append({
        'email': seed_user[0],
        'password': seed_user[1],
        'name': seed_user[2],
        'instruments': seed_user[3],
        'proficiencies': seed_user[4],
        'performers': seed_user[5],
        'teach-student':seed_user[6],
        'genres': seed_user[7],
    })
    
with open('seed_data.json', 'w', encoding='utf-8') as f:
    json.dump(fin_store, f, indent=4)

N = 10
emails = random.sample(list(user_DB.keys()), k=N)
title = ["Utkarsh Jain", "Aryman Navale", "Abhimanyu Bhati", "Aryan Kasliwal", "Wing Chi", "Chun Tsz", "Ming Yuen", "Tsau Ping", "Hoi Pui", "Sze Chung"]
description = ["I am a guitarist looking for a drummer", "I am a drummer looking for a guitarist", "I am a guitarist looking for a bassist", "I am a bassist looking for a guitarist", "I am a drummer looking for a bassist", "I am a bassist looking for a drummer", "I am a guitarist looking for a vocalist", "I am a vocalist looking for a guitarist", "I am a drummer looking for a vocalist", "I am a vocalist looking for a drummer"]
imgs = ["https://daily.jstor.org/wp-content/uploads/2023/01/good_times_with_bad_music_1050x700.jpg",
    "https://img.freepik.com/free-vector/musical-pentagram-sound-waves-notes-background_1017-33911.jpg?w=2000",
    "https://img.freepik.com/free-vector/musical-notes-frame-with-text-space_1017-32857.jpg?w=2000",
    "https://images.template.net/wp-content/uploads/2014/11/background-music1.jpg",
    "https://wallpapers.com/images/file/compact-cassette-music-aesthetic-d9cca07ejzpawq1x.jpg",
    "https://wallpaperaccess.com/full/5208008.jpg",
    "https://ih1.redbubble.net/image.468265504.2261/pp,840x830-pad,1000x1000,f8f8f8.u1.jpg",
    "https://img.freepik.com/free-vector/orange-aesthetic-background-musical-instrument-frame-retro-design-vector_53876-157650.jpg?w=2000",
    "https://thumbs.dreamstime.com/b/abstract-many-metallic-copper-key-note-music-floating-violet-purple-background-d-rendering-144153032.jpg",
    "https://i.pinimg.com/564x/c3/89/18/c3891830f480d90da165aea310f42c81.jpg"
]

feed = {"posts":[]}
for seed_post in zip(emails, title, description, imgs, strict=True):
    feed['posts'].append({
        'email': seed_post[0],
        'title': seed_post[1],
        'description': seed_post[2],
        'img': seed_post[3]
    })

with open('seed_feed_data.json', 'w', encoding='utf-8') as f:
    json.dump(feed, f, indent=4)


