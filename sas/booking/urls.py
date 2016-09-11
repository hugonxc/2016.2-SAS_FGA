from django.conf.urls import url
from django.contrib import admin
from .views import new_user, delete_user

urlpatterns = [
    url(r'newuser/', new_user, name = 'newuser'),
    url(r'delete/(?P<id>\d+/$)', delete_user, name = 'deleteuser')

]
