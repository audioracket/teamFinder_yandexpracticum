# backend/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from .constants import (PROJECT_STATUS_OPEN, PROJECT_STATUS_CLOSED,
                        MAX_LENGTH_NAME, MAX_LENGTH_ABOUT, MAX_LENGTH_PHONE,
                        MAX_LENGTH_PROJECT_NAME, MAX_LENGTH_STATUS)
from .managers import UserManager
from .service import generate_default_avatar


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=MAX_LENGTH_NAME, verbose_name='Имя')
    surname = models.CharField(max_length=MAX_LENGTH_NAME, verbose_name='Фамилия')
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True, verbose_name='Аватар'
    )
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE, blank=True, null=True,
        unique=True, verbose_name='Телефон'
    )
    github_url = models.URLField(blank=True, null=True, verbose_name='GitHub')
    about = models.TextField(
        max_length=MAX_LENGTH_ABOUT, blank=True, null=True, verbose_name='О себе'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            self.avatar = generate_default_avatar(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Skill(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME, unique=True, verbose_name='Навык')

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        (PROJECT_STATUS_OPEN, 'Open'),
        (PROJECT_STATUS_CLOSED, 'Closed'),
    ]

    name = models.CharField(max_length=MAX_LENGTH_PROJECT_NAME, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='owned_projects', verbose_name='Автор'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    github_url = models.URLField(blank=True, null=True, verbose_name='GitHub')
    status = models.CharField(
        max_length=MAX_LENGTH_STATUS, choices=STATUS_CHOICES,
        default=PROJECT_STATUS_OPEN, verbose_name='Статус'
    )
    participants = models.ManyToManyField(
        User, related_name='participated_projects',
        blank=True, verbose_name='Участники'
    )
    skills = models.ManyToManyField(
        Skill, related_name='projects',
        blank=True, verbose_name='Необходимые навыки'
    )

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'project_id': self.id})

    def __str__(self):
        return self.name
    