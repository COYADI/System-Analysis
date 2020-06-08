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
import pandas as pd
import re
from django.core.mail import send_mail
import base64
from itsdangerous import URLSafeTimedSerializer as utsr
import openpyxl
from openpyxl import Workbook
import requests
import urllib
from urllib.request import urlretrieve

SECRET_KEY = '))wug4^rwwoiup4#9an29f5pk=uw#d()fkv@_*(a0sf9%rd9tc'
SECRET_KEY = bytes(SECRET_KEY,encoding = 'utf-8')

#token_confirm = Token(SECRET_KEY)


class Token():
	def __init__(self,security_key):
		self.security_key = security_key
		self.salt = base64.encodestring(security_key)
	def generate_validate_token(self,username):
		serializer = utsr(self.security_key)
		return serializer.dumps(username,self.salt)
	def confirm_validate_token(self,token,expiration=3600):
		serializer = utsr(self.security_key)
		return serializer.loads(token,
		salt=self.salt,
		max_age=expiration) 



# Create your views here.
def active(request,token):
	token_confirm = Token(SECRET_KEY)
	username = token_confirm.confirm_validate_token(token)
	player = Player.objects.get(username=username)
	player.is_active = True
	player.save()
	return HttpResponseRedirect('/index/')

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
		#generate varify token
		token_confirm = Token(SECRET_KEY)
		student_id = request.POST.get('student_id')
		password = request.POST.get('password')
		name = request.POST.get('name')
		sex = request.POST.get('sex')
		grade = request.POST.get('grade')
		if Player.objects.filter(username = student_id).exists():
			return render(request, 'register.html', {'error_message': 'Already registered student ID'})
		email = student_id + '@ntu.edu.tw'

		if re.match('(^b|^t|^r|^d)\d{8}',student_id) == None:
			return render(request, 'register.html', {'error_message': 'Invalid student_id'})
		player = Player.objects.create_user(student_id, email, password)
		player.name = name
		player.sex = sex
		player.grade = grade
		player.save()

		token = token_confirm.generate_validate_token(student_id)
		#active_key = base64.encodestring(username)
		#send email to the register email
		#http://0e2983ec5d6e.ngrok.io 
		#http://localhost:8000
		message = "\n".join([
		u'{0},歡迎加入資管系隊系統~~'.format(student_id),
		u'請訪問下方連結，完成使用者驗證:',
		'/'.join(['http://localhost:8000/active',token])
		])
		send_mail(u'註冊使用者驗證資訊',message,'leo19990709@gmail.com',[email,]) 

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
			personal_photo = current_user.personal_photo
			current_team = []
			training_to_see = []
			voting_to_see = []
			noticing_to_see = []
			is_captain = False
			for i in current_playing_sport:
				current_team.append(i.sport_name)
			for i in current_team:
				training_to_see += Training.objects.filter(sport_name = i, expire_time__gte = timezone.now())
				voting_to_see += Voting.objects.filter(sport_name = i, expire_time__gte = timezone.now())
				noticing_to_see += Noticing.objects.filter(sport_name = i, expire_time__gte = timezone.now())
				team = Team.objects.get(sport_name = i)
				if team.captain == current_user:
					is_captain = True
					is_captain_team = team.sport_name
			training_to_see.sort(key = attrgetter('create_time'))
			voting_to_see.sort(key = attrgetter('create_time'))
			noticing_to_see.sort(key = attrgetter('create_time'))
			training_to_see.reverse()
			voting_to_see.reverse()
			noticing_to_see.reverse()
			if training_to_see:
				next_training = training_to_see[0]
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
					current_training = Training.objects.get(id = num)
					current_playing_sport = Playing_Sport.objects.get(player = current_user, sport_name = current_training.sport_name)
					
					if current_playing_sport in current_training.participant.all():
						pass
					else:
						if current_playing_sport.sport_name.sport_name == '羽球':
							current_playing_sport.points_left -= 1
						#print(current_playing_sport.points_received + 1)
						current_playing_sport.points_received += 1
						#print(current_playing_sport.points_received)
						current_playing_sport.save()
						current_training.participant.add(current_playing_sport)
						current_training.save()									
				elif submit_type == 'cancel_train':
					current_user = request.user
					num = request.POST.get('number')
					current_training = Training.objects.get(id = num)
					current_playing_sport = Playing_Sport.objects.get(player = current_user, sport_name = current_training.sport_name)
					if current_playing_sport not in current_training.participant.all():
						pass
					else:
						if current_playing_sport.sport_name.sport_name == '羽球':
							current_playing_sport.points_left += 1
						current_playing_sport.points_received -= 1
						current_playing_sport.save()
						current_training.participant.remove(current_playing_sport)
						current_training.save()	
				elif submit_type == 'voting':
					current_user = request.user
					poster = current_user
					sport_name = request.POST.get('sport_name')
					sport_input = Team.objects.get(sport_name = sport_name)
					end_time = request.POST.get('end_time')
					expire_time = request.POST.get('expire_time')
					question = request.POST.get('question')
					option_one = request.POST.get('option_one')
					option_two = request.POST.get('option_two')
					if request.POST.get('option_three'):
						option_three = request.POST.get('option_three')
						Voting.objects.create(poster = poster, sport_name = sport_input, end_time = end_time, expire_time = expire_time, question = question, option_one = option_one, option_two = option_two, option_three = option_three)
					else:
						Voting.objects.create(poster = poster, sport_name = sport_input, end_time = end_time, expire_time = expire_time, question = question, option_one = option_one, option_two = option_two)
				elif submit_type == 'govote':
					current_user = request.user
					num = request.POST.get('number')
					current_voting = Voting.objects.get(id = num)
					current_playing_sport = Playing_Sport.objects.get(player = current_user, sport_name = current_voting.sport_name)
					if current_playing_sport in current_voting.participant.all():
						pass
					else:
						current_user_weighted = current_playing_sport.points_received // 5 + 1
						if request.POST.get('answer'):
							current_voting.participant.add(current_playing_sport)
							answer = request.POST.get('answer')
							if answer == 'one':
								current_voting.option_one_cnt += current_user_weighted
							elif answer == 'two':
								current_voting.option_two_cnt += current_user_weighted
							elif answer =='three':
								current_voting.option_three_cnt += current_user_weighted
							current_voting.save()						
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

