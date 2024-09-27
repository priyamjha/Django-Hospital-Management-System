from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)





class Department(models.Model):
    name = models.CharField(max_length=100)
    diagnostics = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name



class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    professional_license_number = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)

    objects = CustomUserManager()
    
    
    
    
class PatientRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'})
    created_date = models.DateField(auto_now_add=True)
    diagnostics = models.TextField()
    observations = models.TextField(blank=True)
    treatments = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    misc = models.TextField(blank=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_records', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Record {self.record_id} for {self.patient}"

