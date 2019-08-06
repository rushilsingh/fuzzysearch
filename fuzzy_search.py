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
        red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
        
        red.flushdb()
        pipe = red.pipeline()
        n = 1
        for line in self.text:
            divide = line.split()
            pipe.hmset(divide[0], divide[1])
            n = n + 1
            if (n % 64) == 0:
                pipe.execute()
                pipe = red.pipeline()

if __name__ == "__main__":
    d = DataSet()
    d.load()
    d.parse()
