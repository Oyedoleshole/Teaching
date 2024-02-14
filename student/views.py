from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .serializers import StudentSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from user_account.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import permission_classes
from parent.models import Parent
from task_app.models import Task, Assignment
from django.db.models import Q
from task_app.serializers import TaskSerializer
import datetime

class Student_class(APIView):
    def get(self, request):
        student_objects = Student.objects.all()
        serializer = StudentSerializer(student_objects, many=True)
        if serializer.is_valid:
            return JsonResponse({"data":serializer.data},status=status.HTTP_200_OK)
        return JsonResponse({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class StudentLogin(APIView):
    def post(self, request):
        student_email = request.POST.get('student_email')
        try:
            student_user = User.objects.get(email=student_email)
            authenticate(email=student_user, password=student_user.password)
            refresh = AccessToken.for_user(student_user)
            return JsonResponse({"message":"login successfully","access_token":str(refresh)},status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"Student email not found"},status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_student_details(request):
    try:
        print(request.user)
        get_student_from_student_table = Student.objects.get(user=request.user)
        student_details = Parent.objects.get(childrens=get_student_from_student_table)
        print(student_details)
    except Parent.DoesNotExist and Student.DoesNotExist and Exception as e:
        print("error")
        return JsonResponse(str(e),safe=False)

#API for Student Profile Details.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_profile_details(request):
    try:
        get_student_from_student_table = Student.objects.get(user=request.user)
        student_details = Parent.objects.get(childrens=get_student_from_student_table)
        if not get_student_from_student_table.image:
            return JsonResponse({"student_details":[{"first_name":get_student_from_student_table.first_name,"last_name":get_student_from_student_table.last_name,"email":request.user.email,"dob":get_student_from_student_table.dob}],"parent_details":[{"first_name":student_details.user.first_name,"last_name":student_details.user.last_name,"email":student_details.user.email,"mobile":student_details.user.mobile}]}, safe=False)
        return JsonResponse({"student_details":[{"first_name":get_student_from_student_table.first_name,"last_name":get_student_from_student_table.last_name,"email":request.user.email,"image":get_student_from_student_table.image.url,"dob":get_student_from_student_table.dob}],"parent_details":[{"first_name":student_details.user.first_name,"last_name":student_details.user.last_name,"email":student_details.user.email,"mobile":student_details.user.mobile}]}, safe=False)
    except Parent.DoesNotExist and Student.DoesNotExist and Exception as e:
        print("error")
        return JsonResponse(str(e),safe=False)        

#Filter the Task with Date, Multiple Types of Tasks.
class FilterTaskForStudent(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        date = request.GET.get('date')
        type_of_task_ids = request.GET.getlist('type_of_task_id', None)
        if not date:
            return Response({"message": "Please provide date in format YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if type_of_task_ids and date:
                q_objects = Q()
                for task_id in type_of_task_ids:
                    q_objects |= Q(task=task_id)
                task_details = Task.objects.filter(q_objects, assigned_student=request.user.email,date_of_posted=date)
                serializer = TaskSerializer(task_details, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"message":"Error"},status=400)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TaskDoneByStudentAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        task_id = request.data.get('task_id')
        assessment_file = request.FILES.get('assessment_file')
        if not task_id:
            return Response({"message": "Please provide task_id"}, status=status.HTTP_400_BAD_REQUEST)
        if not assessment_file:
            return Response({"message": "Please provide assessment_file"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            task = Task.objects.get(id=task_id)
            user = User.objects.get(email=request.user.email)
            student = Student.objects.get(user=user)
            getting_the_teacher = Teacher.objects.get(students=student)
            if getting_the_teacher:
                print("The Teacher is===>", getting_the_teacher)
            else:
                print("No Teacher found")
            Assignment.objects.get_or_create(teacher=getting_the_teacher, student=student, task=task, assessment_file=assessment_file)
            return Response({"message": "Task Completed"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)