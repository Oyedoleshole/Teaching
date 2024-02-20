from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')
    class Meta:
        model = Student
        fields = ['user','teacher']