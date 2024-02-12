from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    task_type = serializers.CharField(source='task.task_type')
    class Meta:
        model = Task
        fields = ('id', 'task_type', 'name', 'description', 'submission_date', 'is_completed','date_of_posted')

class TaskSerializerDate(serializers.ModelSerializer):
    task_type = serializers.CharField(source='task.task_type')
    assigned_teacher = serializers.SerializerMethodField()
    def get_assigned_teacher(self, instance):
        teachers = instance.assigned_teacher.all()
        return [{'id': teacher.id, 'first_name': teacher.user.first_name, 'last_name':teacher.user.last_name} for teacher in teachers]
    class Meta:
        model = Task
        fields = ('id', 'task_type', 'name', 'description', 'submission_date', 'is_completed', 'assigned_teacher')

class TaskUpdateSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    submission_date = serializers.DateField(required=False)
    age_group = serializers.IntegerField(required=True)
    type_of_task = serializers.IntegerField(required=False)

    def update(self, instance, validated_data, age_group):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.submission_date = validated_data.get('submission_date', instance.submission_date)
        instance.age_group = age_group
        instance.task_id = validated_data.get('type_of_task', instance.task_id)
        instance.save()
        return instance
    
class ActivitySerializer(serializers.ModelSerializer):
    task_type = serializers.CharField(source='task.task_type')
    assigned_teacher = serializers.SerializerMethodField()
    def get_assigned_teacher(self, instance):
        teachers = instance.assigned_teacher.all()
        return [{'id': teacher.id, 'first_name': teacher.user.first_name, 'last_name':teacher.user.last_name} for teacher in teachers]
    class Meta:
        model = Task
        fields = ('id', 'task_type', 'name', 'description', 'submission_date', 'is_completed','assigned_teacher')