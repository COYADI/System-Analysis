from django.shortcuts import render
from catalog.models import *
import random
import time
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone

# Create your views here.
def hello_view(request):
    return render(request, 'system.html', {
        'data': "You've got a star!",
    })

def index(request):
	return render(request, 'index.html')

def register(request):
	if request.method == 'GET':
		return render(request, 'register.html')
	if request.method == 'POST':
		student_id = request.POST.get('student_id')
		password = request.POST.get('password')
		name = request.POST.get('name')
		sex = request.POST.get('sex')
		grade = request.POST.get('grade')
		if Player.objects.filter(username = student_id).exists():
			return render(request, 'register.html', {'error_message': 'Already registered student ID'})
		email = student_id + '@ntu.edu.tw'
		player = Player.objects.create_user(student_id, email, password)
		player.name = name
		player.sex = sex
		player.grade = grade
		player.save()

		#auth.login(request, player)
		return HttpResponseRedirect('/index/')


def login(request):
	if request.method == 'GET':
		return render(request, 'login.html')
	if request.method == 'POST':
		if request.user.is_authenticated:
			return HttpResponseRedirect('/mainpage/')
		student_id = request.POST.get('student_id')
		password = request.POST.get('password')
		user = auth.authenticate(username=student_id, password=password)
		if user is not None and user.is_active == True:
			auth.login(request, user)
			return HttpResponseRedirect('/mainpage/')
		else:
			return render(request, 'login.html', {'alert_flag': True})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/index/')

def mainpage(request):
	if request.user.is_authenticated:
		current_user = request.user
		current_playing_sport = Playing_Sport.objects.filter(player = current_user)
		current_team = []
		training_to_see = []
		voting_to_see = []
		noticing_to_see = []
		for i in current_playing_sport:
			current_team.append(i.sport_name)
		for i in current_team:
			training_to_see += Training.objects.filter(sport_name = i, expire_time__gte = timezone.now())
			voting_to_see += Voting.objects.filter(sport_name = i, expire_time__gte = timezone.now())
			noticing_to_see += Noticing.objects.filter(sport_name = i, expire_time__gte = timezone.now())


		return render(request, 'mainpage.html', locals())
	else:
		return HttpResponseRedirect('/login/')