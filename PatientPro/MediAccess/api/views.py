from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from MediAccess.models import CustomUser, Department, PatientRecord
from .serializers import CustomUserSerializer, DepartmentSerializer, PatientRecordSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/departments',
        'GET /api/departments/:id',
        'GET /api/patients',
        'GET /api/patients/:id',
        'GET /api/records',
        'GET /api/records/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getDepartments(request):
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getDepartment(request, pk):
    department = Department.objects.get(id=pk)
    serializer = DepartmentSerializer(department, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getPatients(request):
    patients = CustomUser.objects.filter(user_type='patient')
    serializer = CustomUserSerializer(patients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPatient(request, pk):
    patient = CustomUser.objects.get(id=pk, user_type='patient')
    serializer = CustomUserSerializer(patient, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getRecords(request):
    records = PatientRecord.objects.all()
    serializer = PatientRecordSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRecord(request, pk):
    try:
        record = PatientRecord.objects.get(record_id=pk)  # Use record_id instead of id
        serializer = PatientRecordSerializer(record, many=False)
        return Response(serializer.data)
    except PatientRecord.DoesNotExist:
        return Response({'error': 'Record not found'}, status=404)
