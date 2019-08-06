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
    red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
    red = redis.Redis()
    pipe = red.pipeline()
    n = 1
    search = "*" + key + "*"
    values = red.keys(search)
    values = {key:values}
    """    values.append(str(type(key))
        n = n+ 1
        if (n % 64) == 0:
            pipe.execute()
            pipe = red.pipeline()
    """
    return str(values)
