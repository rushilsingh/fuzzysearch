import os
import requests
import io
import zipfile
import datetime
import textfsm
import redis
import pytz
import pickle

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
        template = "fuzzy_template"

        with open(template) as f:
            parser = textfsm.TextFSM(f)

        lists = parser.ParseText(self.text)
        parsed = []
        for i in range(len(lists)):
            elem = {}
            for j in range(len(parser.header)):
                elem[parser.header[j]] = lists[i][j]
            parsed.append(elem)
        processed = {}
        for elem in parsed:
            word = elem["Word"]
            frequency = elem["Frequency"]
            if frequency in processed:
                processed[frequency].append(word)
            else:
                processed[frequency] = [word]
        parsed = processed
        red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
        wipe_redis(red)
        import pickle
        for key in parsed:
            red.set(key, pickle.dumps(parsed[key]))



if __name__ == "__main__":
    d = DataSet()
    d.load()
    d.parse()
