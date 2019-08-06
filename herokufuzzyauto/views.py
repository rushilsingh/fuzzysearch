# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fuzzy_search import DataSet
import redis
import os
from itertools import izip_longest

def index(request):
   
    red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
    for keybatch in batcher(red.scan_iter("*the*"), 500):
        value = key
        break
    return render(request, 'base.html', {'data': value})


def batcher(iterable, n):
    args = [iter(iterable)] * n
    return izip_longest(*args)

