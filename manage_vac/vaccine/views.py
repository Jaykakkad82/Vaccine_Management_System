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


# #Address and Phone Number update from Nurse. 
# #Information needed: user_id, user_type, phone_number, address
# #If either phone number or address is unchanged, send the original value.

# #ACCESSED BY NURSE
# @csrf_exempt
# def update_nurse_info(request, user_type, user_id):
#     if request.method=='PUT':
#         # query1 = """
#         # SELECT user_type FROM vaccine_user WHERE id = %s
#         # """
#         # cursor = connection.cursor()
#         # cursor.execute(query1, [request.POST['user_id'],])
#         # user_type = cursor.fetchone()
#         user_row = -1
#         # user_type = User.objects.get(id = request.POST['user_id'])
#         # user_type = user_type.user_type
#         if user_type=="Nurse":
#             query2 = """
#             UPDATE vaccine_user SET phone_number=%s, address=%s WHERE id=%s
#             """
#             phone_number = request.POST.get('phone_number')
#             address = request.POST.get('address')
#             cursor = connection.cursor()
#             cursor.execute(query2, [phone_number, address, user_id])
#             user_row = cursor.rowcount
#         if user_row>0:
#             return JsonResponse({'message': 'Nurse Details updated successfully.', 'user_type': user_type})
#         elif user_row==0:
#             return JsonResponse({'message': 'No record found.'}, status=401)
#         else:
#             return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
#     elif request.method=='POST':
#         query = """
#         SELECT phone_number, address FROM vaccine_user WHERE vaccine_user.id=%s
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             columns = [col[0] for col in cursor.description]
#             nurse_data = cursor.fetchone()
#         if not nurse_data:
#             return JsonResponse({'message': 'Nurse ID does not exist'}, status=404)
#         response_data = dict(zip(columns, nurse_data))
#         return JsonResponse(response_data, safe=False)
#     else:
#         return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

