# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fuzzy_search import DataSet
import redis
import os
d = DataSet()

def index(request):
    endpoint = "search"
    return render(request, 'base.html', {'data': endpoint} )

def endpoint(request, word=''):
    word = request.GET.get('word', word)
    values = d.find(word)
    return render(request, 'results.html', {'data': values})
