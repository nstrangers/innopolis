from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, NewTaskForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Task, Comments
from django.core import serializers
import json

def create_json():
    initial_data = json.loads(serializers.serialize('json', Task.objects.all()))
    result = []
    for temp in initial_data:
        task = temp['fields']
        task['id'] = temp['pk']
        task['author'] = User.objects.get(pk=task['author']).first_name + ' ' + User.objects.get(pk=task['author']).last_name
        task['executor'] = User.objects.get(pk=task['executor']).first_name + ' ' + User.objects.get(pk=task['executor']).last_name
        result.append(task)
    print(result)
    return result

@csrf_exempt
def main_page(request):
    user = User.objects.get(username=request.user.username).first_name + ' ' + User.objects.get(username=request.user.username).last_name
    return render(request, "task/main_page.html", {'user': user, 'data' : create_json()})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'task/login.html', {'form': form})


@csrf_exempt
def add_task(request):
    if request.method == "GET":
        executors_list=User.objects.filter(groups__name='Исполнители')
        newtaskform = NewTaskForm()
        return render(request, "task/new_task.html", {'User': executors_list, 'form': newtaskform})
    if request.method == "POST":
        new_task=NewTaskForm(request.POST)
        if new_task.is_valid():
            new_task=new_task.cleaned_data
            new_task['author']=User.objects.get(username=request.user.username)
            new_task['executor'] = User.objects.get(username=new_task['executor'])
            print(new_task)
            a=Task(**new_task)
            a.save()
        return HttpResponse('Ok')

@csrf_exempt
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        edit_form = NewTaskForm(request.POST, instance=task)
        if form.is_valid():

            return HttpResponse('Ok')
    if request.method == "GET":
        edit_form = NewTaskForm(instance=task)
    return render(request, 'blog/post_edit.html', {'form': edit_form})