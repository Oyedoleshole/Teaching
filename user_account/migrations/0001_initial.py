# Generated by Django 3.2.19 on 2024-02-14 07:22

import django.core.validators
from django.db import migrations, models
import user_account.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100, unique=True, validators=[user_account.models.CustomEmailValidator()])),
                ('first_name', user_account.models.OnlyCharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(255), django.core.validators.RegexValidator('^[a-zA-Z\\s]*$', message='Name should only contain alphabets and spaces.')])),
                ('last_name', user_account.models.OnlyCharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(255), django.core.validators.RegexValidator('^[a-zA-Z\\s]*$', message='Name should only contain alphabets and spaces.')])),
                ('mobile', user_account.models.mobile_num_validator(blank=True, max_length=50, null=True, unique=True, validators=[user_account.models.no_repeating_digits_validator, django.core.validators.MaxLengthValidator(10), django.core.validators.MinLengthValidator(6)])),
                ('password', models.CharField(max_length=200)),
                ('otp', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='user_image')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_parent', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', user_account.models.CustomUserManager()),
            ],
        ),
    ]
