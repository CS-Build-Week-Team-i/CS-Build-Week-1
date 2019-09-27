from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('rooms', api.room),
    url('move', api.move),
    url('say', api.say),
]