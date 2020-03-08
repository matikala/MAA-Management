from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required

from .models import *
from .forms import *

def index_view(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {'num_visits': num_visits}

    return render(request, 'index.html', context=context)


@permission_required('academy.can_manage_student')
def create_student(request):
    if request.method == "POST":
        user_form = UserCreateForm(request.POST, prefix="user")
        profile_form = StudentCreateForm(request.POST, prefix="profile")
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            my_group = Group.objects.get(name='student')
            my_group.user_set.add(user)
            return redirect('/')
    else:
        user_form = UserCreateForm(prefix="user")
        profile_form = StudentCreateForm(prefix="profile")
    context = {
        "user_form": user_form,
        "profile_form": profile_form
    }
    return render(request, 'student_form.html', context)


@permission_required('academy.can_manage_trainer')
def create_trainer(request):
    if request.method == "POST":
        user_form = UserCreateForm(request.POST, prefix="user")
        profile_form = TrainerCreateForm(request.POST, prefix="profile")
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            my_group = Group.objects.get(name='trainer')
            my_group.user_set.add(user)
            return redirect('/')
    else:
        user_form = UserCreateForm(prefix="user")
        profile_form = TrainerCreateForm(prefix="profile")
    context = {
        "user_form": user_form,
        "profile_form": profile_form
    }
    return render(request, 'trainer_form.html', context)



@permission_required('academy.can_read_student_personal')
def student_personal_view(request):
    student = Student.objects.get(user=request.user)
    context = {"student": student}
    return render(request, 'student_detail.html', context)


class TrainerListView(PermissionRequiredMixin, ListView):
    model = Trainer
    permission_required = 'academy.can_read_trainer_list'
    template_name = 'trainer_list.html'
    paginate_by = 10


class TrainerDetailView(PermissionRequiredMixin, DetailView):
    model = Trainer
    permission_required = 'academy.can_read_trainer_detail'
    template_name = 'trainer_detail.html'


@login_required
@permission_required('academy.can_manage_trainer')
def update_trainer(request, pk):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=Trainer.objects.get(pk=pk).user)
        profile_form = TrainerUpdateForm(request.POST, instance=Trainer.objects.get(pk=pk))

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('trainer-list')

    else:
        user_form = UserUpdateForm(instance=Trainer.objects.get(pk=pk).user)
        profile_form = TrainerUpdateForm(instance=Trainer.objects.get(pk=pk))

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'trainer_form.html', context)


@login_required
@permission_required('academy.can_manage_student')
def update_student(request, pk):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=Student.objects.get(pk=pk).user)
        profile_form = StudentUpdateForm(request.POST, instance=Student.objects.get(pk=pk))

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('student-list')

    else:
        user_form = UserUpdateForm(instance=Student.objects.get(pk=pk).user)
        profile_form = StudentUpdateForm(instance=Student.objects.get(pk=pk))

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'student_form.html', context)


