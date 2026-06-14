from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    
    # Projects
    path('projects/list/', views.project_list, name='project_list'),
    path('projects/create-project/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/complete/', views.project_complete, name='project_complete'),
    path('projects/<int:project_id>/toggle-participate', views.toggle_participate, name='toggle_participate'),
    
    # Skills (Вариант 3)
    path('projects/skills/', views.skills_autocomplete, name='skills_autocomplete'),
    path('projects/<int:project_id>/skills/add', views.add_skill_to_project, name='add_skill_to_project'),
    path('projects/<int:project_id>/skills/<int:skill_id>/remove/', views.remove_skill_from_project, name='remove_skill_from_project'),
    

    # Users
    path('users/list/', views.user_list, name='user_list'),
    path('users/register/', views.register, name='register'),
    path('users/login/', views.user_login, name='login'),
    path('users/logout/', views.user_logout, name='logout'),
    path('users/edit-profile/', views.edit_profile, name='edit_profile'),
    path('users/change-password/', views.change_password, name='change_password'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
]