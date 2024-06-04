from django import forms
from work.models import User,Taskmodel

class Register(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name',"last_name","email","password"]
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'enter the username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'enter the firstname'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'enter the lastname'}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'enter the email'}),
            'password':forms.TextInput(attrs={'class':'form-control','placeholder':'enter the password'})
            }


class TaskForm(forms.ModelForm):
    class Meta:
        model=Taskmodel
        fields=["task_name","task_description"]
        widgets={
            'task_name':forms.TextInput(attrs={'class':'form-control','placeholder':'enter the task name'}),
            'task_description':forms.Textarea(attrs={'class':'form-control','column':20,'row':5,'placeholder':'enter the description'})
        }


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
