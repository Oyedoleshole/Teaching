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
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import permission_classes
from parent.models import Parent
from task_app.models import Task

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


