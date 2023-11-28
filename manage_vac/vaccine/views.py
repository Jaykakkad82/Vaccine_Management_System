
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import timedelta
from django.http.multipartparser import MultiPartParser
from django.http import QueryDict
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import User, Nurse, Patient, Vaccine, Timeslot, Appointment, Record, Assigned  # Import your User model
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Nurse

# ====================================== LOGIN View ============================================================================
#================================================================================================================================
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
        user_id = user_row[0]
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



@csrf_exempt
def register_patient(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        age = request.POST.get('age')
        phone_number = request.POST.get('phoneNumber')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        ssn = request.POST.get('ssn')
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        race = request.POST.get('race')
        job = request.POST.get('occupation')
        med_det = request.POST.get('medicalHistory')
        #print([name, employee_id, age])

        # Check if user with the given employee_id already exists
        if Patient.objects.filter(user__user_name=user_name).exists():
            return JsonResponse({'message': 'Cannot Register. User with this username already exists'}, status=400)

        query = """
        INSERT INTO vaccine_user (name, password,phone_number, ssn, address, age, gender, user_type, user_name)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [name, password, phone_number, ssn, address, age, gender, 'Patient', user_name])
            user = cursor.lastrowid
        # Create a new nurse in the vaccine_nurse table
      
        query = """
        INSERT INTO vaccine_patient (no_doses_received, race, occupation, medical_history, user_id)
        VALUES(%s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [ 0, race, job, med_det, user])
            check = cursor.rowcount
        if check>0:
            return JsonResponse({'message': 'Patient registered successfully'}, status=201)
        else:
            return JsonResponse({'message': 'Error in Registration.'}, status=401)
    else:
        return JsonResponse({'message': 'HTTP Request other than POST encountered.'}, status=405)


# ======= =======================Admin Dashboard =============================================#
# =============================================================================================
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
# #Information needed: name, dose_number, description, count, user_id
@csrf_exempt
def add_vaccine(request):
    if request.method == "POST":
        query1 = """
        SELECT user_type FROM vaccine_user WHERE id = %s
        """
        cursor = connection.cursor()
        cursor.execute(query1, [request.POST['user_id']])
        user_type = cursor.fetchone()
        user_row = -1
        # user_type = User.objects.get(id = request.POST['user_id'])
        # user_type = user_type.user_type
        print("user type is: ", user_type)
        if user_type[0]=="Admin":
            query2 = """
            INSERT INTO vaccine_vaccine (name, number_doses_free, on_hold, description, total_availability)
            VALUES(%s, %s, %s, %s, %s)
            """
            cursor = connection.cursor()
            cursor.execute(query2, [request.POST['name'], request.POST['dose_number'], 0, request.POST['description'], request.POST['total_count']])
            user_row = cursor.rowcount

            if user_row>0:
                return JsonResponse({'message': 'Vaccine Details added successfully.', 'user_type': user_type})
            elif user_row==0:
                return JsonResponse({'message': 'could not add'}, status=401)
        else:
            return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    else:
        return JsonResponse({'message': 'This endpoint only accepts POST requests'})



# #This method only updates the total availability count of the vaccine (provided it doesn't affect the on-hold vaccines),
# #since the project requirements documentation only mentions the same requirement under 'Update Vaccine'.
# #Information needed: vaccine_id, new_total_count, user_id
@csrf_exempt
def update_vaccine(request):
    if request.method=="POST":
        print(request.POST.get('user_id'))
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
            UPDATE vaccine_vaccine SET total_availability=%s WHERE id=%s AND on_hold<%s
            """
            cursor = connection.cursor()
            cursor.execute(query2, [request.POST['new_count'], request.POST['vaccine_id'],request.POST['new_count']])
            user_row = cursor.rowcount
        if user_row>0:
            return JsonResponse({'message': 'Vaccine Details updated successfully.', 'user_type': user_type})
        elif user_row==0:
            return JsonResponse({'message': 'No record found.'}, status=401)
        else:
            return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    else:
        return JsonResponse({'message': 'This endpoint only accepts POST requests'})





from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Nurse
from .serializers import NurseSerializer

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

        
        #serializer = CustomNurseSerializer(data =nurses_data, many=True)
        #print('Data before sending:', serializer.initial_data)
        return JsonResponse(nurses_data, safe=False)
        
        # #return JsonResponse(serializer.data, safe=False)
        # if serializer.is_valid():
        #     return JsonResponse(serializer.data, safe=False)
        # else:
        #     return JsonResponse({'message': 'Serializer error'}, status=800)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def patient_list(request):
    if request.method == 'GET':
        query = '''
            SELECT vaccine_patient.id as id, vaccine_user.name as name, vaccine_user.age as age, vaccine_user.gender as gender,
            vaccine_patient.race as race, vaccine_patient.no_doses_received as prev_doses,vaccine_timeslot.timestamp as next_appointment
            
            FROM vaccine_patient JOIN vaccine_user ON vaccine_user.id = vaccine_patient.user_id 
            LEFT JOIN vaccine_appointment ON vaccine_appointment.patient_id = vaccine_patient.id
            LEFT JOIN vaccine_timeslot ON vaccine_appointment.timeslot_id = vaccine_timeslot.id
        '''

        # query2 = ''' SELECT vaccine_timeslot.timestamp as next_appointment
        #             FROM vaccine_patient JOIN vaccine_user ON vaccine_user.id = vaccine_patient.user_id 
        #             LEFT JOIN vaccine_appointment ON vaccine_appointment.patient_id = vaccine_patient.id
        #         JOIN vaccine_timeslot ON vaccine_appointment.timeslot_id = vaccine_timeslot.id 
        # '''
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            patients_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        #print(patients_data)
        return JsonResponse(patients_data, safe=False)

        # serializer = CustomPatientSerializer(data=patients_data, many=True)
        
        # if serializer.is_valid():
        #     return JsonResponse(serializer.data, safe=False)
        # else:
        #     return JsonResponse({'message': 'Serializer error'}, status=500)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)





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
        username = request.POST.get('username')
        password = request.POST.get('password')

        print([name, employee_id, age])

        # Check if user with the given employee_id already exists
        if Nurse.objects.filter(emp_id=employee_id).exists():
            return JsonResponse({'message': 'Cannot Register. User already exists'}, status=400)

        # Create a new user in the vaccine_user table
        user = User.objects.create(
            name=name,
            password=password,
            phone_number=phone_number,
            ssn="None",
            address=address,
            age=age,
            gender=gender,
            user_type="nurse",
            user_name=username
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




# ======================================== Nurse Dashboard =================================================================

#Address and Phone Number update from Nurse. 
#Information needed: user_id, user_type, phone_number, address
#If either phone number or address is unchanged, send the original value.

#ACCESSED BY NURSE
@csrf_exempt
def update_nurse_info(request,user_id,user_type):
    
    if request.method=='GET':
        query = """
        SELECT phone_number, address FROM vaccine_user WHERE vaccine_user.id=%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            columns = [col[0] for col in cursor.description]
            nurse_data = cursor.fetchone()
        if not nurse_data:
            return JsonResponse({'message': 'Nurse ID does not exist'}, status=404)
        response_data = dict(zip(columns, nurse_data))
        return JsonResponse(response_data, safe=False)
        
    elif request.method=='POST':
        user_row = -1

        if user_type=="Nurse" or user_type=="nurse":
            query2 = """
            UPDATE vaccine_user SET phone_number=%s, address=%s WHERE id= %s
            """
            #updated_details = json.loads(request.body.decode('utf-8'))['updatedDetails']
            
            phone_number = request.POST.get("phone_number")
            address = request.POST.get("address")

            cursor = connection.cursor()
            cursor.execute(query2, [phone_number, address, user_id])
            user_row = cursor.rowcount
            if user_row>0:
                return JsonResponse({'message': 'Nurse Details updated successfully.', 'user_type': user_type})
            elif user_row==0:
                return JsonResponse({'message': 'No record found.'}, status=401)
        else:
            return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
        
        
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

#Information Needed: appt_id, user_id, user_type
#We can do it this way: Once patient has scheduled an appt, they get the appt id. They can share it with the nurse. 
#So, similar to adding nurse id in admin module, the nurse will simply enter the appt id to create a record.
#Hence, only a put request considered.

### ????? WE NEED TO CHECK IF RECORD ALREADY EXISTS FOR THE GIVEN APPOINTMENT ID??????
### ??? 
@csrf_exempt
def record_appt(request):
    user_type = request.POST.get('user_type')
    print(user_type)
    if user_type not in ["Nurse", "nurse"]:
        return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    if request.method=="POST":
        user_id = request.POST.get('user_id')
        print(user_id)
        nurse_id = Nurse.objects.get(user__id = user_id)
        nurse_id = nurse_id.id
        appt_id = request.POST.get('appt_id')
        with connection.cursor() as cursor:
            # always provide fields when updating because id is auto-increment
            query1 = """INSERT INTO vaccine_record(apt_id_id,nurse_id) 
            VALUES(%s, %s)"""
            cursor.execute(query1, [appt_id, nurse_id])
            query2 ="""UPDATE vaccine_vaccine SET total_availability=total_availability-1, on_hold=on_hold-1 
                    WHERE id IN (SELECT vaccine_id FROM vaccine_appointment WHERE id=%s)"""
            cursor.execute(query2, [appt_id])
            query3 = """UPDATE vaccine_patient SET no_doses_received=(SELECT vaccine_dose FROM vaccine_appointment WHERE id=%s) 
                        WHERE id=(SELECT patient_id FROM vaccine_appointment where id=%s)"""
            cursor.execute(query3, [appt_id, appt_id])
            return JsonResponse({'message': "Record added successfully.", 'user_type': user_type})
    else:
        return JsonResponse({'message': 'This endpoint only accepts POST requests'})

@csrf_exempt
def get_nurse_info(request, user_id):
    try:
        nurse_info = {}
        # Your SQL query to fetch nurse information
        query_nurse = '''SELECT vaccine_nurse.id as id, vaccine_nurse.emp_id as emp_id, vaccine_user.name as name, 
        vaccine_user.phone_number as phone_number, vaccine_user.address as address, vaccine_user.gender as gender,
        vaccine_user.user_name as username  
        FROM vaccine_nurse JOIN vaccine_user ON vaccine_nurse.user_id = vaccine_user.id 
        WHERE vaccine_nurse.user_id = %s'''

        with connection.cursor() as cursor:
            # Execute query to get nurse information
            cursor.execute(query_nurse, [user_id])
            result_nurse = cursor.fetchone()

            if result_nurse:
                # Include basic nurse information in nurse_info
                nurse_info = {
                    'id': result_nurse[0],
                    'emp_id': result_nurse[1],
                    'name': result_nurse[2],
                    'phone_number': result_nurse[3],
                    'address': result_nurse[4],
                    'gender': result_nurse[5],
                    'username': result_nurse[6]
                }

                # Execute query to get schedule times
                query_schedule = '''SELECT vaccine_timeslot.timestamp 
                            FROM vaccine_assigned JOIN vaccine_timeslot  ON vaccine_assigned.timeslot_id = vaccine_timeslot.id
                            WHERE nurse_id = %s'''
                cursor.execute(query_schedule, [result_nurse[0]])
                result_schedule = cursor.fetchall()

                # Include schedule times in nurse_info
                nurse_info['schedule_times'] = [time[0] for time in result_schedule]

        return JsonResponse(nurse_info, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def schedule_nurse_slot(request, user_type, user_id):

    if request.method=='POST':
        print("Check method.")
        user_row = -1
        timestamp = request.POST.get('timestamp')
        print(timestamp)
        timestamp = timestamp.replace('T', ' ')
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        print(timestamp)
        timezone.activate('UTC')
        today = timezone.now().date() + timedelta(1)
        timezone.deactivate()
        # if not timestamp:
        #     timestamp = datetime(today.year, today.month, today.day, 18, 0, 0)
        if user_type in ["Nurse", "nurse"]:
            query1 = """
                SELECT id, open_slots FROM vaccine_timeslot
                WHERE timestamp = %s
            """
            cursor = connection.cursor()
            cursor.execute(query1, [timestamp])
            user_row = cursor.fetchone()
            if user_row:
                print("Check row: ", user_row)
                # query2 = """
                # SELECT COUNT(*) FROM Assigned WHERE timeslot = %s GROUP BY timeslot
                # """
                # cursor = connection.cursor()
                # cursor.execute(query2, [user_row[0], ])
                # count_row = cursor.fetchone()
                # if count_row[0]<12:
                nurse_id = Nurse.objects.get(user__id = user_id)
                nurse_id = nurse_id.id
                print(nurse_id)
                query2 = """
                INSERT INTO vaccine_assigned(timeslot_id, nurse_id) VALUES(%s, %s)
                """
                cursor = connection.cursor()
                cursor.execute(query2, [user_row[0], nurse_id])
                print("assigned.")
                query3 = """
                UPDATE vaccine_timeslot SET open_slots=%s WHERE id=%s
                """
                cursor = connection.cursor()
                cursor.execute(query3, [min(100, user_row[1]+10), user_row[0]])
                print("Ending existing data.")
                if cursor.rowcount>0:
                    return JsonResponse({'message': 'Slot scheduled successfully.', 'user_type': user_type})
                else:
                    return JsonResponse({'message': 'Unable to schedule the slot.'}, status=401)
            else:
                print("No user_row.")
                nurse_id = Nurse.objects.get(user__id = user_id)
                nurse_id = nurse_id.id
                print("No row: ", nurse_id)
                print(timestamp)
                query2 = """
                INSERT INTO vaccine_timeslot(timestamp, open_slots) VALUES(%s, %s)
                """
                cursor = connection.cursor()
                cursor.execute(query2, [timestamp, 10])
                timeid = cursor.lastrowid
                print("Id of slot: ", timeid)
                query3 = """
                INSERT INTO vaccine_assigned(timeslot_id, nurse_id) VALUES(%s, %s)
                """
                cursor.execute(query3, [timeid, nurse_id])
                print("Before end of no row.")
                if cursor.rowcount>0:
                    return JsonResponse({'message': 'Slot scheduled successfully.', 'user_type': user_type})
                else:
                    return JsonResponse({'message': 'Unable to schedule the slot.'}, status=401)
        else:
            return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    elif request.method=='GET':
        print("Nurse or not.")
        nurse_id = Nurse.objects.get(user = user_id)
        nurse_id = nurse_id.id
        if user_type not in ["Nurse", "nurse"]:
            return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
        timezone.activate('UTC')
        today = timezone.now().date() + timedelta(1)
        timezone.deactivate()
        print("Tomorrow is: ", today)
        print("Possible?: ", str(today))
        print(timezone.now())
        timeslots = [10, 11, 12, 13, 14, 15, 16, 17]
        # query = """
        # SELECT A.timestamp AS timestamp FROM vaccine_timeslot A JOIN vaccine_assigned B ON A.id = B.timeslot_id WHERE DATE(A.timestamp)=%s AND B.timeslot_id IN (SELECT timeslot_id from vaccine_assigned WHERE nurse_id=%s) GROUP BY A.id HAVING COUNT(DISTINCT B.nurse_id)<12
        # """
        query = """
        SELECT HOUR(A.timestamp) AS timestamp FROM vaccine_timeslot A JOIN vaccine_assigned B ON A.id = B.timeslot_id WHERE DATE(A.timestamp)=%s GROUP BY B.timeslot_id HAVING COUNT(DISTINCT B.nurse_id)>=12
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [today])
            full_slots = cursor.fetchall()
            print("Full Slots: ", full_slots)
            query2 = """
            SELECT HOUR(A.timestamp) AS timestamp FROM 
            vaccine_timeslot A JOIN vaccine_assigned B on A.id = B.timeslot_id 
            WHERE DATE(timestamp)=%s AND nurse_id = %s
            """
            cursor.execute(query2, [today, nurse_id])
            used_slots = cursor.fetchall()
            print("Used Nurse Slots: ", used_slots)
            for i in used_slots:
                if int(i[0]) in timeslots:
                    timeslots.remove(i[0])
            for i in full_slots:
                if int(i[0]) in timeslots:
                    timeslots.remove(i[0])
            print("Remaining slots: ", timeslots)
            timestamps = []
            for hour in timeslots:
                # query3 = """
                # SELECT STR_TO_DATE(CONCAT(%s, ' ', LPAD(%s, 2, '0'), ':00:00'), '%Y-%m-%D %H:%M:%S') AS full_timestamp;
                # """
                time = datetime(today.year, today.month, today.day, hour, 0, 0)
                print(time)
                # cursor.execute(query3, [str(today), hour])
                # slot = cursor.fetchone()
                slot = time
                print("Str slot: ", slot, type(slot))
                timestamps.append(slot)
            #cursor.execute("""SELECT COUNT(DISTINCT B.nurse_id) FROM vaccine_timeslot A JOIN vaccine_assigned B ON A.id = B.timeslot_id WHERE DATE(A.timestamp)=""")
        if not timestamps:
            return JsonResponse({'message': 'Nurse ID does not exist or no appointments exist.'}, status=404)
        response_data = timestamps
        print("Response Data: ", response_data)
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

        #new


@csrf_exempt
def cancel_slot(request, user_id, user_type):
    if user_type not in ["Nurse", "nurse"]:
        return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    timezone.activate('UTC')
    today = timezone.now()
    timezone.deactivate()
    #timestamp = datetime(today.year, today.month, today.day, 19, 0, 0)
    if request.method=="GET":
        nurse_id = Nurse.objects.get(user__id = user_id)
        nurse_id = nurse_id.id
        print(nurse_id)
        query = """
        SELECT A.timestamp AS timestamp FROM vaccine_timeslot A JOIN vaccine_assigned B ON A.id = B.timeslot_id JOIN vaccine_nurse C ON B.nurse_id = C.id WHERE C.id = %s AND A.timestamp>%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [nurse_id, today])
            #columns = [col[0] for col in cursor.description]
            nurse_data = cursor.fetchall()
            print("Check: ", nurse_data)
        if not nurse_data:
            return JsonResponse({'message': 'Appointments does not exist'}, status=404)
        response_data = nurse_data
        return JsonResponse(response_data, safe=False)
    elif request.method=="POST":
        user_row = -1
        print("POST Req.")
        timestamp = request.POST.get('timestamp')
        timestamp = timestamp.replace('T', ' ')
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        today = today.date() + timedelta(1)
        print("Timestamp: ", timestamp)
        nurse_id = Nurse.objects.get(user__id = user_id)
        nurse_id = nurse_id.id
        print("Nurse?: ", nurse_id)
        query1 = """
        SELECT COUNT(DISTINCT nurse_id) FROM vaccine_assigned A JOIN vaccine_timeslot B ON A.timeslot_id=B.id  WHERE B.timestamp=%s GROUP BY A.timeslot_id
        """
        query2 = """
        DELETE FROM vaccine_assigned WHERE nurse_id=%s AND timeslot_id = (SELECT id FROM vaccine_timeslot WHERE timestamp=%s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query1, [timestamp])
            nurse_count = cursor.fetchone()[0]
            print("Number of nurses in timeslot: ", nurse_count)
            try:
                cursor.execute(query2, [nurse_id, timestamp])
            except e:
                return JsonResponse({'message': 'No other nurse available to attend appointments.'}, status=401)
            user_row = cursor.rowcount
            if user_row==0:
                return JsonResponse({'message': 'No record found.'}, status=401)
            elif user_row<0:
                return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
            else:
                message = 'Slot cancelled successfully.'
            if nurse_count<2:
                try:
                    cursor.execute("""DELETE FROM vaccine_timeslot WHERE timestamp=%s""", [timestamp])
                except:
                    pass
                print("Deleted timeslot.")
                return JsonResponse({'message': message, 'user_type': user_type})
            else:
                cursor.execute("""UPDATE vaccine_timeslot SET open_slots=LEAST(100, open_slots-10) WHERE timestamp=%s""", [timestamp])
                print("Check open slots.")
                return JsonResponse({'message': message, 'user_type': user_type})
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})




