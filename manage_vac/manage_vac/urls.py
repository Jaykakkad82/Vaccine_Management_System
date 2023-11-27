"""
URL configuration for manage_vac project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vaccine.views import login_view
from vaccine.views import nurse_list, patient_list, register_nurse, admin_update_nurse_details, delete_nurse, add_vaccine, update_vaccine
from vaccine.views import update_nurse_info,register_patient, record_appt, get_nurse_info,patient_update_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_view, name='login'),
    path('api/admin_nurses/', nurse_list, name='nurse-list'),
    path('api/admin_patientinfo/', patient_list, name='patient_list'),
    path('api/admin_register_nurse/', register_nurse, name='register-nurse'),
    path('api/admin-update-nurse-details/<int:nurse_id>/', admin_update_nurse_details, name='admin-nurseUpdate'),
    path('api/admin_delete_nurse/', delete_nurse, name='delete-nurse'),
    path('api/admin_add-vaccine/', add_vaccine, name='add-vaccine'),
    path('api/admin_update-vaccine/', update_vaccine, name='update-vaccine'),
    path('api/get-nurse-info/<int:user_id>/<str:user_type>/', update_nurse_info, name='nurse-updateInfo'),
    path('api/register-patient/', register_patient, name='register-patient'),
    path('api/record-appt/nurse/', record_appt, name='record-appt'),
    path('api/nurse-info/<int:user_id>/',get_nurse_info , name='nurse-myinfo'),
    path('api/patient-update-info/<int:user_id>/<str:user_type>/', patient_update_info, name='patient-updateInfo'),

]
