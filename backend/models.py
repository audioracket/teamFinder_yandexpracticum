import io
import random
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, password, **extra_fields)


def generate_default_avatar(name):
    img = Image.new('RGB', (200, 200), color=(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)))
    d = ImageDraw.Draw(img)
    letter = name[0].upper() if name else '?'
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except IOError:
        font = ImageFont.load_default()
    
    bbox = d.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    d.text(((200-text_width)/2, (200-text_height)/2), letter, fill=(255, 255, 255), font=font)
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name=f'default_{name}.png')


class User(AbstractUser):
    
    username = None
    
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=124, verbose_name='Имя')
    surname = models.CharField(max_length=124, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    phone = models.CharField(max_length=12, blank=True, null=True, unique=True, verbose_name='Телефон')
    github_url = models.URLField(blank=True, null=True, verbose_name='GitHub')
    about = models.TextField(max_length=256, blank=True, null=True, verbose_name='О себе')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            self.avatar = generate_default_avatar(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Skill(models.Model):
    name = models.CharField(max_length=124, unique=True, verbose_name='Навык')

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    github_url = models.URLField(blank=True, null=True, verbose_name='GitHub')
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='open', verbose_name='Статус')
    participants = models.ManyToManyField(User, related_name='participated_projects', blank=True, verbose_name='Участники')
    skills = models.ManyToManyField(Skill, related_name='projects', blank=True, verbose_name='Необходимые навыки')

    def __str__(self):
        return self.name