# ================================ Patient Dashboard =============================================
# ================================================================================================

#Information Needed: all user, patient fields
#Information that can't be modified/registered: user_type, no_doses_received
@csrf_exempt
def patient_update_info(request, user_id, user_type):
    if user_type not in ["Patient","patient"]:
        return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    if request.method=="GET":
        query = """
        SELECT A.name as name, A.password as password, A.phone_number as phone_number, A.ssn as ssn, 
        A.address as address, A.age as age, A.gender as gender, A.user_name as user_name, B.race as race, 
        B.occupation as occupation, B.medical_history as medical_history 
        FROM vaccine_user A JOIN vaccine_patient B ON A.id = B.user_id WHERE A.id=%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            columns = [col[0] for col in cursor.description]
            patient_data = cursor.fetchone()
        if not patient_data:
            return JsonResponse({'message': 'Patient does not exist.'}, status=404)
        response_data = dict(zip(columns, patient_data))
        return JsonResponse(response_data, safe=False)
    elif request.method=="POST":
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
            cursor.execute("""UPDATE vaccine_patient SET race=%s, occupation=%s, medical_history=%s WHERE user_id=%s""", [race, job, med_det, user_id])
            return JsonResponse({'message': 'Patient Details updated successfully.', 'user_type': user_type})
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

#Information Needed (for POST): user_type, user_id
#Information Needed (for PUT): user_type, user_id, vaccine_id (or name, no_dose of vaccine), timestamp
@csrf_exempt
def patient_schedule_appt(request, user_id, user_type):
    if user_type not in ["Patient", "patient"]:
        return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    if request.method=="PUT":
        #print("Data: ", request.POST, user_id, user_type)
        put_data = MultiPartParser(request.META, request, request.upload_handlers).parse()
        put_data = dict(put_data[0])
        #print("Try: ", put_data)
        vaccine_id = int(put_data['vaccine_id'][0])
        timestamp = put_data['timestamp'][0]
        timestamp = timestamp.replace('T', ' ')
        #print(vaccine_id, timestamp)
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        #print("Time: ", timestamp, type(timestamp))
        query = """
        INSERT INTO vaccine_appointment(vaccine_dose, vaccine_id, patient_id, timeslot_id) 
        VALUES((SELECT number_doses_free FROM vaccine_vaccine WHERE id=%s), %s, %s, (SELECT id FROM vaccine_timeslot WHERE timestamp=%s))
        """
        patient_id = Patient.objects.get(user__id = user_id)
        patient_id = patient_id.id
        with connection.cursor() as cursor:
            print("Yes.")
            cursor.execute(query, [vaccine_id, vaccine_id, patient_id, timestamp])
            print("Check 1")
            apptid = cursor.lastrowid
            print("ID: ", apptid)
            cursor.execute("UPDATE vaccine_vaccine SET on_hold = on_hold+1 WHERE id=%s", [vaccine_id])
            print("Check X.")
            cursor.execute("UPDATE vaccine_timeslot SET open_slots = open_slots-1 WHERE timestamp=%s", [timestamp])
            print("Updated.")
            count = cursor.rowcount
            print(count)
            if count>0:
                message = 'Appointment registered with ID: '+str(apptid)
                return JsonResponse({'message': message, 'user_type': user_type, 'appt_id': apptid}, status=201)
            else:
                return JsonResponse({'message': 'Error in Registration.'}, status=401) 
    elif request.method=="POST":
        print("here")

        patient_id = Patient.objects.get(user__id = user_id)
        patient_id = patient_id.id
        query = """
        SELECT * FROM vaccine_patient WHERE id=%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [patient_id])
            patient = cursor.fetchone()
            print("Patient details: ", patient_id, patient, patient[1])
        if patient[1]==0:
            query2 = """
            SELECT id, name FROM vaccine_vaccine WHERE number_doses_free=1 AND total_availability-on_hold>0
            """
            with connection.cursor() as cursor:
                cursor.execute(query2)
                columns = [col[0] for col in cursor.description] #name, number_doses_free, on_hold, description, total_availability
                #Change select * from query2 to individual column names if all columns not wanted.
                vaccine_data = cursor.fetchall()
                print("Vaccine data: ", vaccine_data)
            if not vaccine_data:
                return JsonResponse({'message': 'No Vaccines Available.'})
            #vaccine_data = tuple(zip(columns, *vaccine_data))
            timezone.activate('UTC')
            appt_day = timezone.now().date() + timedelta(1)
            timezone.deactivate()
            query3 = """
            SELECT timestamp FROM vaccine_timeslot WHERE open_slots>0 AND DATE(timestamp)=%s
            """
            with connection.cursor() as cursor:
                cursor.execute(query3, [appt_day])                              # query 3
                columns = [col[0] for col in cursor.description]
                schedule_data = cursor.fetchall()
                print("Schedule data 0: ", schedule_data)
            if not schedule_data:
                return JsonResponse({'message': 'No Appointments Available.'})
            #schedule_data = tuple(zip(columns, *schedule_data))
            print("Schedule data: ", schedule_data)
            response_data = {"schedule_data": schedule_data, "vaccine_data": vaccine_data}  # changed schedule_data
            return JsonResponse(response_data, safe=False)
        elif patient[1]>0:
            with connection.cursor() as cursor:
                
                temp_query = """
                SELECT * FROM vaccine_patient WHERE id=%s AND 
                no_doses_received<=(SELECT max(number_doses_free) FROM vaccine_vaccine WHERE 
                name=(SELECT name FROM vaccine_vaccine WHERE id=(SELECT vaccine_id FROM vaccine_appointment 
                WHERE patient_id=%s ORDER BY vaccine_dose DESC LIMIT 1)))
                """
                cursor.execute(temp_query, [patient_id, patient_id])
                vcheck = cursor.fetchall()
                if not vcheck:
                    return JsonResponse({'message': 'You\'ve been completely vaccinated.'})
            vc_id = Appointment.objects.filter(patient=patient_id).order_by('-vaccine_dose').values().first()
            vc_id = vc_id['vaccine_id']
            query2 = """
            SELECT id, name FROM vaccine_vaccine WHERE total_availability-on_hold>0 AND id=%s 
            """
            #IN (SELECT vaccine_id FROM vaccine_appointment WHERE patient_id=%s ORDER BY vaccine_dose DESC LIMIT 1)
            with connection.cursor() as cursor:
                cursor.execute(query2, [vc_id])
                columns = [col[0] for col in cursor.description]
                vaccine_data = cursor.fetchall()
            if not vaccine_data:
                return JsonResponse({'message': 'Vaccine Dose not Available.'}, status=404)
            #vaccine_data = tuple(zip(columns, *vaccine_data))
            timezone.activate('UTC')
            appt_day = timezone.now().date() + timedelta(1)
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


