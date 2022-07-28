from rest_framework import serializers
from .models import Task, Comments
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.CharField(default=serializers.CurrentUserDefault())
    executor = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Task
        fields = ('__all__')

class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comments
        fields = ('id','author','comment')