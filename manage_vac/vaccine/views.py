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
from .models import User, Nurse, Patient, Vaccine, Timeslot, Appointment, Record, Assigned  # Import your User model


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


# ======= COMMENTED OUT - Admin Dashboard - received code =====================#

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


# ======================================== TILL THIS POINT =================================================================


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
