from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class NewTaskForm(forms.Form):
    CHOICES = [(x, x.first_name+' '+x.last_name) for x in User.objects.filter(groups__name='Исполнители')]
    title = forms.CharField(label='Название задачи')
    description = forms.CharField(widget=forms.Textarea, label='Описание задачи')
    executor = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='Исполнитель')
    status = forms.CharField(widget = forms.HiddenInput(), initial='0')