#Information needed: user_id, timestamp, user_type
@csrf_exempt
def schedule_nurse_slot(request, user_type, user_id):
    if request.method=='PUT':
        user_row = -1
        timestamp = request.POST.get('timestamp')
        if user_type=="Nurse":
            query1 = """
                SELECT id, open_slots FROM vaccine_timeslot
                WHERE timestamp = %s
            """
            cursor = connection.cursor()
            cursor.execute(query1, [timestamp,])
            user_row = cursor.fetchone()
            if user_row:
                # query2 = """
                # SELECT COUNT(*) FROM Assigned WHERE timeslot = %s GROUP BY timeslot
                # """
                # cursor = connection.cursor()
                # cursor.execute(query2, [user_row[0], ])
                # count_row = cursor.fetchone()
                # if count_row[0]<12:
                nurse_id = Nurse.objects.get(user__id = user_id)
                nurse_id = nurse_id.id
                query2 = """
                INSERT INTO vaccine_assigned VALUES(%s, %s)
                """
                cursor = connection.cursor()
                cursor.execute(query2, [user_row[0], nurse_id])
                query3 = """
                UPDATE vaccine_timeslot SET open_slots=%s WHERE id=%s
                """
                cursor = connection.cursor()
                cursor.execute(query3, [min(100, user_row[1]+10), user_row[0]])
                if cursor.rowcount>0:
                    return JsonResponse({'message': 'Slot scheduled successfully.', 'user_type': user_type})
                else:
                    return JsonResponse({'message': 'Unable to schedule the slot.'}, status=401)
            else:
                nurse_id = Nurse.objects.get(user__id = user_id)
                nurse_id = nurse_id.id
                query2 = """
                INSERT INTO vaccine_timeslot VALUES(%s, %s)
                """
                cursor = connection.cursor()
                cursor.execute(query2, [timestamp, 10])
                timeid = cursor.lastrowid
                query3 = """
                INSERT INTO vaccine_assigned VALUES(%s, %s)
                """
                cursor.execute(query3, [timeid, nurse_id])
                if cursor.rowcount>0:
                    return JsonResponse({'message': 'Slot scheduled successfully.', 'user_type': user_type})
                else:
                    return JsonResponse({'message': 'Unable to schedule the slot.'}, status=401)
        else:
            return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    elif request.method=='POST':
        if user_type!="Nurse":
            return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
        timezone.activate('CDT')
        today = timezone.now().date() + 1
        timezone.deactivate()
        query = """
        SELECT A.timestamp AS timestamp FROM vaccine_timeslot A JOIN vaccine_assigned B ON A.id = B.timeslot WHERE DATE(A.timestamp)=%s GROUP BY A.id HAVING COUNT(DISTINCT B.nurse)<12
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [today,])
            columns = [col[0] for col in cursor.description]
            nurse_data = cursor.fetchall()
        if not nurse_data:
            return JsonResponse({'message': 'Nurse ID does not exist'}, status=404)
        response_data = tuple(zip(columns, *nurse_data))
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

#Information needed: timestamp, user_id, user_type
@csrf_exempt
def cancel_slot(request, user_id, user_type):
    if user_type!="Nurse":
        return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    if request.method=="POST":
        timezone.activate('CDT')
        today = timezone.now()
        timezone.deactivate()
        nurse_id = Nurse.objects.get(user__id = user_id)
        nurse_id = nurse_id.id
        query = """
        SELECT A.timestamp AS timestamp FROM vaccine_timeslot A JOIN vaccine_assigned B ON A.id = B.timeslot JOIN vaccine_nurse C ON B.nurse = C.id WHERE C.id = %s AND A.timestamp>%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [nurse_id, today])
            columns = [col[0] for col in cursor.description]
            nurse_data = cursor.fetchall()
        if not nurse_data:
            return JsonResponse({'message': 'Nurse ID does not exist'}, status=404)
        response_data = tuple(zip(columns, *nurse_data))
        return JsonResponse(response_data, safe=False)
    elif request.method=="PUT":
        user_row = -1
        timestamp = request.POST.get('timestamp')
        timezone.activate('CDT')
        today = timezone.now()
        timezone.deactivate()
        nurse_id = Nurse.objects.get(user__id = user_id)
        nurse_id = nurse_id.id
        query1 = """
        SELECT COUNT(DISTINCT nurse) FROM vaccine_assigned A JOIN vaccine_timeslot B ON A.timeslot=B.id  WHERE B.timestamp=%s GROUP BY timeslot
        """
        query2 = """
        DELETE FROM vaccine_assigned WHERE nurse=%s AND timeslot IN (SELECT A.id FROM vaccine_timeslot A JOIN vaccine_assigned B ON A.id = B.timeslot WHERE A.timestamp=%s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query1, [timestamp])
            nurse_count = cursor.fetchone()[0]
            cursor.execute(query2, [nurse_id, timestamp])
            user_row = cursor.rowcount
            if user_row==0:
                return JsonResponse({'message': 'No record found.'}, status=401)
            elif user_row<0:
                return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
            else:
                message = 'Slot cancelled successfully.'
            if nurse_count<2:
                cursor.execute("""DELETE FROM vaccine_timeslot WHERE timestamp=%s""", [timestamp])
                return JsonResponse({'message': message, 'user_type': user_type})
            else:
                cursor.execute("""UPDATE vaccine_timeslot SET open_slots=LEAST(100, open_slots-10) WHERE timestamp=%s""", [timestamp])
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
        return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    if request.method=="PUT":
        nurse_id = Nurse.objects.get(user__id = user_id)
        nurse_id = nurse_id.id
        appt_id = request.POST.get('appt_id')
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO vaccine_record VALUES(%s, %s)""", [appt_id, nurse_id])
            cursor.execute("""UPDATE vaccine_vaccine SET total_availability=total_availability-1, on_hold=on_hold-1 WHERE id IN (SELECT vaccine FROM vaccine_appointment WHERE id=%s)""", [appt_id])
            cursor.execute("""UPDATE vaccine_patient SET no_doses_received=(SELECT vaccine_dose FROM vaccine_appointment WHERE id=%s) WHERE id=(SELECT patient FROM vaccine_appointment where id=%s)""", [appt_id, appt_id])
            return JsonResponse({'message': "Record added successfully.", 'user_type': user_type})
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT requests'})        

