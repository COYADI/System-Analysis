from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	list_display = ('username', 'name', 'password', 'sex', 'grade')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	list_display = ('sport_name', 'captain')

@admin.register(Playing_Sport)
class Playing_SportAdmin(admin.ModelAdmin):
	list_display = ('player', 'sport_name')

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
	list_display = ('poster', 'sport_name', 'end_time', 'expire_time', 'time', 'court')

@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
	list_display = ('poster', 'sport_name', 'end_time', 'expire_time')

@admin.register(Noticing)
class NoticingAdmin(admin.ModelAdmin):
	list_display = ('poster', 'sport_name', 'expire_time', 'paragraph')