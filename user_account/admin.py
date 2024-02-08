from django.contrib import admin
from .models import User
from task_app.models import Task, Task_type, Assignment, AgeGroup
from student.models import Student
from teacher.models import Teacher, TeacherAddRemarkandImageForExistinceTask
from parent.models import Parent
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile', 'is_parent', 'is_superuser', 'is_student','is_teacher')
    search_fields = ('first_name', 'last_name', 'email')
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

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','name','description','date_of_posted']
    inlines = [
        TeacherInlineAdmin
    ]
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id','user','date_of_posted')

admin.site.register(AgeGroup)
admin.site.register(Student)
admin.site.register(Task_type)
admin.site.register(Assignment)
admin.site.register(Parent)