#Information Needed: all user, patient fields
#Information that can't be modified/registered: user_type, no_doses_received
@csrf_exempt
def patient_update_info(request, user_id, user_type):
    if user_type!="Patient":
        return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    if request.method=="POST":
        query = """
        SELECT A.name as name, A.password as password, A.phone_number as phone_number, A.ssn as ssn, A.address as address, A.age as age, 
        A.gender as gender, A.user_name as user_name, B.race as race, B.occupation as occupation, B.medical_history as medical_history 
        FROM vaccine_user A JOIN vaccine_patient B ON A.id = B.user WHERE A.id=%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            columns = [col[0] for col in cursor.description]
            patient_data = cursor.fetchone()
        if not patient_data:
            return JsonResponse({'message': 'Patient does not exist.'}, status=404)
        response_data = dict(zip(columns, patient_data))
        return JsonResponse(response_data, safe=False)
    elif request.method=="PUT":
        user_row = -1
        
        name = request.POST.get('name')
        pswd = request.POST.get('password')
        phnum = request.POST.get('phone_number')
        ssn = request.POST.get('ssn')
        addr = request.POST.get('address')
        age = request.POST.get('age')
        gen = request.POST.get('gender')
        uname = request.POST.get('user_name')
        race = request.POST.get('race')
        job = request.POST.get('occupation')
        med_det = request.POST.get('medical_history')
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

 
@csrf_exempt
def register_patient(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        age = request.POST.get('age')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        ssn = request.POST.get('ssn')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        race = request.POST.get('race')
        job = request.POST.get('occupation')
        med_det = request.POST.get('medical_history')
        #print([name, employee_id, age])

        # Check if user with the given employee_id already exists
        if Patient.objects.filter(user__user_name=user_name).exists():
            return JsonResponse({'message': 'Cannot Register. User with this username already exists'}, status=400)

        # Create a new user in the vaccine_user table
        # user = User.objects.create(
        #     name=name,
        #     password=password,
        #     phone_number=phone_number,
        #     address=address,
        #     ssn = snn,
        #     age=age,
        #     gender=gender,
        #     user_type="Patient",
        #     user_name=user_name
        # )
        query = """
        INSERT INTO vaccine_user VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [name, password, phone_number, ssn, address, age, gender, 'Patient', user_name])
            user = cursor.lastrowid
        # Create a new nurse in the vaccine_nurse table
        # Patient.objects.create(
        #     user=user,
        #     no_doses_received = 0,
        #     race = race,
        #     occupation = job,
        #     medical_history = med_det
        # )
        query = """
        INSERT INTO vaccine_patient VALUES(%s, %s, %s, %s, %s)
        """
         with connection.cursor() as cursor:
            cursor.execute(query, [user, 0, race, job, med_det])
            check = cursor.rowcount
        if check>0:
            return JsonResponse({'message': 'Patient registered successfully'}, status=201)
        else:
            return JsonResponse({'message': 'Error in Registration.'}, status=401)
    else:
        return JsonResponse({'message': 'HTTP Request other than POST encountered.'}, status=405)

