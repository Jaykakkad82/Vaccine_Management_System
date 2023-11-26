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
from django.utils import timezone


# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         #print(request)
#         #print(request.body)
#         # print(request.POST.items())
#         # for key, value in request.POST.items():
#         #     print(f'{key}: {value}')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user_type = request.POST.get('userType')

#         query = """
#             SELECT * FROM vaccine_user
#             WHERE user_name = %s AND password = %s AND user_type = %s
#         """
#         cursor = connection.cursor()
#         cursor.execute(query, [username, password, user_type])
#         user_row = cursor.fetchone()
#         print(user_row)

#         # print(username, password, user_type)

#         #user = authenticate(request, username=username, password=password, user_type= user_type)
        
#         if user_row is not None:
#             #login(request, user)
#             return JsonResponse({'message': 'Login successful', 'user_type': user_type})
#         else:
#             return JsonResponse({'message': 'Incorrect password or user does not exist'}, status=401)
#     else:
#         return JsonResponse({'message': 'This endpoint only accepts POST requests'})

# #Assuming username and password are not being updated. So, name, ssn, age, gender would be the updated details. 
# #Information needed: nurse_id, user_id, 
# # def update_nurse_admin(request):
# #     pass
# @csrf_exempt
# def delete_nurse(request):
#     if request.POST:
#         user_row = -1
#         # user_type = User.objects.get(id = request.POST['user_id'])
#         # user_type = user_type.user_type
#         if user_type[0]=="Admin":
#             query2 = """
#             DELETE FROM vaccine_nurse WHERE id = %s
#             """
#             cursor = connection.cursor()
#             cursor.execute(query2, [request.POST['nurse_id'],])
#             user_row = cursor.rowcount

#         if user_row>0:
#             return JsonResponse({'message': 'Nurse Details deleted successfully.', 'user_type': user_type})
#         elif user_row==0:
#             return JsonResponse({'message': 'No record found.', status=401})
#         else:
#             return JsonResponse({'message': 'User doesn\'t have access.', status=401})
#     else:
#         return JsonResponse({'message': 'This endpoint only accepts POST requests'})
            
# #Assumption: Each dose of a vaccine is considered a different vaccine altogether. So, we can have names as Pfizer - Dose 1, Pfizer - Dose 2
# #So, name of vaccine: Pfizer, number_of_dose: 1/2, this way, easier to filter.
# #Assuming that no vaccines are initially on hold.
# #Information needed: name, dose_number, description, total_count, user_id
# @csrf_exempt
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
#             INSERT INTO vaccine_vaccine VALUES(%s, %s, %s, %s, %s)
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
# @csrf_exempt
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
#             UPDATE vaccine_vaccine SET total_availability=%s WHERE id=%s AND on_hold<%s
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


#Address and Phone Number update from Nurse. 
#Information needed: user_id, user_type, phone_number, address
#If either phone number or address is unchanged, send the original value.

