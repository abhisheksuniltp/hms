from django.contrib import admin
from .models import Doctor, Employee, Patient, Appointment, PatientDischargeDetails, Category, Product, Sale, LabTest, LabResult


# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Doctor, DoctorAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Employee, EmployeeAdmin)


class PatientAdmin(admin.ModelAdmin):
    pass


admin.site.register(Patient, PatientAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Appointment, AppointmentAdmin)


class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass


admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)


class SaleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Sale, SaleAdmin)

class LabTestAdmin(admin.ModelAdmin):
    pass


admin.site.register(LabTest, LabTestAdmin)

class LabResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(LabResult, LabResultAdmin)