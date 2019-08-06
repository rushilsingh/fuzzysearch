import os
import requests
import io
import zipfile
import datetime
import textfsm
import redis
import pytz

def wipe_redis(red):
    cursor = '0'
    while cursor != 0:
        cursor, keys = red.scan(cursor=cursor, match="*", count=5000)
        if keys:
            red.delete(*keys)

class DataSet(object):

    def __init__(self):
        self.fname = "word_search.tsv"
        self.text = None

    
    def load(self):
        with open(self.fname) as f:
            self.text = f.read()
        
    def parse(self):
        template = "word_search_template"

        with open(template) as f:
            parser = textfsm.TextFSM(f)

        lists = parser.ParseText(self.text)
        parsed = []
        for i in range(len(lists)):
            elem = {}
            for j in range(len(parser.header)):
                elem[parser.header[j]] = lists[i][j]
            parsed.append(elem)
        index = 1

        red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
        wipe_redis(red)


if __name__ == "__main__":
    d = DataSet()
    d.load()
    print(d.text)
