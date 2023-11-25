from django.shortcuts import render

# Create your views here.
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .models import Nurse, Vaccine
# from .serializers import NurseSerializer, VaccineSerializer


from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import User  # Import your User model


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        #print(request)
        #print(request.body)
        # print(request.POST.items())
        # for key, value in request.POST.items():
        #     print(f'{key}: {value}')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('userType')

        query = """
            SELECT * FROM vaccine_user
            WHERE user_name = %s AND password = %s AND user_type = %s
        """
        cursor = connection.cursor()
        cursor.execute(query, [username, password, user_type])
        user_row = cursor.fetchone()
        print(user_row)

        # print(username, password, user_type)

        #user = authenticate(request, username=username, password=password, user_type= user_type)
        
        if user_row is not None:
            #login(request, user)
            return JsonResponse({'message': 'Login successful', 'user_type': user_type})
        else:
            return JsonResponse({'message': 'Incorrect password or user does not exist'}, status=401)
    else:
        return JsonResponse({'message': 'This endpoint only accepts POST requests'})


# views.py

# from rest_framework.generics import ListAPIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Nurse
# from .serializers import NurseSerializer

# @csrf_exempt
# class NurseListView(ListAPIView):
#     queryset = Nurse.objects.all()
#     serializer_class = NurseSerializer
#     # def get(self, request, *args, **kwargs):
#     #     nurses = Nurse.objects.all()
#     #     serializer = NurseSerializer(nurses, many=True)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Nurse
from .serializers import NurseSerializer

# @csrf_exempt
# def nurse_list(request):
#     #print("Got request")
#     if request.method == 'GET':
#         nurses = Nurse.objects.all()
#         serializer = NurseSerializer(nurses, many=True)
#         #print('Data before sending:', serializer.data)

#         return JsonResponse(serializer.data, safe=False)
#     else:
#         return JsonResponse({'message': 'Method not allowed'}, status=405)

from .serializers import CustomNurseSerializer, CustomPatientSerializer
@csrf_exempt
def nurse_list(request):
    if request.method == 'GET':
        # Write your custom SQL query
        query = "SELECT vaccine_nurse.id as id, vaccine_nurse.emp_id as emp_id, vaccine_user.name as name, vaccine_user.phone_number as phone_number,vaccine_user.address as address, vaccine_user.gender as gender FROM vaccine_nurse join vaccine_user ON vaccine_nurse.user_id = vaccine_user.id "
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            nurses_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        
        serializer = CustomNurseSerializer(data =nurses_data, many=True)
        print('Data before sending:', serializer.initial_data)
        
        #return JsonResponse(serializer.data, safe=False)
        if serializer.is_valid():
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'message': 'Serializer error'}, status=800)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def patient_list(request):
    if request.method == 'GET':
        query = '''
            SELECT vaccine_patient.id as id, vaccine_user.name as name, vaccine_user.age as age, vaccine_user.gender as gender,
            vaccine_patient.race as race, vaccine_patient.no_doses_received as prev_doses,
            vaccine_timeslot.timestamp as next_appointment
            FROM vaccine_patient JOIN vaccine_user ON vaccine_user.id = vaccine_patient.user_id 
            JOIN vaccine_appointment ON vaccine_appointment.patient_id = vaccine_patient.id
            JOIN vaccine_timeslot ON vaccine_appointment.timeslot_id = vaccine_timeslot.id
        '''
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            patients_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        serializer = CustomPatientSerializer(data=patients_data, many=True)
        
        if serializer.is_valid():
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'message': 'Serializer error'}, status=500)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Nurse

@csrf_exempt
def register_nurse(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        employee_id = request.POST.get('employee_id')
        age = request.POST.get('age')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        print([name, employee_id, age])

        # Check if user with the given employee_id already exists
        if Nurse.objects.filter(emp_id=employee_id).exists():
            return JsonResponse({'message': 'Cannot Register. User already exists'}, status=400)

        # Create a new user in the vaccine_user table
        user = User.objects.create(
            name=name,
            password="test",
            phone_number=phone_number,
            ssn="None",
            address=address,
            age=age,
            gender=gender,
            user_type="nurse",
            user_name=employee_id
        )

        # Create a new nurse in the vaccine_nurse table
        Nurse.objects.create(
            user=user,
            emp_id=employee_id
        )

        return JsonResponse({'message': 'Nurse registered successfully'}, status=201)

    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)





# @api_view(['POST'])
# def register_nurse_view(request):
#     if request.method == 'POST':
#         serializer = NurseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['PUT'])
# def update_nurse_info_view(request, nurse_id):
#     try:
#         nurse = Nurse.objects.get(id=nurse_id)
#     except Nurse.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = NurseSerializer(nurse, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# def delete_nurse_view(request, nurse_id):
#     try:
#         nurse = Nurse.objects.get(id=nurse_id)
#     except Nurse.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'DELETE':
#         nurse.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# # views.py in your app



# @api_view(['POST'])
# def add_vaccine_view(request):
#     if request.method == 'POST':
#         serializer = VaccineSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # views.py in your app

# @api_view(['PUT'])
# def update_vaccine_view(request, vaccine_id):
#     try:
#         vaccine = Vaccine.objects.get(id=vaccine_id)
#     except Vaccine.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = VaccineSerializer(vaccine, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # views.py in your app

# @api_view(['GET'])
# def view_nurse_info_view(request, nurse_id):
#     try:
#         nurse = Nurse.objects.get(id=nurse_id)
#     except Nurse.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = NurseSerializer(nurse)
#         return Response(serializer.data)
# # views.py in your app

# from .models import Patient
# from .serializers import PatientSerializer

# @api_view(['GET'])
# def view_patient_info_view(request, patient_id):
#     try:
#         patient = Patient.objects.get(id=patient_id)
#     except Patient.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = PatientSerializer(patient)
#         return Response(serializer.data)

    