@csrf_exempt
def patient_cancel_appt(request, user_id, user_type): 
    if user_type not in ["Patient", "patient"]:
        return JsonResponse({'message': 'User doesn\'t have access.'}, status=401)
    if request.method=="GET":
        print("GET req")
        #appt_id = request.POST.get('appt_id')
        patient_id = Patient.objects.get(user=user_id)
        patient_id = patient_id.id
        patient_name = Patient.objects.filter(user=user_id).values('user_id__name').first()
        
        print(patient_id, patient_name)
        time = timezone.now()
        print("Check")
        apt = Appointment.objects.filter(timeslot__timestamp__gt=time, patient = patient_id).values('id', 'vaccine_dose', 'vaccine_id', 'vaccine_id__name', 'patient_id', 'timeslot_id', 'timeslot_id__timestamp')
        # print(apt)
        # timestamp = str(apt['timeslot_id__timestamp'])
        # timestamp = timestamp.replace('T', " ")
        if apt:
            apt = dict(apt.first())
            response_data = {'appt_id': apt['id'], 'vaccine_id': apt['vaccine_id'], 'vaccine_name': apt['vaccine_id__name'], 'patient_id': patient_id, 'patient_name': patient_name, 'timeslot_id': apt['timeslot_id'], 'timestamp': apt['timeslot_id__timestamp']}
            if response_data:
                return JsonResponse(response_data, safe=False)
        return JsonResponse({'message': 'Unable to fetch appointment.'}, status=401)
    elif request.method=="POST":
        appt_id = request.POST.get('appt_id')
        print("POST req received: ", appt_id)
        apt = Appointment.objects.filter(id = appt_id).values('id', 'vaccine_id', 'timeslot_id', 'timeslot_id__timestamp')
        print("Apt: ", apt)
        if timezone.now()>apt.first()['timeslot_id__timestamp']:
            print("Condition matches, return.")
            return JsonResponse({'message': 'The appointment is past deletion.'}, status=401)
        query = """
        DELETE FROM vaccine_appointment WHERE id = %s
        """
        count = -1
        apt = apt.first()
        print("Deleting: ", apt)
        with connection.cursor() as cursor:
            print("Checking connection.")
            cursor.execute(query, [appt_id])
            print("Deleted.")
            cursor.execute("""UPDATE vaccine_vaccine SET on_hold = GREATEST(0, on_hold-1) WHERE id=%s""", [apt['vaccine_id']])
            print("Updating vaccine.")
            cursor.execute("UPDATE vaccine_timeslot SET open_slots = LEAST(100, open_slots+1) WHERE id=%s", [apt['timeslot_id']])
            print("Updating timeslot.")
            count = cursor.rowcount
            print("Counting changes: ", count)
            connection.commit()
        if count>0:
            return JsonResponse({'message': "Appointment deleted.", 'user_type': user_type}, status=201)
    else:
        return JsonResponse({'message': 'This endpoint only accepts PUT or POST requests'})

