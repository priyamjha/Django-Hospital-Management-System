from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm, DoctorUpdateForm, PatientRecordForm, PatientUpdateForm, UserTypeForm
from .models import CustomUser, Department, PatientRecord
from django.core.paginator import Paginator
from django.db.models import Q




@login_required
def my_patients(request):
    if request.user.user_type != 'doctor':
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('home')

    # Fetch the search query from the request
    query = request.GET.get('search', '')

    # Filter patients assigned to the logged-in doctor, optionally filtering by search query
    patients = PatientRecord.objects.filter(doctor=request.user)
    if query:
        patients = patients.filter(patient__full_name__icontains=query) | patients.filter(diagnostics__icontains=query)

    # Set up pagination: 10 patients per page
    paginator = Paginator(patients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Pass the paginator object to the template
        'search_query': query,  # Pass the search query to maintain input value in the search box
    }
    return render(request, 'my_patients.html', context)
    





@login_required
def choose_user_type(request):
    user = request.user
    # If user_type is not set, or if user_type is set to the default value, redirect to the choose_user_type page
    if not user.user_type:
        if request.method == 'POST':
            form = UserTypeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                if user.user_type == 'patient':
                    return redirect('patient_dashboard')
                elif user.user_type == 'doctor':
                    return redirect('doctor_dashboard')
        else:
            form = UserTypeForm(instance=user)
        
        return render(request, 'choose_user_type.html', {'form': form})
    else:
        # Redirect based on the user_type
        if user.user_type == 'patient':
            return redirect('patient_dashboard')
        elif user.user_type == 'doctor':
            return redirect('doctor_dashboard')



@login_required
def update_patient(request, pk):
    # Ensure the logged-in user is authorized to update the patient's details
    patient = CustomUser.objects.get(pk=pk, user_type='patient')
    # Check if the user is a doctor or the patient themselves
    if request.user.user_type != 'doctor' and request.user != patient:
        messages.warning(request, 'You are not authorized to update this patient\'s details.')
        return redirect('home')

    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient details updated successfully.')
            return redirect('view_patient_record')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = PatientUpdateForm(instance=patient)
        
    return render(request, 'patient_update_form.html', {'form': form, 'patient': patient})



@login_required
def view_patient_record(request):
    # Ensure the user is a patient
    if request.user.user_type != 'patient':
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('home')
    # Get the patient's records
    patient_records = PatientRecord.objects.filter(patient=request.user)
    
    return render(request, 'view_patient_record.html', {
        'patient_records': patient_records,
        'patient': request.user
    })



@login_required
def department_patients_list(request, pk):
    # Get the department
    department = Department.objects.get(pk=pk)
    # Get all patients in the department
    patients = CustomUser.objects.filter(user_type='patient', department=department)
    
    # Get the current logged-in user
    current_user = request.user
    
    # Check if the current user is a doctor in the department
    current_user_is_doctor_in_department = request.user.user_type == 'doctor' and request.user.department == department
    
    # Check which patients are assigned to the current doctor (if the user is a doctor)
    assigned_patients = PatientRecord.objects.filter(doctor=current_user).values_list('patient_id', flat=True)

    return render(request, 'department_patients_list.html', {
        'department': department,
        'patients': patients,
        'current_user_is_doctor_in_department': current_user_is_doctor_in_department,
        'assigned_patients': assigned_patients,
    })



@login_required
def department_doctors_list(request, pk):
    # Handle GET request to list all doctors in a specific department
    department = Department.objects.get(pk=pk)
    doctors = CustomUser.objects.filter(user_type='doctor', department=department)
    
    return render(request, 'department_doctors_list.html', {
        'department': department,
        'doctors': doctors,
        'current_user': request.user
    })



@login_required
def update_doctor(request, pk):
    # Handle GET and POST requests to update a doctor's details
    doctor = CustomUser.objects.get(pk=pk, user_type='doctor')
    if request.method == 'POST':
        form = DoctorUpdateForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('department_doctors_list', pk=doctor.department.pk)
    else:
        form = DoctorUpdateForm(instance=doctor)
    
    return render(request, 'doctor_update_form.html', {'form': form, 'doctor': doctor})




@login_required
def department_list(request):
    # Handle GET requests to list all departments
    departments = Department.objects.all()
    
    return render(request, 'department_list.html', {'departments': departments})



@login_required
def patient_records(request):
    # Ensure the user is a doctor to view patients
    if request.user.user_type != 'doctor':
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('home')
    
    search_query = request.GET.get('search', '')
    # Filter patients based on search query
    if search_query:
        patients = CustomUser.objects.filter(
            user_type='patient',
            full_name__icontains=search_query
        ).order_by('-id')  # Use '-date_joined' to order by latest first
    else:
        patients = CustomUser.objects.filter(user_type='patient').order_by('-id')
    
     # Paginate results
    paginator = Paginator(patients, 10)  # Show 10 patients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    return render(request, 'patient_record_list.html', {'patients': patients, 'search_query': search_query,'page_obj': page_obj})



