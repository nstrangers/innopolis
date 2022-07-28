from django.db import models

from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=250)                                                                        # название задачи
    description = models.TextField()                                                                                # описание задачи
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_author')                          # автор задачи
    status = models.CharField(max_length=1)                                                                         # Статус
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_executor')                      # исполнитель задачи

class Comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')