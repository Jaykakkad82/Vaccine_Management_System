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

    

