from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import IsAuthenticated
import random
from user_account.models import User
from student.models import Student
from parent.models import Parent
from .serializers import ChildActivityProgressSerializer
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateSudentUniqueID(request):
    name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    dob = request.POST.get("dob")
    image = request.FILES.get('image', None)
    if not image:
        pass
    if not name:
        return Response({"message": "Please provide first_name"}, status=400)
    if not last_name:
        return Response({"message": "Please provide last_name"}, status=400)
    if not dob:
        return Response({"message": "Please provide dob in format of YYYY-MM-DD"}, status=400)
    hash_name = generate_unique_id(name)
    child_creation = User.objects.create_user(
        email=hash_name,
        password=dob,
        first_name=name,
        last_name=last_name,
        image=image,
    )
    student = Student.objects.create(user=child_creation)
    student.dob = dob
    student.first_name = name
    student.image = image
    student.last_name = last_name
    student.user.is_verified = True
    student.user.save()
    student.save()
    parent = Parent.objects.get(user=request.user)
    parent.childrens.add(student)
    parent.save()
    return Response({"kid_unique_email": hash_name,"password":dob},status=201)
    
def generate_unique_id(name):
    first_name = name.split()[0].lower()
    random_number = random.randint(1, 1000)
    unique_id = f"{first_name}{random_number}@teaching.com"
    return unique_id


@api_view(['POST'])
def create_parent(request):
    data = request.data
    print(data['name'])
    # parents_data = User.objects.create_parent()
    return Response({"message":"Get data"})

#API for Parent know our children whose kid task is completed.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def parent_know_our_kid_task_status(request):
    parent_table = Parent.objects.get(user=request.user)
    student_table = []
    for child in parent_table.childrens.all():
        student = Student.objects.filter(user=child.user).first()
        if student:
            student_table.append(student)
    print("The Student Table is ====>", student_table)
    return Response({'message': 'success'}, status=200)

#Activity Progress for Parent.
class ActivityProgressForParent(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        result = []
        date_of_task = request.GET.get('date')
        if not date_of_task:
            return Response({"message": "Please provide date in format YYYY-MM-DD"}, status=400)
        date_of_task = datetime.strptime(date_of_task, '%Y-%m-%d').date()
        parent = Parent.objects.get(user=request.user)
        children_they_have = parent.childrens.all()
        for child in children_they_have:
            get_the_data_for_requested_child = Student.objects.filter(user=User.objects.get(email=child.user))
            print('The data is ===>', get_the_data_for_requested_child)
            serialized_data = ChildActivityProgressSerializer(get_the_data_for_requested_child, many=True).data
            result.append(serialized_data)
        return Response({'data': result}, status=200)
