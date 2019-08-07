# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fuzzy_search import DataSet
import redis
import os
d = DataSet()

def index(request):
     
    output = """
   	 <form type="get" action="search" style="margin: 0">
  	 <input  id="search_box" type="text" name="search_box"  placeholder="Search..." >
    	 <button id="search_submit" type="submit" >Submit</button>
	 </form>
    """
    return render(request, 'base.html', {'data': output}   

def search(self, word):
    values = d.find(word)
    return render(request, 'results.html', {'data': values})

def endpoint(request, word=''):
    word = request.GET.get('word', word)
    values = d.find(word)
    return render(request, 'results.html', {'data': values})
