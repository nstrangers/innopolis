from django.urls import path
from .views import user_login, user_logout, add_task, main_page, edit_task, work_task

urlpatterns = [
    # post views
    path('', main_page, name='main'),
    path('login/', user_login),
    path('logout/', user_logout, name='logout'),
    path('add-task/', add_task),
    path('<int:pk>/edit/', edit_task, name='edittask'),
    path('<int:pk>/work/', work_task, name='worktask'),
]

