from django.db import models
from user_account.models import User
# Create your models here.

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='user_image',null=True, blank=True)
    childrens = models.ManyToManyField(to='student.Student',blank=True,related_name='parents')
    date_of_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.email