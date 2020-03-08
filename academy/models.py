from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    born_date = models.DateField()
    phone_number = models.IntegerField()
    master_degree = models.CharField(max_length=5)
    salary = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ['user']
        permissions = (("can_read_trainer_detail", "Can read trainer details"), ("can_manage_trainer", "Can manage trainers"), ('can_read_trainer_list', 'Can read trainers list'), )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse('trainer-detail', args=[str(self.id)])


class Privilege(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    document_name = models.CharField(max_length=100)
    obtain_date = models.DateField()
    expiration_date = models.DateField()
    trainer_id = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        permissions = (('can_read_privilege_list', 'Can read privileges list'), ("can_manage_privilege", "Can manage privileges"), ('can_read_privilege_detail', 'Can read privilege detail'), )


    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('privilege-detail', args=[str(self.id)])


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=70)
    amount_of_trainings = models.IntegerField()
    trainer_id = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    class Meta:
        ordering = ['location']
        permissions = (('can_read_section_list', 'Can read sections list'), ('can_manage_section', 'Can manage sections'), ('can_read_section_detail', 'Can read section detail'), )

    def __str__(self):
        return f'{self.location}'

    def get_absolute_url(self):
        return reverse('section-detail', args=[str(self.id)])


class Training(models.Model):
    id = models.AutoField(primary_key=True)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    date = models.DateField()
    amount_of_students = models.IntegerField()
    rental_price = models.DecimalField(max_digits=7, decimal_places=2)
    location = models.CharField(max_length=70)
    is_paid = models.BooleanField()

    class Meta:
        ordering = ['date']
        permissions = (("can_manage_training", "Can manage trainings"), ("can_read_training_detail", "Can read training details"), ('can_read_training_list', 'Can read trainings list'),)

    def __str__(self):
        return f'{self.date} {self.location}'

    def get_absolute_url(self):
        return reverse('training-detail', args=[str(self.id)])


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    phone_number = models.IntegerField()
    born_date = models.DateField()
    enter_date = models.DateField()
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user']
        permissions = (("can_read_student_detail", "Can read student details"), ("can_manage_student", "Can manage students"), ('can_read_student_list', 'Can read students list'), ('can_read_student_personal', 'Can read students personal'), )


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])

# Camp True, TraineeShip False
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    date = models.DateTimeField()
    location = models.CharField(max_length=70)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    event_type = models.BooleanField()
    amount_of_time = models.IntegerField(blank=True)
    amount_of_days = models.IntegerField(blank=True)
    students = models.ManyToManyField(Student)

    class Meta:
        ordering = ['date', 'name']
        permissions = (("can_manage_event", "Can manage events"), ('can_read_event_list', 'Can read events list'), ("can_read_event_detail", "Can read event details"),)


    def __str__(self):
        return f'{self.name} {self.date}'

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])


class Carnet(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.IntegerField()
    year = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_paid = models.BooleanField()
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        ordering = ['year', 'month']
        permissions = (("can_manage_carnet", "Can manage carnets"), ("can_read_carnet_list", "Can read carnets list"), ('can_read_carnet_detail', 'Can read carnet detail'), )

    def __str__(self):
        return f'{self.month} {self.year}'

    def get_absolute_url(self):
        return reverse('carnet-detail', args=[str(self.id)])


class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    degree = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField()
    is_paid = models.BooleanField()

    class Meta:
        ordering = ['id', 'date']
        permissions = (('can_read_exam_list', 'Can read exams list'), ("can_manage_exam", "Can manage exams"), ('can_read_exam_detail', 'Can read exam detail'), )



    def __str__(self):
        return f'{self.student_id} {self.degree}'

    def get_absolute_url(self):
        return reverse('exam-detail', args=[str(self.id)])
