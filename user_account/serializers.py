import sys
from rest_framework import serializers
from user_account.models import User
import re
import random
from task_app.models import Task, Task_type, AgeGroup
from django.contrib.auth import authenticate
from student.models import Student
from teacher.models import Teacher
from django.db.models import Q
from django.db import transaction
from parent.models import Parent
from datetime import datetime

class RegisterSerializer(serializers.ModelSerializer):
    for_value = serializers.CharField(max_length=10, required=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','email','mobile','password','for_value']

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{6,}$', value):
            raise serializers.ValidationError("Password must meet the criteria: at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        return value
    def create(self, validated_data):
        value = validated_data.get('for_value')
        if value == 'superuser':
            user = User.objects.create_superuser(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                otp=str(random.randint(1000, 9999)),
                mobile = validated_data['mobile']
            )
        elif value == 'student':
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                otp=str(random.randint(1000, 9999)),
                mobile = validated_data['mobile']
            )
            student = Student.objects.create(user=user)
        elif value == 'teacher':
            user = User.objects.create_teacher(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                otp=str(random.randint(1000, 9999)),
                mobile = validated_data['mobile']
            )
            teacher = Teacher.objects.create(user=user)
        elif value == 'parent':
            user = User.objects.create_parent(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                otp=str(random.randint(1000, 9999)),
                mobile = validated_data['mobile']
            )
            parent = Parent.objects.create(user=user)
        else:
            raise serializers.ValidationError("Invalid value for 'for_student'")
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=False)
    mobile = serializers.CharField(max_length=200, required=False)
    for_value = serializers.CharField(max_length=50, required=False)
    # password = serializers.CharField(input=password)
    class Meta:
        model = User
        fields = ['email','password','mobile','for_value']

class TaskCreationforAdminSerializer(serializers.ModelSerializer):
    task = serializers.CharField()
    assign_teacher = serializers.ListField(child=serializers.IntegerField(),write_only=True)
    class Meta:
        model = Task
        fields = ['task','name','description','submission_date','assign_teacher','age_group']

    def validate(self, data):
        task_value = data.get('task',None)
        name = data.get('name', None)
        description = data.get('description', None)
        submission_date = data.get('submission_date', None)
        assigned_teachers = data.get('assign_teacher',None)
        age_group_value =  data.get('age_group')
        if not all(isinstance(teacher_id, int) for teacher_id in assigned_teachers):
            raise serializers.ValidationError("Invalid teacher ID(s)")
        if not task_value:
            raise serializers.ValidationError('Please provide task_type')
        if not name:
            raise serializers.ValidationError("name field is required")
        if not description:
            raise serializers.ValidationError("description is required")
        if not assigned_teachers:
            raise serializers.ValidationError('Please provide assigned_teachers_id')
        if not age_group_value:
            raise serializers.ValidationError('Select the age group')
        if not submission_date:
            pass
        try:
            data['age_group'] = AgeGroup.objects.get(age_group=age_group_value)
            data['task'] = Task_type.objects.get(id=task_value)
        except AgeGroup.DoesNotExist:
            raise serializers.ValidationError(f'Invalid age_group value.')
        except Task_type.DoesNotExist:
            raise serializers.ValidationError(f'Invalid task_type value.')
        return data

    def create(self, validated_data):
        assigned_teacher_ids = validated_data.get('assign_teacher', [])
        task_type = validated_data.get('task', None)
        name = validated_data.get('name', '')
        description = validated_data.get('description', '')
        submission_date = validated_data.get('submission_date', '')
        age_group = validated_data.get('age_group')
        with transaction.atomic():
            task_creation, created = Task.objects.get_or_create(
                task=task_type,
                name=name,
                description=description,
                submission_date=submission_date,
                age_group=age_group
            )
            for teacher_id in assigned_teacher_ids:
                try:
                    teacher = Teacher.objects.get(id=teacher_id)
                    teacher.task_assign.add(task_creation)
                    teacher.date_and_time_of_task_assigned = datetime.now()
                    teacher.save()
                    task_creation.assigned_teacher.add(teacher)
                except Teacher.DoesNotExist:
                    pass
        if created:
            response_message = "Task Created Successfully"
        else:
            response_message = "Task is already created"
        return {task_creation: response_message}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','mobile']

class ChildActivityProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','first_name','last_name','image','task_assign','teacher','dob']