#Information Needed (for POST): user_type, user_id
#Information Needed (for PUT): user_type, user_id, vaccine_id (or name, no_dose of vaccine), timestamp
@csrf_exempt
def patient_schedule_appt(request, user_id, user_type):
    if user_type!="Patient":
        return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    if request.method=="PUT":
        vaccine_id = request.POST.get('vaccine_id')
        timestamp = request.POST.get('timestamp')
        query = """
        INSERT INTO vaccine_appointment 
        VALUES((SELECT no_doses_free FROM vaccine_vaccine WHERE vaccine_id=%s), %s, %s, (SELECT id FROM vaccine_timeslot WHERE timestamp=%s))
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [vaccine_id, vaccine_id, timestamp])
            apptid = cursor.lastrowid
            cursor.execute("UPDATE vaccine_vaccine SET on_hold = on_hold+1")
            count = cursor.rowcount
            if count>0:
                message = 'Appointment registered with ID: '+str(apptid)
                return JsonResponse({'message': message, 'user_type': user_type, 'appt_id': apptid}, status=201)
            else:
                return JsonResponse({'message': 'Error in Registration.'}, status=401) 
    elif request.method=="POST":
        patient_id = Patient.objects.get(user__id = user_id)
        patient_id = patient_id.id
        query = """
        SELECT * FROM vaccine_patient WHERE id=%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [patient_id])
            patient = cursor.fetchone()
        if patient[1]==0:
            query2 = """
            SELECT id, vaccine_name FROM vaccine_vaccine WHERE no_doses_free=1 AND total_availability-on_hold>0
            """
            with connection.cursor() as cursor:
                cursor.execute(query2)
                columns = [col[0] for col in cursor.description] #name, number_doses_free, on_hold, description, total_availability
                #Change select * from query2 to individual column names if all columns not wanted.
                vaccine_data = cursor.fetchall()
            if not vaccine_data:
                return JsonResponse({'message': 'No Vaccines Available.'})
            vaccine_data = tuple(zip(columns, *vaccine_data))
            timezone.activate('CDT')
            appt_day = timezone.now().date() + 1
            timezone.deactivate()
            query3 = """
            SELECT timestamp FROM vaccine_timeslot WHERE open_slots>0 AND DATE(timestamp)=%s
            """
            with connection.cursor() as cursor:
                cursor.execute(query2, [appt_day])
                columns = [col[0] for col in cursor.description]
                schedule_data = cursor.fetchall()
            if not schedule_data:
                return JsonResponse({'message': 'No Appointments Available.'})
            schedule_data = tuple(zip(columns, *schedule_data))
            response_data = {"schedule_data": schedule_options, "vaccine_data": vaccine_data}
            return JsonResponse(response_data, safe=False)
        elif patient[1]>0:
            with connection.cursor() as cursor:
                
                temp_query = """
                SELECT * FROM vaccine_patient WHERE id=%s AND 
                no_doses_received<=(SELECT max(no_doses_free) FROM vaccine_vaccine WHERE 
                name=(SELECT name FROM vaccine_vaccine WHERE id=(SELECT vaccine FROM vaccine_appointment 
                WHERE patient=%s ORDER BY vaccine_dose DESC LIMIT 1)))
                """
                cursor.execute(temp_query, [patient_id, patient_id])
                vcheck = cursor.fetchall()
                if not vcheck:
                    return JsonResponse({'message': 'You\'ve been completely vaccinated.'})
            query2 = """
            SELECT id, vaccine_name FROM vaccine_vaccine WHERE total_availability-on_hold>0 AND id IN (SELECT vaccine FROM vaccine_appointment
            WHERE patient=%s ORDER BY vaccine_dose DESC LIMIT 1)
            """
            with connection.cursor() as cursor:
                cursor.execute(query2, [patient_id])
                columns = [col[0] for col in cursor.description]
                vaccine_data = cursor.fetchall()
            if not vaccine_data:
                return JsonResponse({'message': 'Vaccine Dose not Available.'}, status=404)
            vaccine_data = tuple(zip(columns, *vaccine_data))
            timezone.activate('CDT')
            appt_day = timezone.now().date() + 1
            timezone.deactivate()
            query3 = """
            SELECT timestamp FROM vaccine_timeslot WHERE open_slots>0 AND DATE(timestamp)=%s
            """
            with connection.cursor() as cursor:
                cursor.execute(query2, [appt_day])
                columns = [col[0] for col in cursor.description]
                schedule_data = cursor.fetchall()
            if not schedule_data:
                return JsonResponse({'message': 'No Appointments Available.'})
            schedule_data = tuple(zip(columns, *schedule_data))
            response_data = {"schedule_data": schedule_options, "vaccine_data": vaccine_data}
            return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

#Information Needed: POST/PUT - appt_id, user_id, user_type
@csrf_exempt
def patient_cancel_appt(request, user_id, user_type): 
    patient_id = Patient.objects.get(user=user_id)
    apt = Appointment.objects.filter(id = appt_id, patient = patient_id).values(id, vaccine_dose, vaccine, vaccine__name, patient, patient__name, timeslot, timeslot__timestamp)   
    if user_type!="Patient" or not apt:
        return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    if request.method=="POST":
        appt_id = request.POST.get('appt_id')
        if apt:
            apt = dict(apt.first())
            response_data = {'appt_id': apt['id'], 'vaccine_id': apt['vaccine'], 'vaccine_name': apt['name'], 'patient_id': patient_id, 'patient_name': apt['patient__name'], 'timeslot_id': apt['timeslot'], 'timestamp': apt['timeslot__timestamp']}
            if response_data:
                return JsonResponse(response_data, safe=False)
        return JsonResponse({'message': 'Unable to fetch appointment.'}, status=401)
    elif request.method=="PUT":
        appt_id = request.POST.get('appt_id')
        apt = Appointment.objects.filter(id = appt_id).values(id, vaccine_dose, vaccine, vaccine__name, patient, patient__name, timeslot, timeslot__timestamp)
        if timezone.now()>apt.first()['timeslot__timestamp']:
            return JsonResponse({'message': 'The appointment is past deletion.'}, status=401)
        query = """
        DELETE FROM vaccine_appointment WHERE appt_id = %s
        """
        count = -1
        with connection.cursor() as cursor:
            cursor.execute(query, appt_id)
            cursor.execute("""UPDATE vaccine_vaccine SET on_hold = on_hold-1""")
            count = cursor.rowcount
            connection.commit()
        if count>0:
            return JsonResponse({'message': "Appointment deleted.", 'user_type': user_type, 'appt_id': apptid}, status=201)
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

    

