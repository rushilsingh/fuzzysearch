# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fuzzy_search import DataSet
import redis
import os

def index(request):
   
    red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
    values = []
    for key in red.hscan_iter("h", match=".*procra.*", count=None):
        value = key
        values.append
    values = str(values)

    return render(request, 'base.html', {'data': values})
