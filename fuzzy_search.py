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
        #red = redis.Redis()
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
    
    def find(self, key):

    values = []
    red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
    #red = redis.Redis()
    pipe = red.pipeline()
    search = "*" + key + "*"
    cursor = 0
    if red.hexists("h", key):
        while True:
            cursor, value = red.hscan("h", cursor, search, 1000)
            if cursor == 0:
                break
            if value != {}:
                values.append(value)
    else:
        values = {}
    mapping = values 
    values = []
    for dic in mapping:
        for entry in dic:
            values.append(str(entry)[2:])
    
    if not values:
        return {}

    if len(values) == 1:
        return {1:values[0]}

    results = {}
    unsorted = []
    exact = []
    start = []
    for value in values:
        if value == key:
            exact.append(value)
        elif value.startswith(key) and value != key:
            start.append(value)
        else:   
            unsorted.append(value)

    results["exact"] = exact
    results["start"] = start 
    results["unsorted"] = unsorted
    current = 1
    sorted_results = {}
    if results["exact"]:
        sorted_results[current] = results["exact"]
    if results["start"]:
        sorted_results[current] = results["start"]
    
    sorted_results[current] = results["unsorted"]
    #sorted_results = self.further_sort(sorted_results, 1, mapping)
    return sorted_results

    def further_sort(results, mapping):
        final = {}
        current = 1
        for rank in results:
            if len(results[rank]) == 1:
                final[current] = results[rank]
                current += 1
            else:
                current, extend_by = tertiary_sort (results[rank], current, mapping)
                final.extend(extend_by)                


    def tertiary_sort(results, current, mapping):
        initial_current = current
        occurrences = mapping.values()
        occurrences = occurrences.sort()
        ocurrences = set(occurrences)
        final = {}
        for number in occurrences:
            elements = []
            for word in result:
                if results[word] == occurrences:
                    elements.append(word)
            final[current] = elements

        results = final
        final = {}
        for rank in results:
            if len(results[rank]) == 1:
                final[current] = results[rank]
                current += 1
            else:
                final[rank] = results[rank]
                current += 1
                #TODO: fix this branch
        return current, final

            




                    

            
if __name__ == "__main__":
    d = DataSet()
    d.load()
    d.parse()
