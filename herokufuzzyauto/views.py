# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fuzzy_search import DataSet
import redis
import os

def index(request):
   
    red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
    for key in redis.hscan_iter(name, match="the", count=None):
        value = key

    return render(request, 'base.html', {'data': value})
