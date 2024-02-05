from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    task_type = serializers.CharField(source='task.task_type')
    class Meta:
        model = Task
        fields = ('id', 'task_type', 'name', 'description', 'submission_date', 'is_completed')

class TaskSerializerDate(serializers.ModelSerializer):
    task_type = serializers.CharField(source='task.task_type')
    assigned_teacher = serializers.SerializerMethodField()
    def get_assigned_teacher(self, instance):
        teachers = instance.assigned_teacher.all()
        return [{'id': teacher.id, 'first_name': teacher.user.first_name, 'last_name':teacher.user.last_name} for teacher in teachers]
    class Meta:
        model = Task
        fields = ('id', 'task_type', 'name', 'description', 'submission_date', 'is_completed', 'assigned_teacher')