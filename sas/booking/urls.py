from django.conf.urls import url
from django.contrib import admin
from .views import new_user, login_user, logout_user, delete_user, list_user

urlpatterns = [
    url(r'newuser/', new_user, name = 'newuser'),
    url (r'login/' ,login_user ,name = 'login'),
    url(r'logout/', logout_user, name = 'logout'),
    url(r'delete/(?P<id>\d+/$)', delete_user, name = 'deleteuser'),
  	url(r'^edituser/(?P<id>\d+)/$', edit_user, name = 'edituser'), 
]
