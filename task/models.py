from django.db import models
from user_account.models import User
from teacher.models import Teacher
from student.models import Student

status_choice = (
    ('pending','Pending'),
    ('completed','Completed'),
    ('expired','Expired')
)
class AgeGroup(models.Model):
    age_group = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.age_group
        
class Task_type(models.Model):
    task_type = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.task_type
    
class Task(models.Model):
    age_group = models.ForeignKey(AgeGroup, on_delete=models.SET_NULL,null=True,blank=True)
    task = models.ForeignKey(Task_type, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    task_image_for_hint = models.FileField(upload_to='user_image',null=True, blank=True)
    assigned_teacher = models.ManyToManyField(Teacher, related_name="assigned_tasks", blank=True)
    assigned_student = models.ManyToManyField(Student, related_name="tasks", blank=True)
    tutor_remark = models.TextField(null=True, blank=True)
    submission_date = models.CharField(max_length=200, null=True,blank=True)
    is_completed = models.CharField(max_length=200,choices=status_choice, null=True,blank=True)
    date_of_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.teacher.user.email} - {self.task.name}"
