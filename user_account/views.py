from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from user_account.models import User
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer, TaskCreationforAdminSerializer, UserSerializer, ChildActivityProgressSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPResponseException
from django.template.loader import render_to_string
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import random
from parent.models import Parent
from student.models import Student
from task_app.models import Task

class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError("There is no user registered with the specified email address!")
        return email
        
class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        serializer = RegisterSerializer(data=data)
        data=data
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            otp = result.otp
            try:
                subject = "One Time Password"
                context = {
                    'otp':otp
                    }
                email_context = render_to_string("otp.txt", context)
                send_mail(subject, email_context, 'sharmaeshu54@gmail.com', [email], fail_silently=False)
                return Response({"message":"User created successfully"},status=status.HTTP_201_CREATED)
            except BadHeaderError and SMTPResponseException:
                return Response({"message":"SMTP Error"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if not email or not new_password or not confirm_password:
            message="Please provide all the fields -> email, new_password, confirm_password"
            return Response({"message":message},status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return JsonResponse({'message':'Passwords do not match'}, status=400)
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return JsonResponse({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return JsonResponse({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        
#Password Change API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change(request):
    email = request.user.email
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')
    if not old_password or not new_password or not confirm_password:
        message="Please provide all the fields -> old_password, new_password, confirm_password"
        return Response({"message":message},status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(email=email)
    if not user.check_password(old_password):
        return JsonResponse({"message": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    if new_password!= confirm_password:
        return JsonResponse({'message':'Passwords do not match'}, status=400)
    user.set_password(new_password)
    user.save()
    return JsonResponse({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def email_verification(request):
    try:
        email = request.data.get('email')
        otp = int(request.data.get('otp'))
        if not email or not otp:
            return JsonResponse({"email":"Email is required","otp":"otp is required"}, status=status.HTTP_400_BAD_REQUEST)
        get_the_mobile_from_the_databases = User.objects.filter(email=email)
        for user in get_the_mobile_from_the_databases:
            if user.is_verified:
                return JsonResponse({"message":'Email is already Verified'},status=status.HTTP_200_OK)
        if get_the_mobile_from_the_databases.exists():
            for user in get_the_mobile_from_the_databases:
                if user.otp == otp:
                    user.is_verified = True
                    user.otp = 0
                    user.save()
                    return JsonResponse({"message": "OTP verified"}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"message": "Incorrect OTP"}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse({"message": "Please fill all the details","otp":otp,}, status=status.HTTP_200_OK)  
        return JsonResponse({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": "Something went wrong","otp":"None"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data.get('email')
        mobiles = serializer.validated_data.get('mobile')
        password = serializer.validated_data.get('password')
        for_value = serializer.validated_data.get('for_value')
        if not email and not mobiles:
            return Response({'message': 'Either email or mobile must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not for_value:
            return Response({'message': 'Please enter for value','values':'admin,parent,teacher,children'}, status=status.HTTP_400_BAD_REQUEST)
        if for_value:
            user = None
            if email:
                user = authenticate(request, email=email, password=password)
                print("User is authenticate",user)
            elif mobiles:
                user = authenticate(request,mobile=mobiles, password=password)
                print("User is authenticate with his mobile",user)
            if user is None:
                return Response({'message': 'Either Email or Password is incorrect or the user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                exist_user = User.objects.get(email=user.email)
                if exist_user.is_verified is False:
                    # return Response({"message": "Please verify first"}, status=status.HTTP_400_BAD_REQUEST)
                    pass
                if for_value == "admin" and exist_user.is_superuser == True:
                    refresh = RefreshToken.for_user(user)
                    return Response({'message': "Login successfully", 'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
                elif for_value == "parent" and exist_user.is_parent == True:
                    know_to_have_childrens = Parent.objects.get(user=user)
                    children = know_to_have_childrens.childrens.all().exists()
                    refresh = RefreshToken.for_user(user)
                    return Response({'message': "Login successfully", 'access_token': str(refresh.access_token),'childrens':children}, status=status.HTTP_200_OK)
                elif for_value == 'children' and exist_user.is_student == True:
                    refresh = RefreshToken.for_user(user)
                    return Response({'message': "Login successfully", 'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
                elif for_value == 'teacher' and exist_user.is_teacher == True:
                    refresh = RefreshToken.for_user(user)
                    return Response({'message': "Login successfully", 'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def resend_otp(request):
    try:
        email = request.data.get('email')
        if not email:
            return JsonResponse({"message":"Please enter Email"},status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=email)
        try:
            subject = "One Time Password"
            context = {
            "email": email,
            'otp':str(random.randint(1000,9999))
            }
            email_context = render_to_string("otp.txt", context)
            send_mail(subject, email_context, 'sharmaeshu54@gmail.com', [email], fail_silently=False)
        except BadHeaderError:
            return JsonResponse({"message":"Uncaught Error"},status=status.HTTP_400_BAD_REQUEST)
        user.otp = int(context['otp'])
        user.save()
        return JsonResponse({"message":"OTP is sent successfully"},status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return JsonResponse({"message":"User is None"},status=status.HTTP_400_BAD_REQUEST)

class Task_added_by_admin(APIView):
    def post(self, request):
        serializer = TaskCreationforAdminSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Task added successfully"},status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_any_account(request):
    try:
        id = request.user.id
        user = User.objects.get(id=id)
        user.delete()
        return Response({"message":"Account deleted successfully"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":"User not found",},status=status.HTTP_404_NOT_FOUND)

#Show For All Users Details.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_user_details(request):
    user = User.objects.get(email=request.user)
    serializer = UserSerializer(user)
    return Response({'data':serializer.data}, status=200)

#Activity Progress for Parent.
from datetime import datetime
class ActivityProgressForParent(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        result = []
        date_of_task = request.GET.get('date')
        if not date_of_task:
            return JsonResponse({"message": "Please provide date in format YYYY-MM-DD"}, status=400)
        date_of_task = datetime.strptime(date_of_task, '%Y-%m-%d').date()
        parent = Parent.objects.get(user=request.user)
        children_they_have = parent.childrens.all()
        for child in children_they_have:
            user = User.objects.get(email=child)
            get_the_data_for_requested_child = Student.objects.filter(user=user)
            result.append(get_the_data_for_requested_child)
        # print("Get the data for the requested child========>",result)
            serializer = ChildActivityProgressSerializer(get_the_data_for_requested_child, many=True)
            if serializer.is_valid:
                return Response({'data':serializer.data},status=200)
            return Response({'message':serializer.errors},status=400)
        # get_the_data_for_requested_teacher = Task.objects.filter(assigned_teacher=teacher, date_of_posted = date_of_task)
        # serializer = TeacherActivityProgressSerializer(get_the_data_for_requested_teacher, many=True)
        # if serializer.is_valid:
        #     return Response({'data':serializer.data},status=200)
        # return Response({'message':serializer.errors},status=400)