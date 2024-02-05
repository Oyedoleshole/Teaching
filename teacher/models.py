from django.db import models
from user_account.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='user_image', null=True, blank=True)
    students = models.ManyToManyField(to='student.Student', blank=True, related_name='teachers')
    date_of_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_and_time_of_task_assigned = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.email