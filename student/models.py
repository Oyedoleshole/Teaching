from django.db import models
from user_account.models import User
from teacher.models import Teacher

class Student(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    image = models.FileField(upload_to='user_image',null=True, blank=True)
    task_assign = models.ManyToManyField(to='task_app.task',blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    dob = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.email