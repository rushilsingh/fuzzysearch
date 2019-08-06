import os
import requests
import io
import zipfile
import datetime
import textfsm
import redis
import pytz


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
        print(parsed)



if __name__ == "__main__":
    d = DataSet()
    d.load()
    d.parse()
