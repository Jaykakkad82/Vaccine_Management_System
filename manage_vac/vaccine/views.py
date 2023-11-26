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
from .models import User, Nurse  # Import your User model


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
        user_id = user_row[-1]
        name = user_row[1]

        # print(username, password, user_type)

        #user = authenticate(request, username=username, password=password, user_type= user_type)
        
        if user_row is not None:
            #login(request, user)
            return JsonResponse({'message': 'Login successful', 'user_type': user_type, 'user_id': user_id, 'name': name})
        else:
            return JsonResponse({'message': 'Incorrect password or user does not exist'}, status=401)
    else:
        return JsonResponse({'message': 'This endpoint only accepts POST requests'})


# ======= COMMENTED OUT =====================#

# #Assuming username and password are not being updated. So, name, ssn, age, gender would be the updated details. 
# #Information needed: nurse_id, user_id, 
# # def update_nurse_admin(request):
# #     pass

# #Nurse ID
# #User ID
@csrf_exempt
def delete_nurse(request):
    if request.method == "POST":
        user_row = -1
        query2 = """ DELETE FROM vaccine_nurse WHERE id = %s  """
        nurse_id = request.POST.get('nurse_id')
        print(nurse_id)
        cursor = connection.cursor()
        cursor.execute(query2, [nurse_id])
        user_row = cursor.rowcount
        print("Nurse Deleted")

        if user_row>0:
            return JsonResponse({'message': 'Nurse Details deleted successfully.'})
        elif user_row==0:
            return JsonResponse({'message': 'No record found.'}, status=401)
        else:
            return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    else:
        return JsonResponse({'message': 'This endpoint only accepts POST requests'})
            
# #Assumption: Each dose of a vaccine is considered a different vaccine altogether. So, we can have names as Pfizer - Dose 1, Pfizer - Dose 2
# #So, name of vaccine: Pfizer, number_of_dose: 1/2, this way, easier to filter.
# #Assuming that no vaccines are initially on hold.
# #Information needed: name, dose_number, description, total_count, user_id
# def add_vaccine(request):
#     if request.POST:
#         query1 = """
#         SELECT user_type FROM vaccine_user WHERE id = %s
#         """
#         cursor = connection.cursor()
#         cursor.execute(query1, [request.POST['user_id'],])
#         user_type = cursor.fetchone()
#         user_row = -1
#         # user_type = User.objects.get(id = request.POST['user_id'])
#         # user_type = user_type.user_type
#         if user_type[0]=="Admin":
#             query2 = """
#             INSERT INTO vaccine VALUES(%s, %s, %s, %s, %s)
#             """
#             cursor = connection.cursor()
#             cursor.execute(query2, [request.POST['name'], request.POST['dose_number'], 0, request.POST['description'], request.POST['total_count']])
#             user_row = cursor.rowcount

#         if user_row>0:
#             return JsonResponse({'message': 'Vaccine Details added successfully.', 'user_type': user_type})
#         elif user_row==0:
#             return JsonResponse({'message': 'No record found.', status=401})
#         else:
#             return JsonResponse({'message': 'User doesn\'t have access.', status=401})
#     else:
#         return JsonResponse({'message': 'This endpoint only accepts POST requests'})



# #This method only updates the total availability count of the vaccine (provided it doesn't affect the on-hold vaccines),
# #since the project requirements documentation only mentions the same requirement under 'Update Vaccine'.
# #Information needed: vaccine_id, new_total_count, user_id
# def update_vaccine(request):
#     if request.POST:
#         query1 = """
#         SELECT user_type FROM vaccine_user WHERE id = %s
#         """
#         cursor = connection.cursor()
#         cursor.execute(query1, [request.POST['user_id'],])
#         user_type = cursor.fetchone()
#         user_row = -1
#         # user_type = User.objects.get(id = request.POST['user_id'])
#         # user_type = user_type.user_type
#         if user_type[0]=="Admin":
#             query2 = """
#             UPDATE vaccine SET total_availability=%s WHERE id=%s AND on_hold<%s
#             """
#             cursor = connection.cursor()
#             cursor.execute(query2, [request.POST['new_total_count'], request.POST['vaccine_id'],request.POST['new_total_count']])
#             user_row = cursor.rowcount
#         if user_row>0:
#             return JsonResponse({'message': 'Vaccine Details updated successfully.', 'user_type': user_type})
#         elif user_row==0:
#             return JsonResponse({'message': 'No record found.', status=401})
#         else:
#             return JsonResponse({'message': 'User doesn\'t have access.', status=401})
#     else:
#         return JsonResponse({'message': 'This endpoint only accepts POST requests'})


# ======================================== TILL THIS POINT =================================================================

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


from django.http import JsonResponse
from django.db import connection
import json


@csrf_exempt
def admin_update_nurse_details(request, nurse_id):
    if request.method == 'POST':
        # Check if nurseId exists
        query = f"SELECT * FROM vaccine_nurse JOIN vaccine_user ON vaccine_nurse.user_id = vaccine_user.id WHERE vaccine_nurse.id = {nurse_id}"

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            nurse_data = cursor.fetchone()
        print("Nurse data: ", nurse_data)
        if not nurse_data:
            return JsonResponse({'message': 'Nurse ID does not exist'}, status=404)

        # Return nurse data to frontend
        response_data = dict(zip(columns, nurse_data))
        return JsonResponse(response_data, safe=False)

    elif request.method == 'PUT':
        # Extract updated details from request body
        updated_details = json.loads(request.body.decode('utf-8'))
        
        updated_details = updated_details["updatedDetails"]
        print(updated_details)

        # Update vaccine_user and vaccine_nurse tables
        # Modify the update queries based on your model structure
        # user_update_query = f"UPDATE vaccine_user SET name = '{updated_details['name']}', age = {updated_details['age']}, gender = '{updated_details['gender']}' WHERE id = {nurse_id}"
        # nurse_update_query = f"UPDATE vaccine_nurse SET emp_id = '{updated_details['emp_id']}' WHERE id = {nurse_id}"
        user_update_query = f"UPDATE vaccine_user SET name = '{updated_details['name']}', age = {updated_details['age']}, gender = '{updated_details['gender']}', user_name = '{updated_details['user_name']}', password = '{updated_details['password']}' WHERE id = (SELECT user_id FROM vaccine_nurse WHERE id = {nurse_id})"

        with connection.cursor() as cursor:
            cursor.execute(user_update_query)
            #cursor.execute(nurse_update_query)

        return JsonResponse({'message': 'Information updated'}, status=200)

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

    

