from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import IsAuthenticated
import random
from user_account.models import User
from student.models import Student
from parent.models import Parent

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateSudentUniqueID(request):
    data = request.data
    if not data:
        return Response({"message": "Please provide name"}, status=400)

    hash_name = generate_unique_id(data['name'])
    child_creation = User.objects.create_user(
        email=hash_name,
        password=data['name'],
        first_name=data['name'],
        last_name=data['name'],
    )
    student = Student.objects.create(user=child_creation)
    parent = Parent.objects.get(user=request.user)
    parent.childrens.add(student)
    parent.save()
    return Response({"The Hash id": hash_name})
    
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