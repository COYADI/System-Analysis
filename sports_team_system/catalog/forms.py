from django import forms

class Register_form(forms.Form):
	student_id = forms.CharField(max_length = 10)
	name = forms.CharField(max_length = 20)
	grade = forms.IntegerField()
	sex = forms.CharField(max_length = 1)
	password = forms.CharField(max_length = 256)