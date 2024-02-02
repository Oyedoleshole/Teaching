from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .serializer import TeacherlistingSerializer, ShowStudentRelateToTeacher, TaskSerializer, TeacherSerializer, TaskRemarkSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import permission_classes
from student.models import Student
from task.models import Task
from rest_framework import generics, permissions
class TeacherList(APIView):
    def get(self, request):
        data = Teacher.objects.all()
        print("The data is ====>",data)
        serializer = TeacherlistingSerializer(data, many=True)
        if serializer.is_valid:
            return JsonResponse({"data":serializer.data},status=status.HTTP_200_OK)
        return JsonResponse({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def show_student_relate_to_teacher_(request):
    teacher_id = request.data.get('teacher_id')
    if not teacher_id:
        return JsonResponse({"message": "Please provide teacher_id"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        students = teacher.students.all()
        serializer = ShowStudentRelateToTeacher(students, many=True)
        serialized_data = serializer.data
        return JsonResponse({"data": serialized_data})
    except Teacher.DoesNotExist:
        return JsonResponse({"message": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

class task_assign_to_student_by_teacher(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        task_id = request.GET.get('task_id')
        if not task_id:
            return JsonResponse({"message":"Please provide task_id"},status=400)
        student_listing = Teacher.objects.get(user=request.user)
        students_are = student_listing.students.all()
        student_ID_list = []
        students_name_list = []
        for values in students_are:
            student_ID = values.id
            students_name = f"{values.user.first_name} {values.user.last_name}"
            student_ID_list.append(student_ID)
            students_name_list.append(students_name)
        try:
            task_details = Task.objects.get(id=task_id, assigned_teacher=student_listing)
        except Task.DoesNotExist:
            task_details = False
            return JsonResponse({"message":"Task is not exists or not assign to requested teacher"}, status=400)
        task_ids = task_details.id
        task_name = task_details.name
        task_details_ = task_details.description
        submission_date = task_details.submission_date
        return JsonResponse({"teacher":student_listing.user.email,"task_id":task_ids,"task_name":task_name,"task_details":task_details_,"submission_date":submission_date,"student_id":student_ID_list,"students_name":students_name_list},status=200)

    def post(self, request):
        task_id = request.POST.get('task_id')
        student_id = request.POST.get('student_id')
        if not task_id:
            return JsonResponse({"message": "Please provide task_id"}, status=400)
        if not student_id:
            return JsonResponse({"message": "Please provide student_id"}, status=400)
        try:
            teacher = Teacher.objects.get(user=request.user)
            task = Task.objects.get(id=task_id)
        except Teacher.DoesNotExist:
            return JsonResponse({"message": "Teacher not found"}, status=400)
        except Task.DoesNotExist:
            return JsonResponse({"message": "Task not found"}, status=400)
        try:
            get_the_student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return JsonResponse({"message":"Student not found"},status=400)
        task.assigned_student.add(get_the_student)
        return JsonResponse({"message": "Task assigned successfully"},status=200)

#This is not in use.
class TaskAssignToStudentByTeacher(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TeacherSerializer
        elif self.request.method == 'POST':
            return TaskSerializer

    def get_queryset(self):
        return Teacher.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        task_id = request.data.get('task_id')
        student_id = request.data.get('student_id')
        if not task_id or not student_id:
            return Response({"message": "Please provide both task_id and student_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            teacher = self.get_object()
            task = Task.objects.get(id=task_id)
            student = Student.objects.get(id=student_id)
        except (Task.DoesNotExist, Student.DoesNotExist):
            return Response({"message": "Task or Student not found"}, status=status.HTTP_404_NOT_FOUND)
        task.assigned_student.add(student)
        return Response({"message": "Task assigned successfully"}, status=status.HTTP_200_OK)

class TeacherRemarkAfterPostedTaskForStudent(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = TaskRemarkSerializer(data=request.data)
        if serializer.is_valid():
            task_id = serializer.validated_data['task_id']
            tutor_remark = serializer.validated_data['tutor_remark']
            try:
                fetch_task = Task.objects.get(id=task_id)
                image_or_file = request.FILES.get('image_or_file')
                fetch_task.task_image_for_hint = image_or_file
                fetch_task.tutor_remark = tutor_remark
                fetch_task.save()
                return Response({"message": "Task has some remarks, and the file is uploaded successfully"}, status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({"message": "Task not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)