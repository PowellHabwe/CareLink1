from django.contrib import admin
from .models import Destination,Hospital,ServiceProvided,Doctor, MedicalStaff,Vehicle,Service,HospitalService,Appointment,PaymentService
# Register your models here.

class HospitalAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug':('hospital_name',)}

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(MedicalStaff)
admin.site.register(Vehicle)
admin.site.register(Service)
admin.site.register(HospitalService)
admin.site.register(Appointment)
admin.site.register(PaymentService)
admin.site.register(ServiceProvided)
admin.site.register(Doctor)
admin.site.register(Destination)