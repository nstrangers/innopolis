from django.urls import path
from .views import user_login, add_task, main_page

urlpatterns = [
    # post views
    path('', main_page),
    path('login/', user_login),
    path('add-task/', add_task),
]

