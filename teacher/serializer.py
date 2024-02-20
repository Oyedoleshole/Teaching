from rest_framework import serializers
from .models import Teacher
from task_app.models import Task, Task_type
from django.db import transaction
from student.models import Student

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = 'user.email')
    class Meta:
        model = Student
        fields = ['id', 'user', 'teacher']

class TaskSerializer(serializers.ModelSerializer):
    assigned_student = StudentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'submission_date', 'assigned_student']

class TeacherSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['user', 'students', 'tasks']
        
class TeacherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherlistingSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    date_and_time_of_task_assigned = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Teacher
        fields = ['email', 'students', 'image', 'date_and_time_of_task_assigned']


class ShowStudentRelateToTeacher(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Teacher
        fields = ['id','first_name','last_name','image']


class TaskAssignToStudentByTeacher(serializers.ModelSerializer):
    task = serializers.CharField()
    assigned_student = serializers.ListField(child=serializers.IntegerField(),write_only=True)
    class Meta:
        model = Task
        fields = ['task','name','description','submission_date','assigned_student']

    def validate(self, data):
        task_value = data.get('task',None)
        name = data.get('name', None)
        description = data.get('description', None)
        submission_date = data.get('submission_date', None)
        assigned_student = data.get('assigned_student',None)

        if not all(isinstance(teacher_id, int) for teacher_id in assigned_student):
            raise serializers.ValidationError("Invalid teacher ID(s)")
        if not task_value:
            raise serializers.ValidationError('Please provide task_type')
        if not name:
            raise serializers.ValidationError("name field is required")
        if not description:
            raise serializers.ValidationError("description is required")
        if not assigned_student:
            raise serializers.ValidationError('Please provide assigned_teachers_id')
        if not submission_date:
            pass
        try:
            data['task'] = Task_type.objects.get(id=task_value)
        except Task_type.DoesNotExist:
            raise serializers.ValidationError("Invalid task_type value")
        return data
    
    def create(self, validated_data):
        assigned_teacher_ids = validated_data.get('assign_teacher', [])
        task_type = validated_data.get('task', None)
        name = validated_data.get('name', '')
        description = validated_data.get('description', '')
        submission_date = validated_data.get('submission_date', '')
        with transaction.atomic():
            task_creation, created = Task.objects.get_or_create(
                task=task_type,
                name=name,
                description=description,
                submission_date=submission_date,
            )
            for teacher_id in assigned_teacher_ids:
                try:
                    teacher = Teacher.objects.get(id=teacher_id)
                    task_creation.assigned_teacher.add(teacher)
                except Teacher.DoesNotExist:
                    pass
        if created:
            response_message = "Task Assigned to student"
        else:
            response_message = "Task is already created"
        return {task_creation: response_message}

class TaskRemarkSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    image_or_file = serializers.FileField(required=False)
    tutor_remark = serializers.CharField()

    def validate_task_id(self, value):
        if not Task.objects.filter(id=value).exists():
            raise serializers.ValidationError("Task not found.")
        return value

class Task_Type_serializer(serializers.ModelSerializer):
    class Meta:
        model = Task_type
        fields = '__all__'

class TeacherActivityProgressSerializer(serializers.ModelSerializer):
    task_type = serializers.CharField(source='task.task_type')
    assigned_student = serializers.SerializerMethodField()
    def get_assigned_student(self, instance):
        students = instance.assigned_student.all()
        return [{'id': student.id, 'first_name': student.user.first_name, 'last_name':student.user.last_name} for student in students]
    class Meta:
        model = Task
        fields = ('id', 'task_type', 'name', 'description', 'submission_date', 'is_completed','assigned_student')