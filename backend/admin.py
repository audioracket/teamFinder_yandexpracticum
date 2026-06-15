from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Project, Skill


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личные данные', {
            'fields': ('name', 'surname', 'avatar', 'phone', 'github_url', 'about')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'surname', 'is_active', 'is_staff')
    search_fields = ('email', 'name', 'surname')
    ordering = ('email',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'description')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    