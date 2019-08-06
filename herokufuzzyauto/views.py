# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fuzzy_search import DataSet
import redis
import os

def index(request, word):
   
    values = find(word)
    return render(request, 'base.html', {'data': values})

def find(key):

    values = []
    #red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
    red = redis.Redis()
    pipe = red.pipeline()
    n = 1
    search = "*" + key + "*"
    for value in red.hscan(search):
        values.append(value)

    values = {key:values}
    
    return str(values)
