from rest_framework import serializers
from .models import Task, Comments
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']

class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    executor = UserSerializer()
    class Meta:
        model = Task
        fields = ('__all__')

class CommentsSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comments
        fields = ('id','author','comment')