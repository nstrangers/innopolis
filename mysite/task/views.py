from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, NewTaskForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Task, Comments

@csrf_exempt
def main_page(request):
    return render(request, "task/main_page.html")

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
        a = User.objects.all()
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