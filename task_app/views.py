from rest_framework.response import Response
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from .models import Task, Assignment, Task_type, AgeGroup
from .serializers import TaskSerializer, TaskSerializerDate, TaskUpdateSerializer, ActivitySerializer
from rest_framework.decorators import api_view
from teacher.models import Teacher

#For Teacher and Student.
class ShowTaskBasedOnDateAndCategory(APIView):
    def get(self, request):
        teacher_id = request.GET.get('teacher_id')
        type_of_task_ids = request.GET.getlist('type_of_task_id')
        date = request.GET.get('date')
        if not teacher_id:
            return Response({"message": "Please provide teacher_id"}, status=status.HTTP_400_BAD_REQUEST)
        if not date:
            return Response({"message": "Please provide date in format YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        if not type_of_task_ids:
            return Response({"message": "Please provide type_of_task_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if type_of_task_ids and teacher_id and date:
                q_objects = Q()
                for task_id in type_of_task_ids:
                    q_objects |= Q(task=task_id)
                task_details = Task.objects.filter(
                    q_objects,
                    assigned_teacher=teacher_id,
                    date_of_posted=date
                )
                serializer = TaskSerializer(task_details, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        date = request.GET.get('date')
        if not date:
            return Response({"message":"Please Prodvide date in format of YYYY-MM-DD"})
        try:
            task_details_with_date = Task.objects.filter(date_of_posted__date=date)
            serializer = TaskSerializerDate(task_details_with_date,many=True)
            return Response({"date":serializer.data},status=200)
        except Exception as e:
            return Response({"message":serializer.errors,"error":str(e)},status=400)
    
@api_view(['POST'])
def create_task_type(request):
    task_type_name = request.POST.get('task_type',None)
    if not task_type_name : 
        return Response({"message":"Please provide task_type"}, status=status.HTTP_400_BAD_REQUEST)
    create, created = Task_type.objects.get_or_create(task_type=task_type_name)
    if created:
        return Response({"message":"Task Type Created Successfully"}, status=status.HTTP_200_OK)
    return Response({"message":"Task is already exists"}, status=400)

@api_view(['POST'])
def create_age_group(request):
    age_data = request.POST.get('age')
    if not age_data:
        return  Response({'message':'Age field can\'t be empty'},status=status.HTTP_400_BAD_REQUEST)
    create, created = AgeGroup.objects.get_or_create(age_group=age_data)
    if created:
        return Response({'message':'Age is created'})
    return Response({'message':'Age is already created'})

#Function for Update the Task
@api_view(['POST'])
def update_the_task(request):
    serializer = TaskUpdateSerializer(data=request.data)
    if serializer.is_valid():
        task_id = serializer.validated_data.get('task_id')
        age_group_name = serializer.validated_data.get('age_group')
        try:
            task = Task.objects.get(id=task_id)
            age_group = AgeGroup.objects.get(id=age_group_name)
            serializer.update(task, serializer.validated_data, age_group=age_group)
            return Response({"message": "Task is updated"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"message": "Task does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except AgeGroup.DoesNotExist:
            return Response({"message": "Age group does not exist"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowActivityProgressofTask(APIView):
    def get(self, request):
        get_the_date = request.GET.get('date', None)
        if not get_the_date:
            return Response({"message": "Please provide date in format YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        fetched_data_from_date_params = Task.objects.filter(date_of_posted=get_the_date)
        serializer = ActivitySerializer(fetched_data_from_date_params, many=True)
        if serializer.is_valid:
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)