#ACCESSED BY NURSE
@csrf_exempt
def update_nurse_info(request, user_type, user_id):
    if request.method=='PUT':
        # query1 = """
        # SELECT user_type FROM vaccine_user WHERE id = %s
        # """
        # cursor = connection.cursor()
        # cursor.execute(query1, [request.POST['user_id'],])
        # user_type = cursor.fetchone()
        user_row = -1
        # user_type = User.objects.get(id = request.POST['user_id'])
        # user_type = user_type.user_type
        if user_type=="Nurse":
            query2 = """
            UPDATE vaccine_nurse SET phone_number=%s, address=%s WHERE id=%s
            """
            updated_details = json.loads(request.body.decode('utf-8'))['updatedDetails']
            cursor = connection.cursor()
            cursor.execute(query2, [updated_details['phone_number'], updated_details['address'], user_id])
            user_row = cursor.rowcount
        if user_row>0:
            return JsonResponse({'message': 'Nurse Details updated successfully.', 'user_type': user_type})
        elif user_row==0:
            return JsonResponse({'message': 'No record found.', status=401})
        else:
            return JsonResponse({'message': 'User doesn\'t have access.', status=401})
    elif request.method=='POST':
        query = """
        SELECT phone_number, address FROM vaccine_user WHERE vaccine_user.id=%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            nurse_data = cursor.fetchone()
        if not nurse_data:
            return JsonResponse({'message': 'Nurse ID does not exist'}, status=404)
        response_data = dict(zip(columns, nurse_data))
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

#Information needed: user_id, timestamp, user_type
@csrf_exempt
def schedule_nurse_slot(request, user_type, user_id):
    if request.method=='PUT':
        user_row = -1
        updated_details = json.loads(request.body.decode('utf-8'))['updatedDetails']
        if user_type=="Nurse":
            query1 = """
                SELECT id, open_slots FROM vaccine_timeslot
                WHERE timestamp = %s
            """
            cursor = connection.cursor()
            cursor.execute(query1, [updated_details['timestamp'],])
            user_row = cursor.fetchone()
            if user_row:
                # query2 = """
                # SELECT COUNT(*) FROM Assigned WHERE timeslot = %s GROUP BY timeslot
                # """
                # cursor = connection.cursor()
                # cursor.execute(query2, [user_row[0], ])
                # count_row = cursor.fetchone()
                # if count_row[0]<12:
                query2 = """
                INSERT INTO vaccine_assigned VALUES(%s, %s)
                """
                cursor = connection.cursor()
                cursor.execute(query2, [user_row[0], user_id])
                query3 = """
                UPDATE vaccine_timeslot SET open_slots=%s WHERE id=%s
                """
                cursor = connection.cursor()
                cursor.execute(query3, [min(100, user_row[1]+10), user_row[0]])
                if cursor.rowcount>0:
                    return JsonResponse({'message': 'Slot scheduled successfully.', 'user_type': user_type})
                else:
                    return JsonResponse({'message': 'Unable to schedule the slot.', status=401})
            else:
                query2 = """
                INSERT INTO vaccine_timeslot VALUES(%s, %s)
                """
                cursor = connection.cursor()
                cursor.execute(query2, [updated_details['timestamp'], 10])
                timeid = cursor.lastrowid
                query3 = """
                INSERT INTO vaccine_assigned VALUES(%s, %s)
                """
                cursor.execute(query3, [timeid, updated_details['user_id']])
                if cursor.rowcount>0:
                    return JsonResponse({'message': 'Slot scheduled successfully.', 'user_type': user_type})
                else:
                    return JsonResponse({'message': 'Unable to schedule the slot.', status=401})
        else:
            return JsonResponse({'message': 'User doesn\'t have access.', status=401})
    elif request.method=='POST':
        if user_type!="Nurse":
            return JsonResponse({'message': 'User doesn\'t have access.', status=401})
        timezone.activate('CDT')
        today = timezone.now().date()
        timezone.deactivate()
        query = """
        SELECT HOUR(A.timestamp) AS timestamp FROM vaccine_timeslot A JOIN vaccine_assigned B ON A.id = B.timeslot WHERE DATE(A.timestamp)=%s GROUP BY A.id HAVING COUNT(DISTINCT B.nurse)<12
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [today,])
            columns = [col[0] for col in cursor.description]
            nurse_data = cursor.fetchall()
        if not nurse_data:
            return JsonResponse({'message': 'Nurse ID does not exist'}, status=404)
        response_data = dict(zip(columns, *nurse_data))
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

#Information needed: timestamp, user_id, user_type
@csrf_exempt
def cancel_slot(request, user_id, user_type):
    if user_type!="Nurse":
        return JsonResponse({'message': 'User doesn\'t have access.', status=401})
    if request.method=="POST":
        timezone.activate('CDT')
        today = timezone.now()
        timezone.deactivate()
        query = """
        SELECT A.timestamp AS timestamp FROM vaccine_timeslot A JOIN vaccine_assigned B ON A.id = B.timeslot JOIN vaccine_nurse C ON B.nurse = C.id WHERE C.id = %s AND A.timestamp>%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id, today])
            columns = [col[0] for col in cursor.description]
            nurse_data = cursor.fetchall()
        if not nurse_data:
            return JsonResponse({'message': 'Nurse ID does not exist'}, status=404)
        response_data = dict(zip(columns, *nurse_data))
        return JsonResponse(response_data, safe=False)
    elif request.method=="PUT":
        user_row = -1
        updated_details = json.loads(request.body.decode('utf-8'))['updatedDetails']
        timezone.activate('CDT')
        today = timezone.now()
        timezone.deactivate()
        query1 = """
        SELECT COUNT(DISTINCT nurse) FROM vaccine_assigned A JOIN vaccine_timeslot B ON A.timeslot=B.id  WHERE B.timestamp=%s GROUP BY timeslot
        """
        query2 = """
        DELETE FROM vaccine_assigned WHERE nurse=%s AND timeslot IN (SELECT A.id FROM vaccine_timeslot A JOIN vaccine_assigned B ON A.id = B.timeslot WHERE A.timestamp=%s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query1, [updated_details['timeslot']])
            nurse_count = cursor.fetchone()[0]
            cursor.execute(query2, [user_id, updated_details['timeslot']])
            user_row = cursor.rowcount
            if user_row==0:
                return JsonResponse({'message': 'No record found.', status=401})
            elif user_row<0:
                return JsonResponse({'message': 'User doesn\'t have access.', status=401})
            else:
                message = 'Slot cancelled successfully.'
            if nurse_count<2:
                cursor.execute("""DELETE FROM vaccine_timeslot WHERE timestamp=%s""", [updated_details['timestamp']])
                return JsonResponse({'message': message, 'user_type': user_type})
            else:
                cursor.execute("""UPDATE vaccine_timeslot SET open_slots=LEAST(100, open_slots-10) WHERE timestamp=%s""", [updated_details['timestamp']])
                return JsonResponse({'message': message, 'user_type': user_type})
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

#Information Needed: appt_id, user_id, user_type
#We can do it this way: Once patient has scheduled an appt, they get the appt id. They can share it with the nurse. 
#So, similar to adding nurse id in admin module, the nurse will simply enter the appt id to create a record.
#Hence, only a put request considered.
@csrf_exempt
def record_appt(request, user_id, user_type):
    if user_type!="Nurse":
        return JsonResponse({'message': 'User doesn\'t have access.', status=401})
    if request.method=="PUT":
        updated_details = json.loads(request.body.decode('utf-8'))['updatedDetails']
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO vaccine_record VALUES(%s, %s)""", [updated_details['appt_id'], user_id])
            cursor.execute("""UPDATE vaccine_vaccine SET total_availability=total_availability-1, on_hold=on_hold-1 WHERE id IN (SELECT vaccine FROM vaccine_appointment WHERE id=%s)""", [updated_details['appt_id']])
            cursor.execute("""UPDATE vaccine_patient SET no_doses_received=(SELECT vaccine_dose FROM vaccine_appointment WHERE id=%s) WHERE id=(SELECT patient FROM vaccine_appointment where id=%s)""", [updated_details['appt_id'], updated_details['appt_id']])
            return JsonResponse({'message': "Record added successfully.", 'user_type': user_type})
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT requests'})        

