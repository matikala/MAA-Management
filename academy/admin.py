from django.contrib import admin
from .models import *
# Register your models here.
# mateusz superuser123

admin.site.register(Trainer)
admin.site.register(Student)
admin.site.register(Section)
admin.site.register(Exam)
admin.site.register(Event)
