from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import User, Project, Skill
from .forms import (CustomUserCreationForm, CustomAuthenticationForm, 
                    ProfileEditForm, ProjectForm, CustomPasswordChangeForm)


def index(request):
    return redirect('project_list')


def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    active_skill = request.GET.get('skill')
    all_skills = Skill.objects.all().order_by('name')
    
    if active_skill:
        projects = projects.filter(skills__name=active_skill)
        
    paginator = Paginator(projects, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'projects/project_list.html', {
        'projects': page_obj,
        'all_skills': all_skills,
        'active_skill': active_skill
    })


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def project_complete(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        if project.status == 'open':
            project.status = 'closed'
            project.save()
            return JsonResponse({'status': 'ok', 'project_status': 'closed'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def toggle_participate(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        if request.user in project.participants.all():
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


def skills_autocomplete(request):
    q = request.GET.get('q', '')
    skills = Skill.objects.filter(name__istartswith=q).order_by('name')[:10]
    data = [{'id': s.id, 'name': s.name} for s in skills]
    return JsonResponse(data, safe=False)


@login_required
def add_skill_to_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        skill_id = request.POST.get('skill_id')
        name = request.POST.get('name')
        
        created = False
        added = False
        
        if skill_id:
            skill = get_object_or_404(Skill, id=skill_id)
        elif name:
            skill, created = Skill.objects.get_or_create(name=name)
        else:
            return JsonResponse({'error': 'No skill provided'}, status=400)
            
        if skill not in project.skills.all():
            project.skills.add(skill)
            added = True
            
        return JsonResponse({'skill_id': skill.id, 'created': created, 'added': added})
    return JsonResponse({'error': 'POST required'}, status=400)


@login_required
def remove_skill_from_project(request, project_id, skill_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        skill = get_object_or_404(Skill, id=skill_id)
        if skill in project.skills.all():
            project.skills.remove(skill)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Error'}, status=400)


def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'users/participants.html', {'participants': page_obj})


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user-details.html', {'user': user})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('project_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('project_list')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', user_id=request.user.id)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_detail', user_id=request.user.id)
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})