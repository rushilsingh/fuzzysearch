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
    current = 1
    for dic in mapping:
        for entry in dic:
            values.append(str(entry)[2:])
            current += 1
    
    if not values:
        return {}

    if len(values) == 1:
        return {1:values[0]}

    results = {}
    unsorted = []
    exact = None
    start = []
    for value in values:
        if value == key:
            exact = value
        elif value.startswith(key) and value != key:
            start.append(value)
        else:   
            unsorted.append(value)

    results["exact"] = exact
    restuls["start"] = start 
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
    return sorted_results
        

    
            

    
    
    return str(values)
