# serializers.py

from rest_framework import serializers
from .models import User, Nurse

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class NurseSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Nurse
        fields = '__all__'

class CustomNurseSerializer(serializers.Serializer):
    # Define fields based on your data structure
    id = serializers.IntegerField()
    emp_id = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    address = serializers.CharField()
    gender = serializers.CharField(max_length=7)
    # Add other fields based on your data structure

class CustomPatientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    age = serializers.IntegerField()
    gender = serializers.CharField(max_length=7)
    race = serializers.CharField(max_length=255)
    prev_doses = serializers.IntegerField()
    next_appointment = serializers.DateTimeField()