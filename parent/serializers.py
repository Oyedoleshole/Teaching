from rest_framework import serializers
from parent.models import Parent
from student.models import Student
from task_app.models import Task
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description','submission_date'] 


class ChildActivityProgressSerializer(serializers.ModelSerializer):
    task_assign = TaskSerializer(many=True)
    class Meta:
        model = Student
        fields = ['id','first_name','last_name','image','task_assign','teacher','dob']