import os
import json
import re
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

class ArchiveItem(object):
    def __init__(self, filename, date):
        self._date = date
        self._members = json.load(file(os.path.join(DATA_DIR, filename)))

    @property
    def date(self):
        return self._date

    @property
    def members(self):
        return self._members

class Archive(object):
    _archive = []

    @classmethod
    def reload(cls):
        cls._archive = []

        files = os.listdir(DATA_DIR)
        for fn in files:
            # filename format: YYYY-MM-DD.json
            dates = re.findall('(....-..-..)\.json', fn)
            if len(dates) == 1:
                date = dates[0]
                cls._archive.append(ArchiveItem(fn, date))

    @classmethod
    def archive(cls):
        return cls._archive

    @classmethod
    def latest(cls):
        if cls._archive:
            return max(cls._archive, key = lambda item : item.date)
        else:
            return None

    @classmethod
    def is_empty(cls):
        return not cls._archive

    @classmethod
    def save_new(cls, members):
        date = time.strftime('%Y-%m-%d')
        fn = date + '.json'
        json.dump(members, file(os.path.join(DATA_DIR, fn), 'wb'))

        cls._archive.append(ArchiveItem(fn, date))
