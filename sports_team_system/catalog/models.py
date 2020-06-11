from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta

# Create your models here.
class Player(AbstractUser):
	name = models.CharField(max_length = 20)
	SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))
	sex = models.CharField(max_length = 1, choices = SEX_CHOICES)
	grade = models.IntegerField(blank = True, null = True)
	telephone = models.CharField(max_length = 10, blank = True)
	personal_photo = models.ImageField(upload_to = 'images/personal_photo', default = 'images/personal_photo/unknown_user.jpg')
	student_card_front = models.ImageField(upload_to = 'images/student_card_front', blank = True)
	student_card_back = models.ImageField(upload_to = 'images/student_card_back', blank = True)
	ID_card = models.ImageField(upload_to = 'images/ID_card', blank = True)
	proof = models.ImageField(upload_to = 'images/proof', blank = True)
	is_active = models.BooleanField(default = False)

	def __str__(self):
		return self.name

class Team(models.Model):
	SPORT_TEAMS = (
		('女籃', 'girls_basketball'),
		('男籃', 'boys_basketball'),
		('女排', 'girls_volleyball'),
		('男排', 'boys_volleyball'),
		('羽球', 'badminton'),
		('游泳', 'swimming'),
		('棒壘', 'baseball')
		)
	sport_name = models.CharField(max_length = 10, choices = SPORT_TEAMS)
	captain = models.ForeignKey(Player, on_delete = models.SET_NULL, null = True)

	def __str__(self):
		return self.sport_name

class Availible_Day_Player(models.Model):
	player = models.ForeignKey(Player, on_delete = models.SET_NULL, null = True)
	sport_name = models.ForeignKey(Team, on_delete = models.SET_NULL, null = True)
	monday = models.BooleanField(default = False)
	tuesday = models.BooleanField(default = False)
	wednesday = models.BooleanField(default = False)
	thursday = models.BooleanField(default = False)
	friday = models.BooleanField(default = False)
	priority = models.IntegerField(blank = True)

	def __str__(self):
		return self.player.name + ' ' + self.sport_name.sport_name

class Availible_Day_Sport(models.Model):
	sport_name = models.ForeignKey(Team, on_delete = models.SET_NULL, null = True)
	monday = models.IntegerField(default = 0)
	tuesday = models.IntegerField(default = 0)
	wednesday = models.IntegerField(default = 0)
	thursday = models.IntegerField(default = 0)
	friday = models.IntegerField(default = 0)
	participant = models.ManyToManyField(Player, blank = True)
	def __str__(self):
		return self.sport_name.sport_name

class Playing_Sport(models.Model):
	player = models.ForeignKey(Player, on_delete = models.SET_NULL, null = True)
	sport_name = models.ForeignKey(Team, on_delete = models.SET_NULL, null = True)
	points_left = models.IntegerField()
	points_received = models.IntegerField(default = 0)

	def __str__(self):
		return self.player.name + ' ' + self.sport_name.sport_name

class Training(models.Model):
	poster = models.ForeignKey(Player, on_delete = models.SET_NULL, null = True)
	sport_name = models.ForeignKey(Team, on_delete = models.SET_NULL, null = True)
	end_time = models.DateTimeField(null = True)
	expire_time = models.DateTimeField(null = True)
	time = models.DateTimeField(null = True)
	create_time = models.DateTimeField(default = datetime.now())
	court = models.CharField(max_length = 20)
	participant = models.ManyToManyField(Playing_Sport, blank = True)

class Voting(models.Model):
	poster = models.ForeignKey(Player, on_delete = models.SET_NULL, null = True)
	sport_name = models.ForeignKey(Team, on_delete = models.SET_NULL, null = True)
	end_time = models.DateTimeField(null = True)
	create_time = models.DateTimeField(default = datetime.now())
	expire_time = models.DateTimeField(blank = True, null = True)
	participant = models.ManyToManyField(Playing_Sport, blank = True)
	question = models.TextField()
	option_one = models.TextField()
	option_two = models.TextField()
	option_three = models.TextField(null = True)
	option_one_cnt = models.IntegerField(default = 0)
	option_two_cnt = models.IntegerField(default = 0)
	option_three_cnt = models.IntegerField(default = 0)

class Noticing(models.Model):
	poster = models.ForeignKey(Player, on_delete = models.SET_NULL, null = True)
	sport_name = models.ForeignKey(Team, on_delete = models.SET_NULL, null = True)
	expire_time = models.DateTimeField(null = True)
	create_time = models.DateTimeField(default = datetime.now())
	paragraph = models.TextField()

