from django.urls import path
from .views import choose_user_type, my_patients, register, login, logout, patient_dashboard, doctor_dashboard, doctor_list, doctor_detail, update_doctor_details, home, patient_list, get_patient_detail, update_patient, update_patient_detail, delete_patient, get_patient_records, patient_records, department_list, department_doctors_list, update_doctor, department_patients_list, view_patient_record

urlpatterns = [
    
    path('register/', register, name='register'),
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    
    path('patient-dashboard/', patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', doctor_dashboard, name='doctor_dashboard'),
    
    path('doctors/', doctor_list, name='doctor_list'),
    path('doctors/<int:doctor_id>/', doctor_detail, name='doctor_detail'),
    path('doctors/<int:doctor_id>/update/', update_doctor_details, name='update_doctor'),
    
    path('home/', home, name='home'),
    
    path('patients/', patient_list, name='patient_list'),
    path('patients/<int:patient_id>/', get_patient_detail, name='get_patient_detail'),

    path('patient_records/', patient_records, name='patient-records'),
    path('patient_records/<int:patient_id>/', get_patient_records, name='get_patient_records'),
    
    path('patient_records/<int:patient_id>/update/', update_patient_detail, name='update_patient_detail'),
    path('patients/<int:patient_id>/delete/', delete_patient, name='delete_patient'),
    
    path('departments/', department_list, name='department_list'),
    path('doctors/<int:pk>/update/', update_doctor, name='update_doctor'),
    path('departments/<int:pk>/doctors/', department_doctors_list, name='department_doctors_list'),
    path('department/<int:pk>/patients/', department_patients_list, name='department_patients_list'),
    
    path('patient/record/', view_patient_record, name='view_patient_record'),
    path('patient/update/<int:pk>/', update_patient, name='update_patient'),
    
    path('choose-user-type/', choose_user_type, name='user_type_choice'),
    
    path('my-patients/', my_patients, name='my_patients'),

]
