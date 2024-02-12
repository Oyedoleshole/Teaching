from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from user_account.models import User
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer, TaskCreationforAdminSerializer
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
        if not email and not mobiles:
            return Response({'message': 'Either email or mobile must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        user = None
        if email:
            user = authenticate(request,email=email, password=password)
            print("User is authenticate",user)
        elif mobiles:
            user = authenticate(request,mobile=mobiles, password=password)
            print("User is authenticate with his mobile",user)
        if user is None:
            return Response({'message': 'Either Email or Password is incorrect or the user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            exist_user = User.objects.get(email=user.email)
            if exist_user.is_verified is False:
                return Response({"message": "Please verify first"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        refresh = RefreshToken.for_user(user)
        return Response({'message': "Login successfully", 'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        print("The Id is =====>",id)
        user = User.objects.get(id=id)
        user.delete()
        return Response({"message":"Account deleted successfully"},status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)


