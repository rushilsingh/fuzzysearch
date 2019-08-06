"""
WSGI config for fuzzyauto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from fuzzy_search import DataSet
from django.core.wsgi import get_wsgi_application
print("before")
d = DataSet()
d.load()
d.parse()
print("after")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fuzzyauto.settings")

application = get_wsgi_application()