class TrainerDelete(PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'academy.can_manage_trainer'
    success_url = reverse_lazy('trainer-list')
    template_name = 'trainer_confirm_delete.html'


class StudentListView(PermissionRequiredMixin, ListView):
    model = Student
    permission_required = 'academy.can_read_student_list'
    template_name = 'student_list.html'
    paginate_by = 10


class StudentDetailView(PermissionRequiredMixin, DetailView):
    model = Student
    permission_required = 'academy.can_read_student_detail'
    template_name = 'student_detail.html'


class StudentDelete(PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'academy.can_manage_student'
    success_url = reverse_lazy('student-list')
    template_name = 'student_confirm_delete.html'


class PrivilegeListView(PermissionRequiredMixin, ListView):
    model = Privilege
    permission_required = 'academy.can_read_privilege_list'
    template_name = 'privilege_list.html'
    paginate_by = 10


class PrivilegeDetailView(PermissionRequiredMixin, DetailView):
    model = Privilege
    permission_required = 'academy.can_read_privilege_detail'
    template_name = 'privilege_detail.html'


class PrivilegeCreate(PermissionRequiredMixin, CreateView):
    model = Privilege
    permission_required = 'academy.can_manage_privilege'
    fields = '__all__'
    template_name = 'privilege_form.html'


class PrivilegeUpdate(PermissionRequiredMixin, UpdateView):
    model = Privilege
    permission_required = 'academy.can_manage_privilege'
    fields = '__all__'
    template_name = 'privilege_form.html'


class PrivilegeDelete(PermissionRequiredMixin, DeleteView):
    model = Privilege
    permission_required = 'academy.can_manage_privilege'
    success_url = reverse_lazy('privilege-list')
    template_name = 'privilege_confirm_delete.html'


class SectionListView(PermissionRequiredMixin, ListView):
    model = Section
    permission_required = 'academy.can_read_section_list'
    template_name = 'section_list.html'
    paginate_by = 10


class SectionDetailView(PermissionRequiredMixin, DetailView):
    model = Section
    permission_required = 'academy.can_read_section_detail'
    template_name = 'section_detail.html'


class SectionCreate(PermissionRequiredMixin, CreateView):
    model = Section
    permission_required = 'academy.can_manage_section'
    fields = '__all__'
    template_name = 'section_form.html'


class SectionUpdate(PermissionRequiredMixin, UpdateView):
    model = Section
    permission_required = 'academy.can_manage_section'
    fields = '__all__'
    template_name = 'section_form.html'


class SectionDelete(PermissionRequiredMixin, DeleteView):
    model = Section
    permission_required = 'academy.can_manage_section'
    success_url = reverse_lazy('section-list')
    template_name = 'section_confirm_delete.html'


class TrainingListView(PermissionRequiredMixin, ListView):
    model = Training
    permission_required = 'academy.can_read_training_list'
    template_name = 'training_list.html'
    paginate_by = 10


class TrainingDetailView(PermissionRequiredMixin, DetailView):
    model = Training
    permission_required = 'academy.can_read_training_detail'
    template_name = 'training_detail.html'


class TrainingCreate(PermissionRequiredMixin, CreateView):
    model = Training
    permission_required = 'academy.can_manage_training'
    success_url = reverse_lazy('training-list')
    fields = '__all__'
    template_name = 'training_form.html'


class TrainingUpdate(PermissionRequiredMixin, UpdateView):
    model = Training
    permission_required = 'academy.can_manage_training'
    success_url = reverse_lazy('training-list')
    fields = '__all__'
    template_name = 'training_form.html'


class TrainingDelete(PermissionRequiredMixin, DeleteView):
    model = Training
    permission_required = 'academy.can_manage_training'
    success_url = reverse_lazy('training-list')
    template_name = 'training_confirm_delete.html'


class EventListView(PermissionRequiredMixin, ListView):
    model = Event
    permission_required = 'academy.can_read_event_list'
    template_name = 'event_list.html'
    paginate_by = 10


class EventDetailView(PermissionRequiredMixin, DetailView):
    model = Event
    permission_required = 'academy.can_read_event_detail'
    template_name = 'event_detail.html'


class EventCreate(PermissionRequiredMixin, CreateView):
    model = Event
    permission_required = 'academy.can_manage_event'
    fields = '__all__'
    template_name = 'event_form.html'


class EventUpdate(PermissionRequiredMixin, UpdateView):
    model = Event
    permission_required = 'academy.can_manage_event'
    fields = '__all__'
    template_name = 'event_form.html'


class EventDelete(PermissionRequiredMixin, DeleteView):
    model = Event
    permission_required = 'academy.can_manage_event'
    success_url = reverse_lazy('event-list')
    template_name = 'event_confirm_delete.html'


class CarnetListView(PermissionRequiredMixin, ListView):
    model = Carnet
    permission_required = 'academy.can_read_carnet_list'
    template_name = 'carnet_list.html'
    paginate_by = 10


class CarnetDetailView(PermissionRequiredMixin, DetailView):
    model = Carnet
    permission_required = 'academy.can_read_carnet_detail'
    template_name = 'carnet_detail.html'


class CarnetCreate(PermissionRequiredMixin, CreateView):
    model = Carnet
    permission_required = 'academy.can_manage_carnet'
    fields = '__all__'
    success_url = reverse_lazy('carnet-list')
    template_name = 'carnet_form.html'


class CarnetUpdate(PermissionRequiredMixin, UpdateView):
    model = Carnet
    permission_required = 'academy.can_manage_carnet'
    fields = '__all__'
    success_url = reverse_lazy('carnet-list')
    template_name = 'carnet_form.html'


class CarnetDelete(PermissionRequiredMixin, DeleteView):
    model = Carnet
    permission_required = 'academy.can_manage_carnet'
    success_url = reverse_lazy('carnet-list')
    template_name = 'carnet_confirm_delete.html'


class ExamListView(PermissionRequiredMixin, ListView):
    model = Exam
    permission_required = 'academy.can_read_exam_list'
    template_name = 'exam_list.html'
    paginate_by = 10


class ExamDetailView(PermissionRequiredMixin, DetailView):
    model = Exam
    permission_required = 'academy.can_read_exam_detail'
    template_name = 'exam_detail.html'


class ExamCreate(PermissionRequiredMixin, CreateView):
    model = Exam
    permission_required = 'academy.can_manage_exam'
    fields = '__all__'
    template_name = 'exam_form.html'


class ExamUpdate(PermissionRequiredMixin, UpdateView):
    model = Exam
    permission_required = 'academy.can_manage_exam'
    fields = '__all__'
    template_name = 'exam_form.html'


class ExamDelete(PermissionRequiredMixin, DeleteView):
    model = Exam
    permission_required = 'academy.can_manage_exam'
    success_url = reverse_lazy('exam-list')
    template_name = 'exam_confirm_delete.html'
