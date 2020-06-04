from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Player(AbstractUser):
	name = models.CharField(max_length = 20)
	SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))
	sex = models.CharField(max_length = 1, choices = SEX_CHOICES)
	grade = models.IntegerField(blank = True, null = True)
	telephone = models.CharField(max_length = 10, blank = True)
	personal_photo = models.ImageField(upload_to = 'personal_photo', blank = True)
	student_card_front = models.ImageField(upload_to = 'student_card_front', blank = True)
	student_card_back = models.ImageField(upload_to = 'student_card_back', blank = True)
	ID_card = models.ImageField(upload_to = 'ID_card', blank = True)
	proof = models.ImageField(upload_to = 'proof', blank = True)
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
	court = models.CharField(max_length = 20)
	participant = models.ManyToManyField(Playing_Sport)

class Voting(models.Model):
	poster = models.ForeignKey(Player, on_delete = models.SET_NULL, null = True)
	sport_name = models.ForeignKey(Team, on_delete = models.SET_NULL, null = True)
	end_time = models.DateTimeField(null = True)
	expire_time = models.DateTimeField(null = True)
	participant = models.ManyToManyField(Playing_Sport)

class Noticing(models.Model):
	poster = models.ForeignKey(Player, on_delete = models.SET_NULL, null = True)
	sport_name = models.ForeignKey(Team, on_delete = models.SET_NULL, null = True)
	expire_time = models.DateTimeField(null = True)
	paragraph = models.TextField()

