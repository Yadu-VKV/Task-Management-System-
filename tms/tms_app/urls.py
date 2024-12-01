from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # # Home View - Redirects based on role
    # path('', views.home_view, name='home'),

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/pm/', views.pm_dashboard, name='pm_dashboard'),
    path('dashboard/tl/', views.tl_dashboard, name='tl_dashboard'),
    path('dashboard/tm/', views.tm_dashboard, name='tm_dashboard'),

    # Project Management
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),

    # Task Management
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/status/', views.update_task_status, name='update_task_status'),

    # User Management
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]
