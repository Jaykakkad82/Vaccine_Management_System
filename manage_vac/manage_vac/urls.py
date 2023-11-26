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
from vaccine.views import nurse_list, patient_list, register_nurse, admin_update_nurse_details, delete_nurse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_view, name='login'),
    path('api/admin_nurses/', nurse_list, name='nurse-list'),
    path('api/admin_patientinfo/', patient_list, name='patient_list'),
    path('api/admin_register_nurse/', register_nurse, name='register-nurse'),
    path('api/admin-update-nurse-details/<int:nurse_id>/', admin_update_nurse_details, name='admin-nurseUpdate'),
    path('api/admin_delete_nurse/', delete_nurse, name='delete-nurse'),
    
]
