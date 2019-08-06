# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fuzzy_search import DataSet
import redis
import os

def index(request):
   
    red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
    #keys = red.keys("23135851162")
    #keys.sort().reverse()

    for key in red.scan_iter("the"):
        value = key
        break

    return render(request, 'base.html', {'data': value})



