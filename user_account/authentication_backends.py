from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailMobileBackend(ModelBackend):
    def authenticate(self, request, email=None, mobile=None, password=None, **kwargs):
        UserModel = User
        if email:
            user = UserModel.objects.filter(email=email).first()
        elif mobile:
            user = UserModel.objects.filter(mobile=mobile).first()
        else:
            return None
        if user and user.check_password(password):
            return user
        return None
