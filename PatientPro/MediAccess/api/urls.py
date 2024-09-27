from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('departments/', views.getDepartments),
    path('departments/<str:pk>/', views.getDepartment),
    path('patients/', views.getPatients),
    path('patients/<str:pk>/', views.getPatient),
    path('records/', views.getRecords),
    path('records/<str:pk>/', views.getRecord),
]
