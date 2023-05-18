from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    pricing = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    hospital_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(default="hospital@gmail.com")
    website = models.URLField(default="https://www.google.com/")
    services_offered = models.CharField(null=True, max_length=50000,default="Support Services, Diagnostic Services,Maternity Services,  Pediatric Services")
    ambulance_available = models.BooleanField(default=False)
    ambulance_contacts = models.CharField(max_length=50000)
    vacancies_available = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True, default="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries")
    image = models.ImageField(upload_to='photos/products', blank=True)
    is_available = models.BooleanField(default = True)
    home_available = models.BooleanField(default = False)
    home_general = models.BooleanField(default = False)
    home_specialty = models.BooleanField(default = False)
    home_psychiatric = models.BooleanField(default = False)
    home_clinic = models.BooleanField(default = False)
    affordable = models.BooleanField(default = False)
    top_rated = models.BooleanField(default = False)
    new = models.BooleanField(default = False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    hospital_appointments = models.ManyToManyField('Appointment', related_name='hospitals')

    service_provided = models.ManyToManyField('ServiceProvided', related_name='hospitals')

    accepted_paymentservices = models.ManyToManyField('PaymentService', related_name='hospitals')

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.hospital_name
    
class HospitalService(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    pricing = models.CharField(max_length=200)
    availability = models.BooleanField(default=False)
    slots = models.IntegerField()

    def __str__(self):
        return f"{self.hospital.hospital_name} - {self.service.name}"
    
class MedicalStaff(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Vehicle(models.Model):
    VEHICLE_TYPES = (
        ('ambulance', 'Ambulance'),
        ('medical_shuttle', 'Medical Shuttle'),
    )
    vehicle_type = models.CharField(choices=VEHICLE_TYPES, max_length=20)
    vehicle_name = models.CharField( max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact = models.CharField(max_length=200)
    availability = models.BooleanField(default=True)
    price_per_km = models.DecimalField(max_digits=9, decimal_places=2)  # Add the new field for price per kilometer

    def __str__(self):
        return self.vehicle_name
    

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='appointments')
    email = models.EmailField()

    def __str__(self):
        return self.name

class PaymentService(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='accepted_payment_services')
    payment_method = models.CharField(max_length=100)
    service = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.payment_method} - {self.service}"
    

class ServiceProvided(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    service = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.hospital.hospital_name} - {self.service}"
    

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    hospitals_worked = models.ManyToManyField('Hospital', related_name='doctors')
    available_from = models.DateField()
    available_to = models.DateField()
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class Destination(models.Model):
    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()


    def __str__(self):
        return self.destination_latitude
    