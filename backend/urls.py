from django.urls import path, include

from . import views

projects_urls = [
    path('list/', views.project_list, name='project_list'),
    path('create-project/', views.create_project, name='create_project'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/complete/', views.project_complete, name='project_complete'),
    path('<int:project_id>/toggle-participate', views.toggle_participate, name='toggle_participate'),
    path('skills/', views.skills_autocomplete, name='skills_autocomplete'),
    path('<int:project_id>/skills/add', views.add_skill_to_project, name='add_skill_to_project'),
    path('<int:project_id>/skills/<int:skill_id>/remove/', views.remove_skill_from_project, name='remove_skill_from_project'),
]

users_urls = [
    path('list/', views.user_list, name='user_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', include(projects_urls)),
    path('users/', include(users_urls)),
]
