import datetime

class FeedPost:
    def __init__(self, username:str, title:str, link:str, summary:str):
        self._title = title
        self._img_link = link
        self._summary = summary
        self._username = username
        self._postime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self._title

    @property
    def id(self):
        return self._title + self._img_link + self._username