def applyteam(request):
	if request.user.is_authenticated:
		if request.method == 'GET':
			team = Team.objects.all()
			return render(request, 'apply_team.html', locals())
		if request.method == 'POST':
			current_user = request.user
			if request.POST.get('password'):
				password = request.POST.get('password')
				user = auth.authenticate(username=current_user.username, password=password)
				if user is not None and user.is_active == True:
					applying_team = request.POST.get('team')
					target_team = Team.objects.get(sport_name = applying_team)
					if target_team.sport_name == '羽球':
						Playing_Sport.objects.create(player = current_user, sport_name = target_team, points_left = 10)
					else:
						Playing_Sport.objects.create(player = current_user, sport_name = target_team)
				else:
					alert_flag = True
					team = Team.objects.all()
					return render(request, 'apply_team.html', locals())

		return HttpResponseRedirect('/mainpage/')
	else:
		return HttpResponseRedirect('/login/')

def manageteam(request):
	if request.user.is_authenticated:
		if request.method == 'GET':
			current_user = request.user
			current_playing_sport = Playing_Sport.objects.filter(player = current_user)
			current_team = []
			is_captain = False
			for i in current_playing_sport:
				current_team.append(i.sport_name)
			for i in current_team:
				team = Team.objects.get(sport_name = i)
				if team.captain == current_user:
					is_captain = True
					break
			if is_captain == False:
				return HttpResponseRedirect('/mainpage/')
			team_member = Playing_Sport.objects.filter(sport_name = team)
			return render(request, 'manageteam.html', locals())
		if request.method == 'POST':
			current_user = request.user
			current_playing_sport = Playing_Sport.objects.filter(player = current_user)
			current_team = []
			is_captain = False
			for i in current_playing_sport:
				current_team.append(i.sport_name)
			for i in current_team:
				team = Team.objects.get(sport_name = i)
				if team.captain == current_user:
					is_captain = True
					break
			if request.POST.get('submit'):
				submit_type = request.POST.get('submit')
				if request.POST.get('password'):
					password = request.POST.get('password')
					user = auth.authenticate(username=current_user.username, password=password)
					if user is not None and user.is_active == True:
						if submit_type == 'get_team':
							member = request.POST.getlist('members')
							output_list = []
							for i in member:
								target = Player.objects.filter(name = i)
								output_list += target.values('name', 'username', 'sex', 'grade', 'telephone', 'personal_photo', 'student_card_front', 'student_card_back', 'ID_card', 'proof')
							output = pd.DataFrame.from_records(output_list)
							Result_PATH = 'team_member.xlsx'
							writer = pd.ExcelWriter(Result_PATH, engine='xlsxwriter')
							output.to_excel(writer, sheet_name = 'mem_list')
							writer.save()
							#def down_file(request):
							with open('team_member.xlsx', 'rb') as model_excel:
								result = model_excel.read()
							response = HttpResponse(result)
							response['Content-Disposition'] = 'attachment; filename=team_member_list.xlsx'
							return response
							#xlsx_url = 'http://localhost:8000/media/team_member.xlsx'
							#urlretrieve(xlsx_url, "test.xlsx")
							print(output.head())
							#output.to_excel('member_list.xlsx')
						elif submit_type == 'change_captain':
							next_captain_name = request.POST.get('captain')
							next_captain = Player.objects.get(name = next_captain_name)
							team.captain = next_captain
							team.save()
					else:
						alert_flag = True
						return render(request, 'manageteam.html', locals())
			return HttpResponseRedirect('/mainpage/')
	else:
		return HttpResponseRedirect('/login/')

def myinfo(request):
	if request.user.is_authenticated:
		if request.method == 'GET':
			current_user = request.user
			current_playing_sport = Playing_Sport.objects.filter(player = current_user)
			return render(request, 'myinfo.html', locals())
		if request.method == 'POST':
			current_user = request.user
			if request.POST.get('password'):
				password = request.POST.get('password')
				user = auth.authenticate(username=current_user.username, password=password)
				if user is not None and user.is_active == True:
					applying_team = request.POST.get('team')
					target_team = Team.objects.get(sport_name = applying_team)
					if target_team.sport_name == '羽球':
						Playing_Sport.objects.create(player = current_user, sport_name = target_team, points_left = 10)
					else:
						Playing_Sport.objects.create(player = current_user, sport_name = target_team)
				else:
					alert_flag = True
					team = Team.objects.all()
					return render(request, 'apply_team.html', locals())

		return HttpResponseRedirect('/mainpage/')
	else:
		return HttpResponseRedirect('/login/')