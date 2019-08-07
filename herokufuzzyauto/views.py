# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fuzzy_search import DataSet
import redis
import os
d = DataSet()

def index(request):
    return "build here"

def endpoint(request, word=''):
    word = request.GET.get('word', word)
    values = d.find(word)
    return render(request, 'base.html', {'data': values})
