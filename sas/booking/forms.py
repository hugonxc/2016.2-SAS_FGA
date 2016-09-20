from django.utils.translation import ugettext as _
from django.forms import ModelForm
from .models import UserProfile,Booking,BookTime,Place
from .models import CATEGORY
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from datetime import date, time
from django.utils import timezone
from datetime import date, datetime, time

class LoginForm(ModelForm):
	email = forms.CharField(
					label=_('Email:'),
					widget=forms.TextInput(attrs={'placeholder': 'example@email.com'}))
	password = forms.CharField(
					label=_('Password:'),
					widget=forms.PasswordInput(attrs={'placeholder': ''}))

	def save(self, force_insert=False, force_update=False, commit=True):
		username = self.cleaned_data.get("email")
		password = self.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		if user is None:
			self.add_error('password', _('Email or Password does not match'))
		return user

	class Meta:
		model = User
		fields = ['email', 'password']

class UserForm(ModelForm):
	name = forms.CharField(
					label=_('Name:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	email = forms.CharField(
					label=_('Email:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	password = forms.CharField(
					label=_('Password:'),
					required=False,
					widget=forms.PasswordInput(attrs={'placeholder': ''}))
	repeat_password = forms.CharField(
					label=_('Repeat Password:'),
					required=False,
					widget=forms.PasswordInput(attrs={'placeholder': ''}))
	repeat_password = forms.CharField(
					label=_('Repeat Password:'),
					widget=forms.PasswordInput(attrs={'placeholder': ''}))
	registration_number = forms.CharField(
					label=_('Registration number:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	category = forms.ChoiceField(choices=CATEGORY, label=_('Category:'))

	def save(self, force_insert=False, force_update=False, commit=True):
		userprofile = super(UserForm, self).save(commit=False)
		userprofile.user = User()
		userprofile.name(self.cleaned_data.get('name'))
		userprofile.user.email = self.cleaned_data.get('email')
		userprofile.user.username=userprofile.user.email
		userprofile.user.set_password(self.cleaned_data.get('password'))
		print(commit)
		# do custom stuff
		if commit:
			userprofile.save()
		return userprofile

	class Meta:
		model = UserProfile
		fields = ['name', 'registration_number',
				  'category', 'email', 'password', 'repeat_password']

class EditUserForm(UserForm):

	class Meta:
		model = UserProfile
		fields = ['name', 'registration_number',
				  'category', 'email']

class NewUserForm(UserForm):

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password1 = cleaned_data.get('password')
		password2 = cleaned_data.get('repeat_password')
		if password1 and password2 and password1 != password2:
			self.add_error('password', _('Passwords do not match'))


class BookingForm(ModelForm):
	name = forms.CharField(
					label=_('Nome:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	start_hour = forms.TimeField(
					label=_('Hora inicial:'),
					widget=forms.widgets.TimeInput)
	end_hour = forms.TimeField(
					label=_('Hora final:'),
					widget=forms.widgets.TimeInput)
	start_date = forms.DateField(
					label=_('Data inicial:'),
					widget=forms.widgets.DateInput)
	end_date = forms.DateField(
					label=_('Data final:'),
					widget=forms.widgets.DateInput)
	place_name = forms.CharField(
					label=_('Sala:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))
	localization = forms.CharField(
					label=_('Predio:'),
					widget=forms.TextInput(attrs={'placeholder': ''}))

	def save(self, force_insert=False, force_update=False, commit=True):
		booking = super(BookingForm, self).save(commit=False)
		booking_time = BookTime()
		booking_time.start_hour = self.cleaned_data.get('start_hour')
		booking_time.end_hour = self.cleaned_data.get('end_hour')
		booking_time.start_date = self.cleaned_data.get('start_date')
		booking_time.end_date = self.cleaned_data.get('end_date')
		booking_time.save()
		booking.name = self.cleaned_data.get('name')
		booking_place = Place()
		booking_place.name = self.cleaned_data.get('place_name')
		booking_place.localization = self.cleaned_data.get('localization')
		booking_place.save()
		booking.place = booking_place

		# do custom stuff
		if commit:
			booking.save()
			booking.time.add(booking_time)
			booking.save()
		return booking

	def clean(self):
		cleaned_data = super(BookingForm, self).clean()
		today = date.today()
		now = datetime.now().time()
		start_date = cleaned_data.get('start_date')
		end_date = cleaned_data.get('end_date')
		start_hour = cleaned_data.get('start_hour')
		end_hour = cleaned_data.get('end_hour')
		try:
			if today > start_date:
				msg = 'A data de inicio deve ser posterior a data atual.'
				self.add_error('start_date', msg)
		except TypeError as TypeErrorException:
			self.add_error('start_date', '')
		else:
			try:
				if today == start_date and today == end_date and now > start_hour:
					msg = 'A hora de inicio deve ser posterior a hora atual para uma reserva hoje.'
					self.add_error('start_hour', msg)
			except TypeError as TypeErrorException3:
				self.add_error('start_hour', '')
			else:
				try:
					if today == start_date and today == end_date and now > end_hour:
						msg = 'A hora final deve ser posterior a hora atual para uma reserva hoje.'
						self.add_error('end_hour', msg)
					elif end_date < start_date:
						msg = 'A data final deve ser posterior a data de inicio.'
						self.add_error('end_date', msg)
				except TypeError as TypeErrorException:
					self.add_error('end_hour', '')
				else:
					if end_hour <= start_hour:
						msg = 'A hora final deve ser posterior a hora inicial.'
						self.add_error('end_hour', msg)
		finally:
			try:
				if today > end_date:
					msg = 'A data final deve ser posterior a data atual.'
					self.add_error('end_date', msg)
			except TypeError as TypeErrorException2:
				self.add_error('end_date', '')


	class Meta:
		model = Booking
		fields = ['name', 'place_name',
				  'start_hour', 'end_hour', 'start_date', 'end_date']
