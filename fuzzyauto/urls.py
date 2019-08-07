from django.conf.urls import url
from herokufuzzyauto import views
from django.views.generic import RedirectView

urlpatterns = [
     url(r'^search/{0,1}$', views.endpoint),
     url(r'^/{0,1}$', views.index),
     url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),

]
