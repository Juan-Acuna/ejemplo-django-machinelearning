from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Inicio),
    url(r'^predict/$', views.Predict),
    url(r'^insert/$', views.Insert),
    url(r'^postinsert/$', views.postinsert),
]
