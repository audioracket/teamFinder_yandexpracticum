import http

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .constants import (PROJECT_STATUS_OPEN, PROJECT_STATUS_CLOSED,
                        SKILLS_AUTOCOMPLETE_LIMIT, USERS_PER_PAGE)
from .forms import (UserCreationForm, AuthenticationForm,
                    ProfileEditForm, ProjectForm, PasswordChangeForm)
from .models import User, Project, Skill
from .service import paginate


def index(request):
    return redirect('project_list')


def project_list(request):
    projects = Project.objects.select_related('owner').prefetch_related(
        'participants', 'skills'
    ).order_by('-created_at')
    active_skill = request.GET.get('skill')
    all_skills = Skill.objects.all().order_by('name')

    if active_skill:
        projects = projects.filter(skills__name=active_skill)

    page_obj = paginate(projects, request.GET.get('page'))

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
        if project.status == PROJECT_STATUS_OPEN:
            project.status = PROJECT_STATUS_CLOSED
            project.save()
            return JsonResponse({'status': 'ok', 'project_status': PROJECT_STATUS_CLOSED})
    return JsonResponse({'status': 'error'}, status=http.HTTPStatus.BAD_REQUEST)


@login_required
def toggle_participate(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        if project.participants.filter(id=request.user.id).exists():
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=http.HTTPStatus.BAD_REQUEST)


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('project_detail', project_id=project.id)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('project_detail', project_id=project.id)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


def skills_autocomplete(request):
    q = request.GET.get('q', '')
    skills = Skill.objects.filter(
        name__istartswith=q
    ).order_by('name')[:SKILLS_AUTOCOMPLETE_LIMIT]
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
            return JsonResponse(
                {'error': 'No skill provided'},
                status=http.HTTPStatus.BAD_REQUEST
            )

        if not project.skills.filter(id=skill.id).exists():
            project.skills.add(skill)
            added = True

        return JsonResponse({'skill_id': skill.id, 'created': created, 'added': added})
    return JsonResponse({'error': 'POST required'}, status=http.HTTPStatus.BAD_REQUEST)


@login_required
def remove_skill_from_project(request, project_id, skill_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        skill = get_object_or_404(Skill, id=skill_id)
        if project.skills.filter(id=skill.id).exists():
            project.skills.remove(skill)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Error'}, status=http.HTTPStatus.BAD_REQUEST)


def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    page_obj = paginate(users, request.GET.get('page'), per_page=USERS_PER_PAGE)
    return render(request, 'users/participants.html', {'participants': page_obj})


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user-details.html', {'user': user})


def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('project_list')
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('project_list')


@login_required
def edit_profile(request):
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('user_detail', user_id=request.user.id)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('user_detail', user_id=request.user.id)
    return render(request, 'users/change_password.html', {'form': form})
