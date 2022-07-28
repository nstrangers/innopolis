from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Task

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class NewTaskForm(forms.Form):
    CHOICES = [(x, x.first_name+' '+x.last_name) for x in User.objects.filter(groups__name='Исполнители')]
    title = forms.CharField(label='Название задачи')
    description = forms.CharField(widget=forms.Textarea, label='Описание задачи')
    executor = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='Исполнитель')
    status = forms.CharField(widget = forms.HiddenInput(), initial='0')

class EditTaskForm(ModelForm):
    CHOICES = [(x, x.first_name + ' ' + x.last_name) for x in User.objects.filter(groups__name='Исполнители')]
    title = forms.CharField(label='Название задачи')
    description = forms.CharField(widget=forms.Textarea, label='Описание задачи')
    status = forms.CharField(widget = forms.HiddenInput(), initial='0')
    executor = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Исполнители'), label='Исполнитель')
    class Meta:
        model = Task
        fields = ['title', 'description', 'executor', 'status']

class NewCommentForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea, label='Комментарий')
    class Meta:
        model = Task
        fields = ['comment']