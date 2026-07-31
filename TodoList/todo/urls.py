from django.contrib import admin
from django.urls import path
from .views import RegisterViewSet, ProfileViewSet, TaskViewSet, ListViewSet
from .views import index, list_detail, create_task, create_list, toggle_task, delete_list, delete_task, edit_task, logout_view, login_view, signup_page
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    #ath('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
   #path('signup/', RegisterViewSet.as_view({'post': 'create'}), name='signup'),
    path('profile/', ProfileViewSet.as_view({'get': 'list'}), name='profile'),
    path('tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='tasks'),
    path('tasks/<int:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task-detail'),
    path('lists/', ListViewSet.as_view({'get': 'list', 'post': 'create'}), name='lists'),
    path('lists/<int:pk>/', ListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='list-detail'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_page, name='signup'),
    path('', index, name='index'),
    path('list/<int:list_id>/', list_detail, name='list_detail'),
    path('list/<int:list_id>/create_task/', create_task, name='create_task'),
    path('create_list/', create_list, name='create_list'),
    path('task/<int:task_id>/toggle/', toggle_task, name='toggle_task'),
    path('list/<int:list_id>/delete/', delete_list, name='delete_list'),
    path('task/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('task/<int:task_id>/edit/', edit_task, name='edit_task'),

]