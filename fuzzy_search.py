import os
import redis


class DataSet(object):

    def __init__(self):
        self.fname = "word_search.tsv"
        self.text = None

    
    def load(self):
        with open(self.fname) as f:
            self.text = f.readlines()
        
    def parse(self):
        #red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
        red = redis.Redis()
        red.flushdb()
        pipe = red.pipeline()
        n = 1
        for line in self.text:
            word, frequency = line.split()   
            pipe.hset("h", word, frequency)
            n = n + 1
            if (n % 64) == 0:
                pipe.execute()
                pipe = red.pipeline()

if __name__ == "__main__":
    d = DataSet()
    d.load()
    d.parse()