#Information Needed: all user, patient fields
#Information that can't be modified/registered: user_type, no_doses_received
@csrf_exempt
def patient_update_info(request, user_id, user_type):
    if user_type!="Patient":
        return JsonResponse({'message': 'User doesn\'t have access.', status=401})
    if request.method=="POST":
        query = """
        SELECT A.name as name, A.password as password, A.phone_number as phone_number, A.ssn as ssn, A.address as address, A.age as age, 
        A.gender as gender, A.user_name as user_name, B.race as race, B.occupation as occupation, B.medical_history as medical_history 
        FROM vaccine_user A JOIN vaccine_patient B ON A.id = B.user WHERE vaccine_user.id={user_id}
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            patient_data = cursor.fetchone()
        if not patient_data:
            return JsonResponse({'message': 'Patient does not exist.'}, status=404)
        response_data = dict(zip(columns, nurse_data))
        return JsonResponse(response_data, safe=False)
    elif request.method=="PUT":
        user_row = -1
        updated_details = json.loads(request.body.decode('utf-8'))['updatedDetails']
        name = updated_details['name']
        pswd = updated_details['password']
        phnum = updated_details['phone_number']
        ssn = updated_details['ssn']
        addr = updated_details['address']
        age = updated_details['age']
        gen = updated_details['gender']
        uname = updated_details['user_name']
        race = updated_details['race']
        job = updated_details['occupation']
        med_det = updated_details['medical_history']
        query = """
        UPDATE vaccine_user SET name=%s, password=%s, phone_number=%s, ssn=%s, address=%s, age=%s, gender=%s, 
        user_name=%s WHERE id=%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [name, pswd, phnum, ssn, addr, age, gen, uname, user_id])
            cursor.execute("""UPDATE vaccine_patient SET race=%s, occupation=%s, medical_history=%s WHERE user=%s""", [race, job, med_det, user_id])
            return JsonResponse({'message': 'Patient Details updated successfully.', 'user_type': user_type})
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

 


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

    

