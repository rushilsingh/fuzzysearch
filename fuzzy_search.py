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
            self.text = f.readlines()
        
    def parse(self):
        red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
        
        wipe_redis(red)

        for line in self.text:
            divide = line.split()
            red.hset("h", divide[0], divide[1])

if __name__ == "__main__":
    d = DataSet()
    d.load()
    d.parse()
