from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PasswordForm
from .forms import UserForm, NewUserForm, LoginForm, EditUserForm, BookingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, Booking
from django.contrib import messages


def index(request):
    form = LoginForm()
    return render(request, 'booking/index.html', {'form': form})


def new_user(request):
	if request.method == "POST":
		form = NewUserForm(request.POST, UserProfile)
		if not(form.is_valid()):
			return render(request, 'booking/newUser.html', {'form_user': form})
		else:
			user_profile = form.save()
			messages.success(request,_('You have been registered'))
			return index(request) 
	else:
		form = NewUserForm()
		return render(request, 'booking/newUser.html', {'form_user': form})


def list_user(request):
    users = UserProfile.objects.all()
    return render(request, 'booking/listUser.html', {'users': users})


def edit_user(request):
	if request.user.is_authenticated() and request.method == "POST":
		form = EditUserForm(request.POST, instance=request.user.profile_user)
		if form.is_valid():
			user = form.save()
			messages.success(request, _('Your data has been updated'))
		return render_edit_user(request, user_form=form)
	elif not request.user.is_authenticated():
		return index(request)
	else:
		return render_edit_user(request)


def render_edit_user(request, user_form=None, change_form=PasswordForm()):
	user = request.user
	initial = {}
	initial['name'] = user.profile_user.full_name()
	initial['email'] = user.email
	if user_form is None:
		user_form = EditUserForm(initial=initial,
								 instance=request.user.profile_user)
	return render(request,
				  'booking/editUser.html',
				  {'form_user': user_form, 'change_form': change_form})


def login_user(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.save()
			if user is not None:
				login(request, user);
				return render(request, 'booking/home.html', {})
			else:
				return render(request, 'booking/index.html', {'form': form})
		else:
			return render(request, 'booking/index.html', {'form': form})
	else:
		return index(request)


def logout_user(request):
    logout(request)
    form = LoginForm()
    return render(request, 'booking/index.html', {'form': form})


def delete_user(request):
	if request.user.is_authenticated():
		request.user.delete()
		logout(request)
		return index(request)
	else:
		return index(request)


def change_password(request):
	if request.user.is_authenticated() and request.POST:
		form = PasswordForm(request.POST)
		if form.is_valid() and form.is_password_valid(request.user.username):
			form.save(request.user)
			login(request, request.user)
			messages.success(request, _('Your password has been changed'))
			return render_edit_user(request)
		else:
			return render_edit_user(request, change_form=form)
	if not request.user.is_authenticated():
		return index(request)
	else:
		return render_edit_user(request)


def new_booking(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			form_booking = BookingForm(request.POST)
			if not(form_booking.is_valid()):
				return render(request, 'booking/newBooking.html', {'form_booking': form_booking})
			else:
				booking = form_booking.save(request.user)
				if not booking:
					messages.error(request, _("Booking alread exists"))
					return render(request, 'booking/newBooking.html', {'form_booking': form_booking})
				request.session['booking'] = booking.pk
				return render(request, 'booking/showDates.html', {'booking': booking})
		else:
			form_booking = BookingForm()
			return render(request, 'booking/newBooking.html', {'form_booking': form_booking})

	else:
		return index(request)


def search_booking(request):
    if request.user.is_authenticated():
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'booking/searchBooking.html', {'bookings': bookings})
    else:
        form = LoginForm()
        return render(request, 'booking/index.html', {'form': form})


def cancel_booking(request, id):
	if request.user.is_authenticated() and request.session['booking']:
		id = int(id)
		if(id == request.session.get('booking')):
			request.session.pop('booking')
			Booking.objects.get(pk=id).delete()
			messages.success(request, _("Booking has been canceled"))
			return index(request)
		else:
			messages.error(request, _("You cannot cancel this booking"))
			return index(request)
	else:
		return index(request)


def confirm_booking(request, id):
	if request.user.is_authenticated() and request.session['booking']:
		id = int(id)
		if id == request.session.get('booking'):
			request.session.pop('booking')
			messages.success(request, _("Booking has been saved."))
			return index(request)
		else:
			messages.error(request, _("You cannot confirm this booking"))
			return index(request)
	else:
		return index(request)
