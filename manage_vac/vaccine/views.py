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

#Assuming username and password are not being updated. So, name, ssn, age, gender would be the updated details. 
#Information needed: nurse_id, user_id, 
# def update_nurse_admin(request):
#     pass

#Nurse ID
#User ID
def delete_nurse(request):
    if request.POST:
        user_row = -1
        # user_type = User.objects.get(id = request.POST['user_id'])
        # user_type = user_type.user_type
        if user_type[0]=="Admin":
            query2 = """
            DELETE FROM nurse WHERE id = %s
            """
            cursor = connection.cursor()
            cursor.execute(query2, [request.POST['nurse_id'],])
            user_row = cursor.rowcount

        if user_row>0:
            return JsonResponse({'message': 'Nurse Details deleted successfully.', 'user_type': user_type})
        elif user_row==0:
            return JsonResponse({'message': 'No record found.', status=401})
        else:
            return JsonResponse({'message': 'User doesn\'t have access.', status=401})
    else:
        return JsonResponse({'message': 'This endpoint only accepts POST requests'})
            
#Assumption: Each dose of a vaccine is considered a different vaccine altogether. So, we can have names as Pfizer - Dose 1, Pfizer - Dose 2
#So, name of vaccine: Pfizer, number_of_dose: 1/2, this way, easier to filter.
#Assuming that no vaccines are initially on hold.
#Information needed: name, dose_number, description, total_count, user_id
def add_vaccine(request):
    if request.POST:
        query1 = """
        SELECT user_type FROM vaccine_user WHERE id = %s
        """
        cursor = connection.cursor()
        cursor.execute(query1, [request.POST['user_id'],])
        user_type = cursor.fetchone()
        user_row = -1
        # user_type = User.objects.get(id = request.POST['user_id'])
        # user_type = user_type.user_type
        if user_type[0]=="Admin":
            query2 = """
            INSERT INTO vaccine VALUES(%s, %s, %s, %s, %s)
            """
            cursor = connection.cursor()
            cursor.execute(query2, [request.POST['name'], request.POST['dose_number'], 0, request.POST['description'], request.POST['total_count']])
            user_row = cursor.rowcount

        if user_row>0:
            return JsonResponse({'message': 'Vaccine Details added successfully.', 'user_type': user_type})
        elif user_row==0:
            return JsonResponse({'message': 'No record found.', status=401})
        else:
            return JsonResponse({'message': 'User doesn\'t have access.', status=401})
    else:
        return JsonResponse({'message': 'This endpoint only accepts POST requests'})


#This method only updates the total availability count of the vaccine (provided it doesn't affect the on-hold vaccines),
#since the project requirements documentation only mentions the same requirement under 'Update Vaccine'.
#Information needed: vaccine_id, new_total_count, user_id
def update_vaccine(request):
    if request.POST:
        query1 = """
        SELECT user_type FROM vaccine_user WHERE id = %s
        """
        cursor = connection.cursor()
        cursor.execute(query1, [request.POST['user_id'],])
        user_type = cursor.fetchone()
        user_row = -1
        # user_type = User.objects.get(id = request.POST['user_id'])
        # user_type = user_type.user_type
        if user_type[0]=="Admin":
            query2 = """
            UPDATE vaccine SET total_availability=%s WHERE id=%s AND on_hold<%s
            """
            cursor = connection.cursor()
            cursor.execute(query2, [request.POST['new_total_count'], request.POST['vaccine_id'],request.POST['new_total_count']])
            user_row = cursor.rowcount
        if user_row>0:
            return JsonResponse({'message': 'Vaccine Details updated successfully.', 'user_type': user_type})
        elif user_row==0:
            return JsonResponse({'message': 'No record found.', status=401})
        else:
            return JsonResponse({'message': 'User doesn\'t have access.', status=401})
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

    

