from django.db import models
from django.contrib.auth.models import User


# Create your models here.

doctor_departments = [
    ('General Physician', 'General Physician'), ('Pediatrician', 'Pediatrician'),
    ('General Surgeon', 'General Surgeon'),
    ('Dentist', 'Dentist'), ('ENT Specialist', 'ENT Specialist'),
    ('Cardiologist', 'Cardiologist'), ('Dermatologists', 'Dermatologists'),
    ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
    ('Allergists/Immunologists', 'Allergists/Immunologists'),
    ('Anesthesiologists', 'Anesthesiologists'),
    ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
]


#
# need to add invalid email, invalid password or username,etc...
#

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=1280)
    mobile = models.CharField(max_length=12, null=True)
    email = models.EmailField(max_length=128, null=True)
    department = models.CharField(max_length=128, choices=doctor_departments, default='Cardiologist')
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} {} ({})".format(self.user.first_name, self.user.last_name, self.department)


employee_department = [('Reception', 'Reception'), ('Pharmacy', 'Pharmacy'),
                       ('Laboratory', 'Laboratory'),
                       ]


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/EmployeeProfilePic/', null=True, blank=True)
    department = models.CharField(max_length=128, choices=employee_department, default='Receptionist')
    address = models.CharField(max_length=128)
    mobile = models.CharField(max_length=12, null=True)
    email = models.EmailField(max_length=128, null=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name + " (" + self.department + ")"


class Patient(models.Model):
    patientName = models.CharField(max_length=128, null=True)
    patientAddress = models.CharField(max_length=128)
    patientMobile = models.CharField(max_length=12, null=False)

    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate = models.DateField(auto_now=True)
    pendingMedicalCharge = models.PositiveIntegerField(default=0)
    pendingLabTestCharge = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.patientName

    @property
    def get_id(self):
        return self.pk

    def __str__(self):
        return self.patientName + " (" + self.patientMobile + ")"


class Appointment(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    doctorId = models.PositiveIntegerField(null=True)
    doctorName = models.CharField(max_length=128, null=True)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=250)
    status = models.BooleanField(default=False)


class PatientDischargeDetails(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=128)
    assignedDoctorName = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    mobile = models.CharField(max_length=12, null=True)
    admitDate = models.DateField(null=False)
    releaseDate = models.DateField(null=False)
    daySpent = models.PositiveIntegerField(null=False, default=0)

    roomCharge = models.PositiveIntegerField(null=False, default=0)
    medicineCost = models.PositiveIntegerField(null=False, default=0)
    labTestCost = models.PositiveIntegerField(null=False, default=0)
    doctorFee = models.PositiveIntegerField(null=False, default=0)
    OtherCharge = models.PositiveIntegerField(null=False, default=0)
    total = models.PositiveIntegerField(null=False, default=0)

    def __str__(self):
        return self.patientName + " (" + self.mobile + ") " + str(self.releaseDate)


# Pharmacy models

class Category(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    categoryId = models.PositiveIntegerField(null=True)
    categoryName = models.CharField(max_length=50, null=True, blank=True)
    itemName = models.CharField(max_length=50, null=True, blank=True, unique=True)
    totalQuantity = models.IntegerField(default=0, null=True, blank=True)
    issuedQuantity = models.IntegerField(default=0, null=True, blank=True)
    receivedQuantity = models.IntegerField(default=0, null=True, blank=True)
    unitPrice = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.itemName


class Sale(models.Model):
    patientId = models.IntegerField(default=0, null=True)
    issuedTo = models.CharField(max_length=50, null=True, blank=True)

    itemId = models.PositiveIntegerField(null=True)
    itemName = models.CharField(max_length=50, null=True, blank=True)

    unitPrice = models.PositiveIntegerField(null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    saleDate = models.DateField(auto_now=True)

    totalPrice = models.IntegerField(default=0, null=True, blank=True)

    paymentStatus = models.BooleanField(default=False)

    def __str__(self):
        return self.issuedTo + " (" + self.itemName + ")"


# Laboratory


class LabTest(models.Model):
    testName = models.CharField(max_length=128, null=True, blank=True, unique=True)
    testPrice = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.testName


class LabResult(models.Model):
    patientId = models.IntegerField(default=0, null=True)
    patientName = models.CharField(max_length=50, null=True, blank=True)

    testId = models.PositiveIntegerField(null=True)
    testName = models.CharField(max_length=128)

    testDate = models.DateField(auto_now=True)
    testResult = models.TextField(max_length=750)

    paymentStatus = models.BooleanField(default=False)

    def __str__(self):
        return self.patientName + " (" + self.testName + ")"
