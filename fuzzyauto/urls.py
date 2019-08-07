from django.conf.urls import url
from herokufuzzyauto import views

urlpatterns = [
     url(r'^search/{0,1}$', views.endpoint),
     url('', views.index)

]
