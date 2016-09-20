from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, NewUserForm, LoginForm, EditUserForm, BookingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, Booking
from django.http import HttpResponse
import json



def index(request):
    form = LoginForm()
    return render(request, 'booking/index.html', {'form':form})

def new_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST, UserProfile)
        if not(form.is_valid()):
            return render(request, 'booking/newUser.html', {'form_user': form})
        else:
            user_profile = form.save()
            form = LoginForm()
            return render(request, 'booking/index.html', {'form':form})
    else:
        form = NewUserForm()
        return render(request, 'booking/newUser.html', {'form_user': form})


def list_user(request):
    users = UserProfile.objects.all()
    return render(request, 'booking/listUser.html', {'users': users})


def edit_user(request):
    if request.user.is_authenticated() and request.method == "POST":
        print(request.user.pk)
        print(request.user.profile_user.pk)
        form = EditUserForm(request.POST, instance=request.user.profile_user)
        if form.is_valid():
            user = form.save()
            print(user.user.pk)
            return render(request, 'booking/editUser.html', {'form_user': form})
        else:
            print(form.errors)
            return render(request, 'booking/editUser.html', {'form_user': form})
    elif not request.user.is_authenticated():
        return render(request, 'booking/index.html', {})
    else:
        print(request.user.pk)
        user = request.user
        initial = {}
        initial['name'] = user.profile_user.full_name()
        initial['email'] = user.email
        form = EditUserForm(initial=initial, instance=request.user.profile_user)
        return render(request, 'booking/editUser.html', {'form_user': form})

def login_user(request) :
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.save()
			if user is not None:
				login ( request , user) ;
				return render (request ,'booking/home.html',{})
			else:
				return render (request,'booking/index.html',{'form':form})
	else:
		form = LoginForm()
		return render (request ,'booking/index.html',{'form':form})

def logout_user(request):
    logout(request)
    form = LoginForm()
    return render(request, 'booking/index.html', {'form': form})


def delete_user(request):
    if request.user.is_authenticated():
        User.objects.get(pk=request.user.pk).delete()
        form = LoginForm()
        return render(request, 'booking/index.html', {'form': form})
    else:
        return render(request, 'booking/editUser.html', {})


def new_booking(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form_booking = BookingForm(request.POST, Booking)
            if form_booking.is_valid():
                booking = form_booking.save(commit=False)
                booking.user = request.user
                form_booking.save()
                form = LoginForm()
                return render(request, 'booking/index.html', {'form':form})
            else:
                return render(request, 'booking/newBooking.html', {'form_booking':form_booking})
        else:
            form_booking = BookingForm()
            return render(request, 'booking/newBooking.html', {'form_booking':form_booking})

    else:
        form = LoginForm()
        return render(request, 'booking/index.html', {'form':form})

def check_new_booking(request):
    form_booking=BookingForm(request.POST,Booking)
    if form_booking.is_valid():
        return HttpResponse(json.dumps({'ok':1,'errors':''}))
    else:
        return HttpResponse(json.dumps({'ok':0,'errors':form_booking.errors}    ))

def search_booking(request):
    if request.user.is_authenticated():
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'booking/searchBooking.html', {'bookings':bookings})
    else:
        form = LoginForm()
        return render(request, 'booking/index.html', {'form':form})