def get_patient_info(request, user_id):
    try:
        patient_info = {}
        # Your SQL query to fetch patient information
        query_patient = '''SELECT vaccine_patient.id as id, vaccine_user.name as name, 
        vaccine_user.phone_number as phone_number, vaccine_user.address as address, 
        vaccine_user.gender as gender, vaccine_user.user_name as username, vaccine_patient.no_doses_received as totaldoses,
        vaccine_patient.race as race, vaccine_patient.occupation as occup, vaccine_patient.medical_history as medhistory  
        FROM vaccine_patient JOIN vaccine_user ON vaccine_patient.user_id = vaccine_user.id 
        WHERE vaccine_patient.user_id = %s'''

        with connection.cursor() as cursor:
            # Execute query to get patient information
            cursor.execute(query_patient, [user_id])
            result_patient = cursor.fetchone()

            if result_patient:
                # Include basic patient information in patient_info
                patient_info = {
                    'id': result_patient[0],
                    'name': result_patient[1],
                    'phone_number': result_patient[2],
                    'address': result_patient[3],
                    'gender': result_patient[4],
                    'username': result_patient[5],
                    'totaldoses': result_patient[6],
                    'race': result_patient[7],
                    'occup': result_patient[8],
                    'medhistory': result_patient[9]
                }

                # Execute query to get schedule times (modify as needed for patient schedule)
                query_schedule = '''SELECT vaccine_timeslot.timestamp 
                                    FROM vaccine_timeslot JOIN vaccine_appointment ON vaccine_timeslot.id = vaccine_appointment.timeslot_id
                                    WHERE patient_id = %s'''
                cursor.execute(query_schedule, [result_patient[0]])
                result_schedule = cursor.fetchall()

                # Include schedule times in patient_info
                patient_info['schedule_times'] = [time[0] for time in result_schedule]

        return JsonResponse(patient_info, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

