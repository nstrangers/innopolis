from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, NewTaskForm, EditTaskForm, NewCommentForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Task, Comments
from django.core import serializers
from .serializer import TaskSerializer, CommentsSerializer
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
    if request.method =='POST':
        return redirect(add_task)
    else:
        if request.user.is_anonymous == False:
            tag_author='1' if request.user in User.objects.filter(groups__name='Заказчики') else '0'
            user = User.objects.get(username=request.user.username).first_name + ' ' + User.objects.get(username=request.user.username).last_name
            print(request.headers)
            return render(request, "task/main_page.html", {'user': user, 'data' : create_json(), 'tag_author': tag_author})
        else:
            return redirect(user_login)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(main_page)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'task/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect(main_page)
    # Redirect to a success page.

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
            new_task['author'] = User.objects.get(username=request.user.username)
            new_task['executor'] = User.objects.get(username=new_task['executor'])
            a=Task(**new_task)
            a.save()
        return redirect(main_page)

@csrf_exempt
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        edit_form = EditTaskForm(request.POST,instance=task)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponse('Ok')
    if request.method == "GET":
        edit_form = EditTaskForm(instance=task)
    return render(request, 'task/new_task.html', {'form': edit_form})

@csrf_exempt
def work_task(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "GET":
        newcommentform = NewCommentForm
        taskserializer = TaskSerializer(task)
        data = taskserializer.data
        data['user'] = request.user.username
        data['username'] = User.objects.get(username=data['user']).first_name + ' ' + User.objects.get(
            username=request.user.username).last_name
        data['form'] = newcommentform
        comments = Comments.objects.filter(task=task)
        commentserializer = CommentsSerializer(comments, many=True)
        data['comments']=json.loads(json.dumps(commentserializer.data))
        print(data)

        return render(request, 'task/work_task.html', data)
    if request.method == "POST":
        if 'take-to-work' in request.POST: #нажали кнопку принять в работу
            task.status='1'
            task.save()
        elif 'task-completed' in request.POST: #нажали кнопку работа выполнена
            task.status='2'
            task.save()
        elif 'task-confirm' in request.POST: #нажали кнопку работа выполнена
            task.status='3'
            task.save()
        elif 'task-not-confirm' in request.POST: #нажали кнопку работа выполнена
            task.status='0'
            task.save()
        elif 'delete-task' in request.POST:  # нажали кнопку удалить задачу
            task.status = '0'
            task.delete()
        elif 'add-comment' in request.POST:  # нажали кнопку добавить комментарий
            new_comment = NewCommentForm(request.POST)
            if new_comment.is_valid():
                print('form ok')
                new_comment = new_comment.cleaned_data
                new_comment['author'] = User.objects.get(username=request.user.username)
                new_comment['task'] = Task.objects.get(pk=pk)
                a = Comments(**new_comment)
                a.save()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            else:
                return HttpResponse('Error form')
    return redirect(main_page)