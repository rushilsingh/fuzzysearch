import os
import redis
import copy

class DataSet(object):

    def __init__(self):
        self.fname = "word_search.tsv"
        self.text = None

    def load(self):
        """ Loads data file into text field as a list of lines """

        with open(self.fname) as f:
            self.text = f.readlines()

    def parse(self):
        """ Parses data file into Redis database"""

        red = redis.from_url(os.environ.get(
            'REDIS_URL'), decode_responses=True)
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
        """ Find instances of the occurrence of the key anywhere in the word fields stored in the database
            Performs initial sorting (three groups: exact match, starting match, and others)
        """

        values = []
        red = redis.from_url(os.environ.get(
            'REDIS_URL'), decode_responses=True)
        #red = redis.Redis()
        pipe = red.pipeline()
        search = "*" + key + "*"
        cursor = 0
        while True:
            cursor, value = red.hscan("h", cursor, search, 1000)
            if cursor == 0:
                break
            if value != {}:
                values.append(value)
        mapping = values
        values = []
        temp = {}
        for dic in mapping:
            for entry in dic:
                word = entry
                values.append(word)
                temp[word] = dic[entry]

        mapping = temp

        if not values:
            return {}

        if len(values[0]) == 1:
            return {1: values[0]}
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
            current += 1
        if results["start"]:
            sorted_results[current] = results["start"]
            current += 1

        sorted_results[current] = results["unsorted"]

        sorted_results = self.further_sort(sorted_results, mapping)
        results = copy.deepcopy(sorted_results)
        for key in sorted_results:
            if key > 25:
                if key in results:
                    results.pop(key)
        return results

    def further_sort(self, results, mapping):
        """ Furthers sorting pipeline by fixing single element entries and sends multiple element entries to
            next function to be sorted by number of occurrences
        """

        current = 1
        final = {}
        for rank in results:
            if len(results[rank]) == 1:
                final[current] = results[rank][0]
                current += 1
            elif current <= 25:
                current, extend_by = self.tertiary_sort(
                    results[rank], current, mapping)
                final.update(extend_by)
            else:
                pass
        return final

    def tertiary_sort(self, results, current, mapping):
        """ Sorts words by number of occurrences. If there are clashes, sends those lists to next function to be sorted to length """

        initial_curr = current
        occurrences = list(mapping.values())
        ocurrences = list(set(occurrences))
        occurrences.sort()
        final = {}
        for number in occurrences:
            number = int(number)
            elements = []
            for word in results:
                match = int(mapping[word])
                if match == number:
                    elements.append(word)
            if elements:
                final[current] = elements
                current += 1
                if current > 25:
                    break
            if current > 25:
                break

        results = final
        final = {}
        current = initial_curr
        for rank in results:
            if len(results[rank]) == 1:
                final[current] = results[rank][0]
                current += 1
            else:
                current, extend_by = self.final_sort(results[rank], current)
                final.update(extend_by)

        return current, final

    def final_sort(self, results, current):
        final = {}
        lengths = [len(result) for result in results]
        lengths = list(set(lengths))
        for length in lengths:
            for result in results:
                if len(result) == length:
                    final[current] = result
                    current += 1
                    if current > 25:
                        break
                if current > 25:
                    break
        return current, final


if __name__ == "__main__":
    d = DataSet()
    d.load()
    d.parse()
