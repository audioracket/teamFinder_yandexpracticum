import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from .models import User, Project


class GithubUrlMixin:
    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and 'github.com' not in url:
            raise forms.ValidationError('Ссылка должна вести именно на Github.')
        return url


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'surname', 'email', 'password1', 'password2')


class AuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))


class ProfileEditForm(GithubUrlMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            digits = re.sub(r'\D', '', phone)
            if len(digits) == 11 and (digits.startswith('7') or digits.startswith('8')):
                formatted_phone = '+7' + digits[1:]
                if User.objects.filter(phone=formatted_phone).exclude(id=self.instance.id).exists():
                    raise forms.ValidationError('Этот номер телефона уже используется.')
                return formatted_phone
            raise forms.ValidationError('Формат: 8XXXXXXXXXX или +7XXXXXXXXXX')
        return phone


class ProjectForm(GithubUrlMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')


class PasswordChangeForm(PasswordChangeForm):
    pass
