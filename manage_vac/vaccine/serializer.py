from rest_framework import serializers
from .models import *


class NurseSerializer(serializers.Serializer):

    emp_id = serializers.CharField(max_length=50)

    def save(self):
        name = self.validated_data['name']
        password = self.validated_data['password']
        phn = self.validated_data['phone_number']
        ssn = self.validated_data['ssn']
        addr = self.validated_data['address']
        age = self.validated_data['age']
        gen = self.validated_data['gen']
        unm = self.validated_data['user_name']
        emp_id = self.validated_data['emp_id']

        user = User(name = name, password = password, phone_number = phn, ssn = ssn, address = addr, age = age, gender = gen, unm = user_name, user_type = "Nurse")
        user.save()
        nurse = Nurse(user = user, emp_id = emp_id)
        nurse.save()

    class Meta:
        model = User
        fields = ['name', 'password', 'phone_number', 'ssn', 'address', 'age', 'gender', 'user_name', 'emp_id']

class VaccineSerializer(serializers.Serializer):

    class Meta:
        fields = __all__

class PatientSerializer(serializers.Serializer):

    class Meta:
        fields = __all__

class TimeslotSerializer(serializers.Serializer):

    class Meta:
        fields = __all__

class AppointmentSerializer(serializers.Serializer):

    class Meta:
        fields = __all__

class RecordSerializer(serializers.Serializer):

    class Meta:
        fields = __all__

class AssignedSerializer(serializers.Serializer):

    class Meta:
        fields = __all__