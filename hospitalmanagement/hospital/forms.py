from django import forms
from django.contrib.auth.models import User
from . import models


# ------------------------------ For Admin -----------------------------

class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


# ------------------------------ For Doctor ------------------------------

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields = ['address', 'mobile', 'department', 'email', 'status', 'profile_pic']


# ------------------------------  For Employee ------------------------------

class EmployeeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = ['address', 'department', 'mobile', 'status', 'email', 'profile_pic']


class PatientForm(forms.ModelForm):
    assignedDoctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),
                                              empty_label="Doctor Name and Department", to_field_name="user_id")

    class Meta:
        model = models.Patient
        fields = ['patientName', 'patientAddress', 'patientMobile', 'status']


class AppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),
                                      empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId = forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),
                                       empty_label="Patient Name and Phone number", to_field_name="id")

    class Meta:
        model = models.Appointment
        fields = ['description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class PatientAppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),
                                      empty_label="Doctor Name and Department", to_field_name="user_id")

    class Meta:
        model = models.Appointment
        fields = ['description', 'status']


class ProductForm(forms.ModelForm):
    categoryId = forms.ModelChoiceField(queryset=models.Category.objects.all(),
                                        empty_label="Category Name", to_field_name="id")

    class Meta:
        model = models.Product
        fields = ['itemName', 'issuedQuantity', 'receivedQuantity', 'totalQuantity', 'unitPrice']


class SaleForm(forms.Form):
    patientId = forms.IntegerField()

    itemId = forms.ModelChoiceField(queryset=models.Product.objects.all(),
                                        empty_label="Category Name", to_field_name="id")

    quantity = forms.IntegerField()

    amountReceived = forms.IntegerField()
    class Meta:
        model = models.Sale


class LabTestForm(forms.ModelForm):
    class Meta:
        model = models.LabTest
        fields = '__all__'


class LabForm(forms.ModelForm):
    patientId = forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),
                                       empty_label="Patient Name and Phone number", to_field_name="id")
    testId = forms.ModelChoiceField(queryset=models.LabTest.objects.all().order_by('testName'),
                                       empty_label="Test Name", to_field_name="id")

    class Meta:
        model = models.LabResult
        fields = ['testResult']