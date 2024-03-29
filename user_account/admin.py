from typing import Any
from django.contrib.auth.models import Group
from django.contrib import admin
from .models import User
from task_app.models import Task, Task_type, Assignment, AgeGroup
from student.models import Student
from teacher.models import Teacher, TeacherAddRemarkandImageForExistinceTask
from parent.models import Parent
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPResponseException
from django.contrib.auth.hashers import make_password

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile', 'is_parent', 'is_superuser', 'is_student','is_teacher')
    exclude = ('is_active', 'is_staff',)
    search_fields = ('first_name', 'last_name', 'email')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if 'password' in form.changed_data:
            plain_password = form.cleaned_data['password']
            if obj.is_teacher and obj.is_parent:
                Teacher.objects.create(user=obj)
                Parent.objects.create(user=obj)
            elif obj.is_teacher:
                Teacher.objects.create(user=obj)
            elif obj.is_parent:
                Parent.objects.create(user=obj)
        send_mail("Congratulations! Your Account Details", f"Email: {obj.email}, Password: {plain_password}", 'sharmaeshu54@gmail.com', [obj.email], fail_silently=False)
        
    # ordering = ['email']
    # ordering = ['email']
    # def staff_status(self, obj):
    #     return obj.is_staff
    # staff_status.boolean = True
    # staff_status.short_description = 'Teacher'

    # def active_status(self, obj):
    #     return obj.is_active
    # active_status.boolean = True
    # active_status.short_description = 'Student'

    # def superuser_status(self, obj):
    #     return obj.is_superuser  
    # superuser_status.boolean = True
    # superuser_status.short_description = 'Admin'
admin.site.register(TeacherAddRemarkandImageForExistinceTask)
class TeacherInlineAdmin(admin.TabularInline):
    model = TeacherAddRemarkandImageForExistinceTask
    extra = 1
class AssessmentAdmin(admin.TabularInline):
    model = Assignment
    extra = 1
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','name','description','date_of_posted']
    inlines = [
        AssessmentAdmin,
        TeacherInlineAdmin,
    ]
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id','user','date_of_posted')
    inlines = [AssessmentAdmin]
    
admin.site.register(AgeGroup)
admin.site.register(Student)
admin.site.register(Task_type)
admin.site.register(Parent)
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['id','completion_date','task',
    'teacher',
    'student',
    'is_completed',
    ]
admin.site.unregister(Group)
admin.site.site_header = "Teaching Administration"
admin.site.site_title = "Teaching"