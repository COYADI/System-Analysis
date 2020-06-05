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
from operator import itemgetter, attrgetter
from datetime import datetime, timedelta

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
		if request.method == 'GET':
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
			training_to_see.sort(key = attrgetter('create_time'))
			voting_to_see.sort(key = attrgetter('create_time'))
			noticing_to_see.sort(key = attrgetter('create_time'))
			training_to_see.reverse()
			voting_to_see.reverse()
			noticing_to_see.reverse()
			return render(request, 'mainpage.html', locals())
		if request.method == 'POST':
			if request.POST.get('submit'):
				submit_type = request.POST.get('submit')
				if submit_type == 'noticing':
					current_user = request.user
					poster = current_user
					sport_name = request.POST.get('sport_name')
					sport_input = Team.objects.filter(sport_name = sport_name)
					expire_time = request.POST.get('expire_time')
					paragraph = request.POST.get('paragraph')
					Noticing.objects.create(poster = poster, sport_name = sport_input[0], expire_time = expire_time, paragraph = paragraph)
				elif submit_type == 'training':
					current_user = request.user
					poster = current_user
					sport_name = request.POST.get('sport_name')
					sport_input = Team.objects.filter(sport_name = sport_name)
					time = request.POST.get('time')
					end_time = request.POST.get('end_time')
					court = request.POST.get('court')
					Training.objects.create(poster = poster, sport_name = sport_input[0], time = time, end_time = end_time, expire_time = time, court = court)
				elif submit_type == 'participate_train':
					current_user = request.user
					num = request.POST.get('number')
					current_training = Training.objects.filter(id = num)
					current_playing_sport = Playing_Sport.objects.filter(player = current_user, sport_name = current_training[0].sport_name)
					current_training[0].participant.add(current_playing_sport[0])
					current_training[0].save()
				return HttpResponseRedirect('/mainpage/')
	else:
		return HttpResponseRedirect('/login/')

def settings(request):
	if request.user.is_authenticated:
		if request.method == 'GET':
			return render(request, 'settings.html', locals())
		if request.method == 'POST':
			current_user = request.user
			if request.POST.get('password'):
				password = request.POST.get('password')
				user = auth.authenticate(username=current_user.username, password=password)
				if user is not None and user.is_active == True:
					if request.POST.get('name'):
						new_name = request.POST.get('name')
						current_user.name = new_name
						current_user.save()
					if request.POST.get('telephone'):
						new_telephone = request.POST.get('telephone')
						current_user.telephone = new_telephone
						current_user.save()
					if request.FILES.get('personal_photo'):
						new_personal_photo = request.FILES.get('personal_photo')
						current_user.personal_photo = new_personal_photo
						current_user.save()
					if request.FILES.get('student_card_front'):
						new_student_card_front = request.FILES.get('student_card_front')
						current_user.student_card_front = new_student_card_front
						current_user.save()
					if request.FILES.get('student_card_back'):
						new_student_card_back = request.FILES.get('student_card_back')
						current_user.student_card_back = new_student_card_back
						current_user.save()
					if request.FILES.get('ID_card'):
						new_ID_card = request.FILES.get('ID_card')
						current_user.ID_card = new_ID_card
						current_user.save()
					if request.FILES.get('proof'):
						new_proof = request.FILES.get('proof')
						current_user.proof = new_proof
						current_user.save()
				else:
					alert_flag = True
					return render(request, 'settings.html', locals())

		return HttpResponseRedirect('/mainpage/')
	else:
		return HttpResponseRedirect('/login/')