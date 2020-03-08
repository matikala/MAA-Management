from django.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Student, Trainer


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')


class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['phone_number', 'born_date', 'enter_date', 'section_id']


class TrainerCreateForm(ModelForm):
    class Meta:
        model = Trainer
        fields = ['phone_number', 'born_date', 'master_degree', 'salary']


class UserUpdateForm(ModelForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class TrainerUpdateForm(ModelForm):
    class Meta:
        model = Trainer
        fields = ['phone_number', 'born_date', 'master_degree', 'salary']


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['phone_number', 'born_date', 'enter_date']
