# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fuzzy_search import DataSet
import redis

def index(request):
   
    red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
    keys = red.keys("*")
    keys.sort().reverse()
    value = red.get(keys[0])
    import pickle
    value = pickle.loads(value)


    return render(request, 'base.html', {'data': value})



