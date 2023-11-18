from django.contrib import admin

# Register your models here.
from .models import User, Patient, Nurse, Vaccine, Timeslot, Appointment, Record, Assigned

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Nurse)
admin.site.register(Vaccine)
admin.site.register(Timeslot)
admin.site.register(Appointment)
admin.site.register(Record)
admin.site.register(Assigned)
