from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.contrib.auth.password_validation import  validate_password
import uuid
# from teacher.models import Teacher

# from Cart.models import Cart

class CustomPasswordValidator(object):
    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(f"The password must be at least {self.min_length} characters long.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("The password must contain at least one special character.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("The password must contain at least one numeric digit.")
        if not any(char.isupper() for char in password):
            raise ValidationError("The password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise ValidationError("The password must contain at least one lowercase letter.")

    def get_help_text(self):
        return f"The password must be at least {self.min_length} characters long. It must also contain at least one special character and one uppercase letter."


User._meta.get_field('first_name').validators.append(MinLengthValidator(3))
User._meta.get_field('first_name').validators.append(MaxLengthValidator(25))

User._meta.get_field('last_name').validators.append(MinLengthValidator(3))
User._meta.get_field('last_name').validators.append(MaxLengthValidator(25))


class CustomEmailValidator(EmailValidator):
    regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    message = 'Enter a valid email address.'
    code = 'invalid_email'

class OnlyCharField(models.CharField):
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        value_str = str(value)
        pattern = r'^[a-zA-Z\s]*$'
        if not re.match(pattern, value_str):
            raise ValidationError("Only characters are allowed")

        
class mobile_num_validator(models.CharField):
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        value_str = str(value)
        pattern = r'[0-9]+$'
        if not re.match(pattern,value_str):
            raise ValidationError("Mobile number should be digits not characters")


class PincodeValidator(models.CharField):
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        value_str = str(value)
        if len(value_str) < 6:
            raise ValidationError("Pincode must be 6 digits")
        pattern = r'^[0-9]+$'
        if not re.match(pattern, value_str):
            raise ValidationError("Pincode should be numeric")
        no_repeating_pincode_digits_validator(value_str)

    def max_length(self):
        return self.validators[-1].limit_value
        

# class pan_number_validator(models.CharField):
#     def validate(self, value, model_instance):
#         super().validate(value, model_instance)
#         value_str = str(value) 
#         if len(value_str) < 10:
#             raise ValidationError("Pan number should be 10 alphanumeric digits")
#         pattern = r'[A-Z0-9]+$'
#         if not re.match(pattern, value_str):
#             raise ValidationError("Pan number should be alphanumeric")
#         no_repeating_value_in_pan(value_str)

#     def max_length(self):
#         return self.validators[-1].limit_value
        
# class aadhar_number_validation(models.CharField):
#     def validate(self, value, model_instance):
#         super().validate(value, model_instance)
#         value_str = str(value)
#         if len(value_str) < 12:
#             raise ValidationError("Aadhar number should be 12 digits")
#         pattern = r'[0-9]+$'
#         if not re.match(pattern, value_str):
#             raise ValidationError("Aadhar number should be numeric")
#         no_repeating_value_in_aadhar(value_str)

#     def max_length(self):
#         return self.validators[-1].limit_value

def no_repeating_digits_validator(value):
    str_value = str(value)
    if len(set(str_value)) == 1:
        raise ValidationError('Mobile number should not have the same digits')

def no_repeating_pincode_digits_validator(value):
    str_value = str(value)
    if len(set(str_value)) == 1:
        raise ValidationError("Pincode digits should not have the same digits")

def no_repeating_value_in_pan(value):
    str_value = str(value)
    if len(set(str_value)) == 1:
        raise ValidationError("Pan number should contain 10 alphanumeric digits")

def no_repeating_value_in_aadhar(value):
    str_value = str(value)
    if len(set(str_value)) == 1:
        raise ValidationError("Aadhar number should contain 12 digits")
    
# Create your models here.
class CustomUserManager(BaseUserManager,):
    use_in_migrations = True
    def _create_user(self, email, password, first_name, last_name, mobile, **extra_fields,):
        if not email:
            raise ValueError('Email Must Be Provided')
        if not password:
            raise ValueError('Password is not Provided')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
#For Customer
    def __create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('Please Provide Email')
        if not password:
            raise ValueError('Please Provide Password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user    
#Distributor 
    def make_distributor(self, email, password, first_name, last_name, mobile, **extra_fields):
        if not email:
            raise ValueError('Please Provide Email')
        if not password:
            raise ValueError('Please Provide Password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
#Parent
    def make_parent(self, email, password, first_name, last_name, mobile, **extra_fields):
        if not email:
            raise ValueError('Please Provide Email11')
        if not password:
            raise ValueError('Please Provide Password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
#for Parent
    def create_parent(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_verified',False)
        extra_fields.setdefault('is_parent', True)
        return self.make_parent(email, password, first_name, last_name, mobile, **extra_fields)

# for Student or Children
    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_verified',False)
        extra_fields.setdefault('is_student', True)
        return self.__create_user(email, password, first_name, last_name, **extra_fields)

# for Super Admin
    def create_superuser(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_verified',False)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)

# for Tutor
    def create_teacher(self, email, password, first_name,last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_verified',False)
        extra_fields.setdefault('is_teacher',True)
        return self.make_distributor(email, password, first_name, last_name, mobile, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin,):
    #AbstractBaseUser has only three fields{Password, Last_login, Is_active}
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True, max_length=100, validators=[CustomEmailValidator()])
    first_name=OnlyCharField(max_length=255,validators=[
        MinLengthValidator(3),
        MaxLengthValidator(255),
        RegexValidator(r'^[a-zA-Z\s]*$',
                       message='Name should only contain alphabets and spaces.')
    ])
    last_name=OnlyCharField(max_length=255,validators=[
        MinLengthValidator(3),
        MaxLengthValidator(255),
        RegexValidator(r'^[a-zA-Z\s]*$',
                       message='Name should only contain alphabets and spaces.')
    ])
    mobile=mobile_num_validator(validators=[no_repeating_digits_validator, MaxLengthValidator(10), MinLengthValidator(6)],max_length=50, unique=True, null=True, blank=True)
    password = models.CharField(max_length=200)
    otp=models.IntegerField(default=int(0000))
    image = models.ImageField(upload_to="user_image",null=True, blank=True)

    is_staff=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    is_parent=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    is_teacher=models.BooleanField(default=False)


    objects=CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','mobile']

    def validate_password(self, password):
        try:
            validate_password(password, self)
        except ValidationError as e:
            return ValidationError(
                "Your password must contain at least %(min_length)d characters.6"
            )

    def save(self, *args, **kwargs):
        self.validate_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def clean(self):
        super().clean()
        validator = CustomPasswordValidator(6)
        validator.validate(self.password, self)
        self.set_password(self.password)
    
    def __str__(self):
        return self.email