@login_required
def get_patient_records(request, patient_id):
    patient = CustomUser.objects.get(id=patient_id, user_type='patient')
    patient_record = PatientRecord.objects.filter(patient=patient).first()
    context = {
        'patient': patient,
        'patient_record': patient_record
    }
    
    return render(request, 'patient_records.html', context)


@login_required
def get_patient_detail(request, patient_id):
    patient = CustomUser.objects.get(id=patient_id, user_type='patient')
    patient_record = PatientRecord.objects.filter(patient=patient).first()
    context = {
        'patient': patient,
        'patient_record': patient_record
    }
    
    return render(request, 'patient_detail.html', context)



@login_required
def update_patient_detail(request, patient_id):
    patient = CustomUser.objects.get(id=patient_id, user_type='patient')
    
    if request.user.user_type != 'doctor':
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('home')
    
    patient_record, created = PatientRecord.objects.get_or_create(patient=patient)
    
    if request.method == 'POST':
        form = PatientRecordForm(request.POST, instance=patient_record)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient  # Ensure the patient field is set
            record.save()
            
            # Update the patient's department if it was changed in the form
            patient.department = record.department
            patient.save()
            
            messages.success(request, 'Patient record updated successfully.')
            return redirect('get_patient_records', patient_id=patient.id)
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = PatientRecordForm(instance=patient_record)    

    return render(request, 'update_patient_detail.html', {'form': form, 'patient': patient})



@login_required
def delete_patient(request, patient_id):
    patient = CustomUser.objects.get(id=patient_id, user_type='patient')
    if request.user.user_type != 'doctor':
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('home')
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    else:
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('home')


@login_required
def patient_list(request):
    # Ensure the user is a doctor to view patients
    if request.user.user_type != 'doctor':
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('home')
    
    search_query = request.GET.get('search', '')
    patients = CustomUser.objects.filter(user_type='patient').order_by('-id')
    
    if search_query:
        patients = patients.filter(full_name__icontains=search_query)
    
    paginator = Paginator(patients, 10)  # Show 10 patients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'patient_list.html', {'patients': patients,'page_obj': page_obj, 'search_query': search_query})



@login_required
def update_doctor_details(request, doctor_id):
    doctor = CustomUser.objects.get(id=doctor_id, user_type='doctor')
    if request.method == 'POST':
        form = DoctorUpdateForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your detail is updated!')
            return redirect('doctor_detail', doctor_id=doctor.id)
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = DoctorUpdateForm(instance=doctor)

    return render(request, 'update_doctor.html', {'form': form, 'doctor': doctor})



@login_required
def doctor_detail(request, doctor_id):
    doctor = CustomUser.objects.get(id=doctor_id, user_type='doctor')
    is_own_profile = (request.user.id == doctor_id)
    
    return render(request, 'doctor_detail.html', {'doctor': doctor, 'is_own_profile': is_own_profile})



@login_required
def doctor_list(request):
    search_query = request.GET.get('search', '')
    doctors = CustomUser.objects.filter(user_type='doctor', is_superuser=False).values('id', 'full_name')
    
    if search_query:
        doctors = doctors.filter(full_name__icontains=search_query)
    
    paginator = Paginator(doctors.values('id', 'full_name'), 10)  # Show 10 doctors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'doctor_list.html', {'doctors': doctors, 'search_query': search_query, 'page_obj': page_obj})



@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


@login_required
def patient_dashboard(request):
    if request.user.user_type == 'patient':
        records = PatientRecord.objects.filter(patient=request.user)
        return render(request, 'patient_dashboard.html', {'records': records})
    else:
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('login')


@login_required
def doctor_dashboard(request):
    if request.user.user_type == 'doctor':
        return render(request, 'doctor_dashboard.html')
    else:
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('login')



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='MediAccess.backends.MyCustomBackend')
            messages.success(request, 'Registration successful.')
            return redirect('login')  # Redirect to login or another page as needed
        else:
            # Show detailed error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, error)
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})




def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Logged in successfully.')
                if user.user_type == 'patient':
                    return redirect('patient_dashboard')
                elif user.user_type == 'doctor':
                    return redirect('doctor_dashboard')
            else:
                messages.warning(request, 'Invalid credentials.')
        else:
            for error in form.non_field_errors():
                    messages.warning(request, error)
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})




def logout(request):
    auth_logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')


