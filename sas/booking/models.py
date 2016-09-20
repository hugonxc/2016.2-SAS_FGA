from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

CATEGORY = (('1', _('Student')),('2', _('Teaching Staff')), ('3', _('Employees')))

BUILDINGS = (('1', _('')), ('2', _('UAC')), ('3', _('UED')))

# TODO: Select spaces according to building selected
SPACES = (('1', _('')), ('2', _('I1')), ('3', _('I2')), ('4', _('I3')), ('5', _('I4')), ('6', _('I5')),
	('7', _('I6')), ('8', _('I7')), ('9', _('I8')), ('10', _('I9')), ('11', _('I10')), ('12', _('S1')), ('13', _('S2')),
	('14', _('S3')), ('15', _('S4')), ('16', _('S5')), ('17', _('S6')), ('18', _('S7')), ('19', _('S8')),
	('20', _('S9')), ('21', _('S10')))

class UserProfile(models.Model):
	registration_number = models.CharField(max_length=20)
	user = models.OneToOneField(User, on_delete=models.CASCADE,
								related_name="profile_user")
	category = models.CharField(choices=CATEGORY, max_length=20)

	def name(self, name):
		if self.user is None:
			self.user = User()
		names = name.split()
		self.user.first_name = names.pop(0)
		self.user.last_name = str.join(" ", names)

	def full_name(self):
		name = str.join(" ", [self.user.first_name, self.user.last_name])
		return name

	def save(self, *args, **kwargs):
		self.user.save()
		self.user_id = self.user.pk
		super(UserProfile, self).save(*args, **kwargs)

class Place(models.Model):
	name = models.CharField(max_length=50)
	capacity = models.CharField(max_length=250)
	is_laboratory = models.BooleanField()
	localization = models.CharField(max_length=50)
	
	

class BookTime(models.Model):
	start_hour = models.TimeField(null=False, blank=False)
	end_hour = models.TimeField(null=False, blank=False)
	date_booking = models.DateField(null=False, blank=False)

	def add_days(self,nr_days):
		delta = timedelta(days=nr_days)
		self.date_booking = self.date_booking + delta

	def next_week_day(self,nr_weekday):
		diff_of_weekdays = self.date_booking.weekday() - nr_weekday
		if diff_of_weekdays > 0:
			self.add_days(7 - diff_of_weekdays)
		elif diff_of_weekdays < 0:
			self.add_days(diff_of_weekdays * (-1))

	def save(self, *args, **kwargs):
		super(BookTime, self).save(*args, **kwargs)

class Booking(models.Model):
	user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)
	time = models.ManyToManyField(BookTime, related_name="booking_time")
	place = models.ForeignKey(Place, related_name="booking_place") 
	name = models.CharField(max_length=50)
	start_date = models.DateField(null=False, blank=False)
	end_date = models.DateField(null=False, blank=False)

	def save(self, *args, **kwargs):
		super(Booking, self).save(*args, **kwargs)

