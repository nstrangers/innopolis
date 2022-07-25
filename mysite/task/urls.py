from django.urls import path
from .views import user_login, add_task, main_page, edit_task

urlpatterns = [
    # post views
    path('', main_page),
    path('login/', user_login),
    path('add-task/', add_task),
    path('task/<int:pk>/edit/', edit_task),
]

