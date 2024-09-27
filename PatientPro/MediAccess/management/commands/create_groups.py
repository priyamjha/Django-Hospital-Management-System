from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create Patient and Doctor groups'

    def handle(self, *args, **kwargs):
        # Create Patient group
        patient_group, created = Group.objects.get_or_create(name='Patients')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Patient group'))

        # Create Doctor group
        doctor_group, created = Group.objects.get_or_create(name='Doctors')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Doctor group'))
