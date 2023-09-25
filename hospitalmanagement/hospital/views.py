from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from django.contrib import messages
from django.core.exceptions import ValidationError


# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return redirect('userlogin')


def signup_view(request):
    return render(request, 'hospital/index.html')


def admin_signup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            messages.success(request, "Admin account created successfully.")
            return HttpResponseRedirect('userlogin')
        messages.error(request, "Error. Admin account creation failed.")
    return render(request, 'hospital/admin/adminsignup.html', {'form': form})


def doctor_signup_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            messages.success(request, "Doctor account created successfully.")
            return HttpResponseRedirect('userlogin')
        messages.error(request, "Error. Doctor account creation failed.")
    return render(request, 'hospital/doctor/doctorsignup.html', context=mydict)


def employee_signup_view(request):
    userForm = forms.EmployeeUserForm()
    employeeForm = forms.EmployeeForm()
    mydict = {'userForm': userForm, 'employeeForm': employeeForm}
    if request.method == 'POST':
        userForm = forms.EmployeeUserForm(request.POST)
        employeeForm = forms.EmployeeForm(request.POST, request.FILES)
        if userForm.is_valid() and employeeForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            employee = employeeForm.save(commit=False)
            employee.user = user
            employee.save()
            my_employee_group = Group.objects.get_or_create(name='EMPLOYEE')
            my_employee_group[0].user_set.add(user)
            messages.success(request, "Employee account created successfully.")
            return HttpResponseRedirect('userlogin')
        messages.error(request, "Error. Employee account creation failed.")
    return render(request, 'hospital/employee/employeesignup.html', context=mydict)


# -----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()


def is_employee(user):
    return user.groups.filter(name='EMPLOYEE').exists()


# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval = models.Doctor.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request, 'hospital/doctor/doctor_wait_for_approval.html')
    elif is_employee(request.user):
        accountapproval = models.Employee.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return employee_department_check(request)
        else:
            return render(request, 'hospital/employee/employee_wait_for_approval.html')


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def employee_department_check(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    department = employee.department
    if department == "Reception":
        return redirect('reception-dashboard')
    elif department == 'Pharmacy':
        return redirect('pharmacy-dashboard')
    elif department == 'Laboratory':
        return redirect('laboratory-dashboard')


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # for tables in admin dashboard
    doctors = models.Doctor.objects.all().order_by('-id')
    employees = models.Employee.objects.all().order_by('-id')
    appointments = models.Appointment.objects.all().order_by('-id')
    patients = models.Patient.objects.all()
    pendingAppointmentCount = models.Appointment.objects.all().filter(status=False).count()

    myDict = {
        'doctors': doctors,
        'employees': employees,
        'appointments': appointments,
        'patients': patients,
        'pendingAppointmentCount': pendingAppointmentCount,
    }
    return render(request, 'hospital/admin/admin_dashboard.html', context=myDict)


# ------------------ Doctor ------------------------
@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request, 'hospital/admin/admin_doctor.html')


# Inside Doctor Record
@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, 'hospital/admin/admin_view_doctor.html', {'doctors': doctors})


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_update_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)

    userForm = forms.DoctorUserForm(instance=user)
    doctorForm = forms.DoctorForm(instance=doctor)
    myDict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST, instance=user)
        doctorForm = forms.DoctorForm(request.POST,request.FILES, instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.status = True
            doctor.save()
            messages.success(request, "Updating successful.")
            return redirect('admin-view-doctor')
        messages.error(request, "Error. Updating failed.")
    return render(request, 'hospital/admin/admin_update_doctor.html', context=myDict)


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_delete_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')


# Inside Register Doctor
@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            messages.success(request, "Doctor added successfully.")
            return HttpResponseRedirect('admin-view-doctor')
        messages.error(request, "Error. Registration failed.")
    return render(request, 'hospital/admin/admin_add_doctor.html', context=mydict)


# Inside Approve Doctor
@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=False)
    return render(request, 'hospital/admin/admin_approve_doctor.html', {'doctors': doctors})


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    doctor.status = True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')


# ----------------------Employee-----------------------

@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_employee_view(request):
    return render(request, 'hospital/admin/admin_employee.html')


# inside employee record
@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_view_employee_view(request):
    employees = models.Employee.objects.all().filter(status=True)
    return render(request, 'hospital/admin/admin_view_employee.html', {'employees': employees})


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_update_employee_view(request, pk):
    employee = models.Employee.objects.get(id=pk)
    user = models.User.objects.get(id=employee.user_id)

    userForm = forms.EmployeeUserForm(instance=user)
    employeeForm = forms.EmployeeForm(instance=employee)
    myDict = {'userForm': userForm, 'employeeForm': employeeForm}
    if request.method == 'POST':
        userForm = forms.EmployeeUserForm(request.POST, instance=user)
        employeeForm = forms.EmployeeForm(request.POST,request.FILES, instance=employee)
        if userForm.is_valid() and employeeForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            employee = employeeForm.save(commit=False)
            employee.status = True
            employee.save()
            messages.success(request, "Updating successful.")
            return redirect('admin-view-employee')
        messages.error(request, "Error. Updating failed.")
    return render(request, 'hospital/admin/admin_update_employee.html', context=myDict)


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_delete_employee_view(request, pk):
    employee = models.Employee.objects.get(id=pk)
    user = models.User.objects.get(id=employee.user_id)
    user.delete()
    employee.delete()
    return redirect('admin-view-employee')


# Inside Employee Record
@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_add_employee_view(request):
    userForm = forms.EmployeeUserForm()
    employeeForm = forms.EmployeeForm()
    myDict = {'userForm': userForm, 'employeeForm': employeeForm}
    if request.method == 'POST':
        userForm = forms.EmployeeUserForm(request.POST)
        employeeForm = forms.EmployeeForm(request.POST, request.FILES)
        if userForm.is_valid() and employeeForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            employee = employeeForm.save(commit=False)
            employee.user = user
            employee.status = True
            employee.save()

            my_employee_group = Group.objects.get_or_create(name='EMPLOYEE')
            my_employee_group[0].user_set.add(user)
            messages.success(request, "Employee added successfully.")
            return HttpResponseRedirect('admin-view-employee')
        messages.error(request, "Error. Registration failed.")
    return render(request, 'hospital/admin/admin_add_employee.html', context=myDict)


# Inside Approve Employee
@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_approve_employee_view(request):
    employees = models.Employee.objects.all().filter(status=False)
    return render(request, 'hospital/admin/admin_approve_employee.html', {'employees': employees})


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def approve_employee_view(request, pk):
    employee = models.Employee.objects.get(id=pk)
    employee.status = True
    employee.save()
    return redirect(reverse('admin-approve-employee'))


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def reject_employee_view(request, pk):
    employee = models.Employee.objects.get(id=pk)
    user = models.User.objects.get(id=employee.user_id)
    user.delete()
    employee.delete()
    return redirect('admin-approve-employee')


# ----------------PATIENT START -----------------------

@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    allPatients = models.Patient.objects.all().order_by('patientName')
    patients = models.Patient.objects.all()
    doctors = models.Doctor.objects.all().filter(status=True)
    # For searching
    if request.method == 'POST':
        if request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            doctorId = request.POST.get('doctorId')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            patients = models.Patient.objects.filter(assignedDoctorId=doctorId, id=patientId,
                                                     admitDate__range=(startDate, endDate))

        elif request.POST.get('startDate') and not request.POST.get('endDate') and not request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            startDate = request.POST.get('startDate')
            patients = models.Patient.objects.filter(admitDate=startDate)

        elif not request.POST.get('startDate') and request.POST.get('endDate') and not request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            endDate = request.POST.get('endDate')
            patients = models.Patient.objects.filter(admitDate=endDate)

        elif not request.POST.get('startDate') and not request.POST.get('endDate') and request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            doctorId = request.POST.get('doctorId')
            patients = models.Patient.objects.filter(assignedDoctorId=doctorId)

        elif not request.POST.get('startDate') and not request.POST.get('endDate') and not request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            print(1)
            patientId = request.POST.get('patientId')
            patients = models.Patient.objects.filter(id=patientId)

        elif request.POST.get('startDate') and request.POST.get('endDate') and not request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            patients = models.Patient.objects.filter(admitDate__range=(startDate, endDate))

        elif request.POST.get('startDate') and not request.POST.get('endDate') and request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            doctorId = request.POST.get('doctorId')
            startDate = request.POST.get('startDate')
            patients = models.Patient.objects.filter(assignedDoctorId=doctorId, admitDate=startDate)

        elif request.POST.get('startDate') and not request.POST.get('endDate') and not request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            startDate = request.POST.get('startDate')
            patients = models.Patient.objects.filter(admitDate=startDate, id=patientId)

        elif not request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            doctorId = request.POST.get('doctorId')
            endDate = request.POST.get('endDate')
            patients = models.Patient.objects.filter(assignedDoctorId=doctorId, admitDate=endDate)

        elif not request.POST.get('startDate') and request.POST.get('endDate') and not request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            endDate = request.POST.get('endDate')
            patients = models.Patient.objects.filter(admitDate=endDate, id=patientId)

        elif not request.POST.get('startDate') and not request.POST.get('endDate') and request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            doctorId = request.POST.get('doctorId')
            patientId = request.POST.get('patientId')
            patients = models.Patient.objects.filter(assignedDoctorId=doctorId, id=patientId)

        elif request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            doctorId = request.POST.get('doctorId')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            patients = models.Patient.objects.filter(assignedDoctorId=doctorId, admitDate__range=(startDate, endDate))

        elif request.POST.get('startDate') and request.POST.get('endDate') and not request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            patients = models.Patient.objects.filter(id=patientId, admitDate__range=(startDate, endDate))

        elif request.POST.get('startDate') and not request.POST.get('endDate') and request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            doctorId = request.POST.get('doctorId')
            startDate = request.POST.get('startDate')
            patients = models.Patient.objects.filter(assignedDoctorId=doctorId, id=patientId, admitDate=startDate)

        elif not request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            doctorId = request.POST.get('doctorId')
            endDate = request.POST.get('endDate')
            patients = models.Patient.objects.filter(assignedDoctorId=doctorId, id=patientId, admitDate=endDate)

    return render(request, 'hospital/admin/admin_patient.html',
                  {'allPatients': allPatients, 'patients': patients, 'doctors': doctors})


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_admit_patient_view(request):
    if request.method == 'POST':
        patient = models.Patient.objects.get(id=request.POST.get('patientId'))
        patient.status = True
        patient.save()
        messages.success(request, "Patient Admitted successfully.")
        return HttpResponseRedirect('admin-patient')
    messages.error(request, "Error. Patient Admit failed. ")
    return HttpResponseRedirect('admin-patient')


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    dischargedPatients = models.Patient.objects.all().filter(status=False)
    patientForm = forms.PatientForm()
    myDict = {'patientForm': patientForm, 'dischargedPatients': dischargedPatients}
    if request.method == 'POST':
        patientForm = forms.PatientForm(request.POST)
        if patientForm.is_valid():
            patient = patientForm.save(commit=False)
            patient.patientName = request.POST.get('patientName')
            patient.patientAddress = request.POST.get('patientAddress')
            patient.patientMobile = request.POST.get('patientMobile')
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.status = True
            patient.save()
            messages.success(request, "Patient registration successful.")
            return HttpResponseRedirect('admin-patient')
        messages.error(request, "Error. Patient registration failed. ")
    return render(request, 'hospital/admin/admin_add_patient.html', context=myDict)


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_delete_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.delete()
    return redirect('admin-patient')


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patientForm = forms.PatientForm(instance=patient)
    myDict = {'patientForm': patientForm}
    if request.method == 'POST':
        patientForm = forms.PatientForm(request.POST, instance=patient)
        if patientForm.is_valid():
            patient = patientForm.save(commit=False)
            patient.patientName = request.POST.get('patientName')
            patient.patientAddress = request.POST.get('patientAddress')
            patient.patientMobile = request.POST.get('patientMobile')
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()
            messages.success(request, "Updating successful.")
            return redirect('admin-patient')
        messages.error(request, "Error. Updating failed.")
    return render(request, 'hospital/admin/admin_update_patient.html', context=myDict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharged_patients_view(request):
    dischargedPatients = models.PatientDischargeDetails.objects.all().distinct()
    return render(request, 'hospital/admin/admin_view_discharged_patient.html',
                  {'dischargedPatients': dischargedPatients})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_delete_discharge_record_view(request, pk):
    record = models.PatientDischargeDetails.objects.get(id=pk)
    record.delete()
    return redirect('admin-discharged-patients')


# --------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'hospital/admin/admin_discharge_patient.html', {'patients': patients})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    days = (date.today() - patient.admitDate)  # 2 days, 0:00:00
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days  # only how many day that is 2
    patientDict = {
        'patientId': pk,
        'name': patient.get_name,
        'mobile': patient.patientMobile,
        'address': patient.patientAddress,
        'admitDate': patient.admitDate,
        'todayDate': date.today(),
        'day': d,
        'assignedDoctorName': assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict = {
            'roomCharge': int(request.POST['roomCharge']) * int(d),
            'doctorFee': request.POST['doctorFee'],
            'medicineCost': patient.pendingMedicalCharge,
            'labTestCost': patient.pendingLabTestCharge,
            'OtherCharge': request.POST['OtherCharge'],
            'total': (int(request.POST['roomCharge']) * int(d)) + int(request.POST['doctorFee']) + int(
                patient.pendingMedicalCharge) + int(patient.pendingLabTestCharge) + int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        # for updating to database patientDischargeDetails (pDD)
        pDD = models.PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.patientAddress
        pDD.mobile = patient.patientMobile

        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(patient.pendingMedicalCharge)
        pDD.labTestCost = int(patient.pendingLabTestCharge)
        pDD.roomCharge = int(request.POST['roomCharge']) * int(d)
        pDD.doctorFee = int(request.POST['doctorFee'])
        pDD.OtherCharge = int(request.POST['OtherCharge'])
        pDD.total = (int(request.POST['roomCharge']) * int(d)) + int(request.POST['doctorFee']) + int(
            patient.pendingMedicalCharge) + int(patient.pendingLabTestCharge) + int(request.POST['OtherCharge'])
        patient.pendingMedicalCharge = 0
        patient.pendingLabTestCharge = 0
        patient.status = False
        pDD.save()
        patient.save()
        messages.success(request, "Discharge successful.")
        return render(request, 'hospital/admin/patient_final_bill.html', context=patientDict)
    return render(request, 'hospital/admin/patient_generate_bill.html', context=patientDict)


# -----------------APPOINTMENT START---------------------

@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    appointments = models.Appointment.objects.all()
    patients = models.Patient.objects.all().order_by('patientName')
    doctors = models.Doctor.objects.all().filter(status=True)
    # For searching
    if request.method == 'POST':
        if request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            doctorId = request.POST.get('doctorId')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            appointments = models.Appointment.objects.filter(doctorId=doctorId, patientId=patientId,
                                                             appointmentDate__range=(startDate, endDate))

        elif request.POST.get('startDate') and not request.POST.get('endDate') and not request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            startDate = request.POST.get('startDate')
            appointments = models.Appointment.objects.filter(appointmentDate=startDate)

        elif not request.POST.get('startDate') and request.POST.get('endDate') and not request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            endDate = request.POST.get('endDate')
            appointments = models.Appointment.objects.filter(appointmentDate=endDate)

        elif not request.POST.get('startDate') and not request.POST.get('endDate') and request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            doctorId = request.POST.get('doctorId')
            appointments = models.Appointment.objects.filter(doctorId=doctorId)

        elif not request.POST.get('startDate') and not request.POST.get('endDate') and not request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            print(1)
            patientId = request.POST.get('patientId')
            appointments = models.Appointment.objects.filter(patientId=patientId)

        elif request.POST.get('startDate') and request.POST.get('endDate') and not request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            appointments = models.Appointment.objects.filter(appointmentDate__range=(startDate, endDate))

        elif request.POST.get('startDate') and not request.POST.get('endDate') and request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            doctorId = request.POST.get('doctorId')
            startDate = request.POST.get('startDate')
            appointments = models.Appointment.objects.filter(doctorId=doctorId, appointmentDate=startDate)

        elif request.POST.get('startDate') and not request.POST.get('endDate') and not request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            startDate = request.POST.get('startDate')
            appointments = models.Appointment.objects.filter(appointmentDate=startDate, patientId=patientId)

        elif not request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            doctorId = request.POST.get('doctorId')
            endDate = request.POST.get('endDate')
            appointments = models.Appointment.objects.filter(doctorId=doctorId, appointmentDate=endDate)

        elif not request.POST.get('startDate') and request.POST.get('endDate') and not request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            endDate = request.POST.get('endDate')
            appointments = models.Appointment.objects.filter(appointmentDate=endDate, patientId=patientId)

        elif not request.POST.get('startDate') and not request.POST.get('endDate') and request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            doctorId = request.POST.get('doctorId')
            patientId = request.POST.get('patientId')
            appointments = models.Appointment.objects.filter(doctorId=doctorId, patientId=patientId)

        elif request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get(
                'doctorId') and not request.POST.get('patientId'):
            doctorId = request.POST.get('doctorId')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            appointments = models.Appointment.objects.filter(doctorId=doctorId,
                                                             appointmentDate__range=(startDate, endDate))

        elif request.POST.get('startDate') and request.POST.get('endDate') and not request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            appointments = models.Appointment.objects.filter(patientId=patientId,
                                                             appointmentDate__range=(startDate, endDate))

        elif request.POST.get('startDate') and not request.POST.get('endDate') and request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            doctorId = request.POST.get('doctorId')
            startDate = request.POST.get('startDate')
            appointments = models.Appointment.objects.filter(doctorId=doctorId, patientId=patientId,
                                                             appointmentDate=startDate)

        elif not request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get(
                'doctorId') and request.POST.get('patientId'):
            patientId = request.POST.get('patientId')
            doctorId = request.POST.get('doctorId')
            endDate = request.POST.get('endDate')
            appointments = models.Appointment.objects.filter(doctorId=doctorId, patientId=patientId,
                                                             appointmentDate=endDate)

    return render(request, 'hospital/admin/admin_appointment.html',
                  {'appointments': appointments, 'patients': patients, 'doctors': doctors})


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_book_appointment_view(request):
    appointmentForm = forms.AppointmentForm()
    myDict = {'appointmentForm': appointmentForm, }
    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.POST.get('patientId')
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = models.Patient.objects.get(id=request.POST.get('patientId')).patientName
            appointment.status = False
            appointment.save()
            messages.success(request, "Appointment booked successfully.")
            return HttpResponseRedirect('admin-appointment')
        messages.error(request, "Error. Appointment booking failed. ")
    return render(request, 'hospital/admin/admin_book_appointment.html', context=myDict)


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_delete_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-appointment')


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_update_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointmentForm = forms.AppointmentForm(instance=appointment)
    patientName = models.Patient.objects.get(id=appointment.patientId).patientName
    myDict = {'appointmentForm': appointmentForm, 'patientName': patientName}
    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST, instance=appointment)
        appointmentForm.fields['patientId'].required = False
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = models.Appointment.objects.get(id=pk).patientId
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = models.Patient.objects.get(id=appointment.patientId).patientName
            appointment.save()
            messages.success(request, "Updating successful.")
            return redirect('admin-appointment')
        messages.error(request, "Error. Updating failed.")
    return render(request, 'hospital/admin/admin_update_appointment.html', context=myDict)


# ------------------------Pharmacy ----------------------------

@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_pharmacy_view(request):
    sales = models.Sale.objects.all().order_by('-id')
    return render(request, 'hospital/admin/admin_pharmacy.html', {'sales': sales})


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_pharmacy_receipt_details_view(request, receipt_id):
    patients = models.Patient.objects.all().filter(status=True)
    receipt = models.Sale.objects.get(id=receipt_id)
    return render(request, 'hospital/admin/admin_pharmacy_receipt_details.html',
                  {'receipt': receipt, 'patients': patients})


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_laboratory_view(request):
    tests = models.LabResult.objects.all().order_by('-id')
    return render(request, 'hospital/admin/admin_laboratory.html', {'tests': tests})


@login_required(login_url='userlogin')
@user_passes_test(is_admin)
def admin_laboratory_receipt_details_view(request, receipt_id):
    patients = models.Patient.objects.all().filter(status=True)
    receipt = models.LabResult.objects.get(id=receipt_id)
    return render(request, 'hospital/admin/admin_laboratory_receipt_details.html',
                  {'receipt': receipt, 'patients': patients})


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------

@login_required(login_url='userlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # for  table in doctor dashboard
    pendingAppointmentCount = models.Appointment.objects.all().filter(status=False, doctorId=request.user.id).count()
    appointments = models.Appointment.objects.all().filter(doctorId=request.user.id).order_by('-id')
    patients = models.Patient.objects.all()
    mydict = {
        'pendingAppointmentCount': pendingAppointmentCount,
        'patients': patients,
        'appointments': appointments,
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # for profile picture of doctor in sidebar
    }
    return render(request, 'hospital/doctor/doctor_dashboard.html', context=mydict)


# ----------Doctor Appointment ---------
@login_required(login_url='userlogin')
@user_passes_test(is_doctor)
def approve_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse('doctor-dashboard'))


@login_required(login_url='userlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('doctor-dashboard')


# ----------- Doctor Patient ---------------

@login_required(login_url='userlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # for profile picture of doctor in sidebar
    }
    return render(request, 'hospital/doctor/doctor_patient.html', context=mydict)


@login_required(login_url='userlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id).order_by(
        'patientName')
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'hospital/doctor/doctor_view_patient.html', {'patients': patients, 'doctor': doctor})


@login_required(login_url='userlogin')
@user_passes_test(is_doctor)
def doctor_view_discharged_patient_view(request):
    dischargedPatients = models.PatientDischargeDetails.objects.all().distinct().filter(
        assignedDoctorName=request.user.first_name)
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'hospital/doctor/doctor_view_discharged_patient.html',
                  {'dischargedPatients': dischargedPatients, 'doctor': doctor})


# ---------------------------------------------------------------------------------
# ------------------------ EMPLOYEE RELATED VIEWS ------------------------------
# ---------------------------------------------------------------------------------

# ----------- RECEPTION --------------------
@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def reception_dashboard_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    patients = models.Patient.objects.all().filter(status=False)
    return render(request, 'hospital/employee/reception_dashboard.html',
                  context={'employee': employee, 'patients': patients})


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def reception_admit_patient_view(request):
    if request.method == 'POST':
        patient = models.Patient.objects.get(id=request.POST.get('patientId'))
        patient.status = True
        patient.save()
        messages.success(request, "Patient Admitted successfully.")
        return HttpResponseRedirect('reception-dashboard')
    messages.error(request, "Error. Patient Admit failed. ")
    return HttpResponseRedirect('reception-dashboard')


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def reception_book_appointment_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    appointmentForm = forms.AppointmentForm()
    mydict = {'appointmentForm': appointmentForm, 'employee': employee}
    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.POST.get('patientId')
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = models.Patient.objects.get(id=request.POST.get('patientId')).patientName
            appointment.status = False
            appointment.save()
            messages.success(request, "Appointment booked successfully.")
            return HttpResponseRedirect('reception-book-appointment')
        messages.error(request, "Error. Appointment booking failed. ")
    return render(request, 'hospital/employee/reception_book_appointment.html', context=mydict)


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def reception_view_appointment_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.all()
    patients = models.Patient.objects.all()
    return render(request, 'hospital/employee/reception_view_appointment.html',
                  {'appointments': appointments, 'patients': patients, 'employee': employee})


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def reception_add_patient_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    patientForm = forms.PatientForm()
    mydict = {'patientForm': patientForm, 'employee': employee}
    if request.method == 'POST':
        patientForm = forms.PatientForm(request.POST)
        if patientForm.is_valid():
            patient = patientForm.save(commit=False)
            patient.patientName = request.POST.get('patientName')
            patient.patientAddress = request.POST.get('patientAddress')
            patient.patientMobile = request.POST.get('patientMobile')
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.status = True
            patient.save()
            messages.success(request, "Patient registration successful.")
            return HttpResponseRedirect('reception-book-appointment')
        messages.error(request, "Error. Patient registration failed. ")
    return render(request, 'hospital/employee/reception_add_patient.html', context=mydict)


# --------------------- FOR DISCHARGING PATIENT BY RECEPTION-------------------------


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def reception_discharge_patients_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'hospital/employee/reception_discharge_patient.html',
                  {'patients': patients, 'employee': employee})


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def reception_discharge_patient_view(request, pk):
    employee = models.Employee.objects.get(user_id=request.user.id)
    patient = models.Patient.objects.get(id=pk)
    days = (date.today() - patient.admitDate)  # 2 days, 0:00:00
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days  # only how many day that is 2
    patientDict = {
        'patientId': pk,
        'name': patient.get_name,
        'mobile': patient.patientMobile,
        'address': patient.patientAddress,
        'admitDate': patient.admitDate,
        'todayDate': date.today(),
        'day': d,
        'assignedDoctorName': assignedDoctor[0].first_name,
        'employee': employee,
    }
    if request.method == 'POST':
        feeDict = {
            'employee': employee,
            'roomCharge': int(request.POST['roomCharge']) * int(d),
            'doctorFee': request.POST['doctorFee'],
            'medicineCost': patient.pendingMedicalCharge,
            'labTestCost': patient.pendingLabTestCharge,
            'OtherCharge': request.POST['OtherCharge'],
            'total': (int(request.POST['roomCharge']) * int(d)) + int(request.POST['doctorFee']) + int(
                patient.pendingMedicalCharge) + int(patient.pendingLabTestCharge) + int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        # for updating to database patientDischargeDetails (pDD)
        pDD = models.PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.patientAddress
        pDD.mobile = patient.patientMobile
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(patient.pendingMedicalCharge)
        pDD.labTestCost = int(patient.pendingLabTestCharge)
        pDD.roomCharge = int(request.POST['roomCharge']) * int(d)
        pDD.doctorFee = int(request.POST['doctorFee'])
        pDD.OtherCharge = int(request.POST['OtherCharge'])
        pDD.total = (int(request.POST['roomCharge']) * int(d)) + int(request.POST['doctorFee']) + int(
            patient.pendingMedicalCharge) + int(patient.pendingLabTestCharge) + int(request.POST['OtherCharge'])
        patient.pendingMedicalCharge = 0
        patient.pendingLabTestCharge = 0
        patient.status = False
        pDD.save()
        patient.save()
        messages.success(request, "Last Discharge successful.")
        return render(request, 'hospital/employee/reception_patient_final_bill.html', context=patientDict)
    return render(request, 'hospital/employee/reception_patient_generate_bill.html', context=patientDict)


# ------------------ PHARMACY ---------------------------

@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_dashboard_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    patients = models.Patient.objects.all().filter(status=True)

    return render(request, 'hospital/employee/pharmacy_dashboard.html',
                  {'employee': employee, 'patients': patients})


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_issue_to_view(request):
    if request.method == 'GET':
        patientId = request.GET.get("patientId")
        return pharmacy_issue_to_patient_view(request, patientId)
    return redirect('pharmacy-dashboard')


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_issue_to_patient_view(request, patientId):
    employee = models.Employee.objects.get(user_id=request.user.id)
    products = models.Product.objects.all().order_by('itemName')

    patient = models.Patient.objects.get(id=patientId)

    myDict = {'employee': employee, 'patient': patient, 'products': products}
    return render(request, "hospital/employee/pharmacy_issue_to_patient.html", context=myDict)


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_sale_confirm_view(request):
    if request.method == 'POST':
        patientId = request.POST.get("patientId")
        patient = models.Patient.objects.get(id=patientId)
        issueTo = patient.patientName
        itemId = request.POST.get("itemId")
        itemName = models.Product.objects.get(id=request.POST.get("itemId")).itemName
        product = models.Product.objects.get(id=request.POST.get("itemId"))
        unitPrice = int(request.POST.get("unitPrice"))
        quantity = int(request.POST.get("quantity"))
        totalPrice = unitPrice * quantity

        obj = models.Sale(patientId=patientId, issuedTo=issueTo, itemId=itemId, itemName=itemName,
                          unitPrice=unitPrice, quantity=quantity, totalPrice=totalPrice)
        patient.pendingMedicalCharge += totalPrice
        product.issuedQuantity += quantity
        product.totalQuantity -= quantity
        product.save()
        obj.save()
        patient.save()
        messages.success(request, "Sale successful.")
        return pharmacy_issue_to_patient_view(request, patientId)
    messages.error(request, "Error. Sale failed. ")
    return HttpResponseRedirect('pharmacy-dashboard')


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_product_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    patients = models.Patient.objects.all()
    products = models.Product.objects.all().order_by("itemName")
    return render(request, 'hospital/employee/pharmacy_product.html',
                  {'employee': employee, 'patients': patients, 'products': products})


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_add_new_product_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    productForm = forms.ProductForm()
    myDict = {'employee': employee, 'productForm': productForm}
    if request.method == 'POST':
        productForm = forms.ProductForm(request.POST)
        if productForm.is_valid():
            product = productForm.save(commit=False)
            product.categoryId = request.POST.get('categoryId')
            product.categoryName = models.Category.objects.get(id=request.POST.get('categoryId')).name
            product.itemName = request.POST.get('itemName')
            product.receivedQuantity = request.POST.get('receivedQuantity')
            product.totalQuantity = product.receivedQuantity
            product.unitPrice = request.POST.get('unitPrice')
            product.status = True
            product.save()
            messages.success(request, "Product registration successful.")
            return HttpResponseRedirect('pharmacy-add-new-product')
        messages.error(request, "Error. Product registration failed. ")
    return render(request, 'hospital/employee/pharmacy_add_new_product.html', context=myDict)


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_delete_product_view(request, pk):
    product = models.Product.objects.get(id=pk)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('pharmacy-product')


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_add_new_category_view(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        categoryObj = models.Category()
        categoryObj.name = category
        try:
            categoryObj.full_clean()
            categoryObj.save()
        except ValidationError:
            messages.error(request, "Error. Adding Category failed. ")
            return HttpResponseRedirect('pharmacy-add-new-product')
        except ValueError:
            return HttpResponseRedirect('pharmacy-add-new-product')
        messages.success(request, "Adding Category successful.")
        return HttpResponseRedirect('pharmacy-add-new-product')
    messages.error(request, "Error. Adding Category failed. ")
    return HttpResponseRedirect('pharmacy-add-new-product')


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_delete_category_view(request):
    if request.method == 'POST':
        categoryId = request.POST.get('categoryId')
        try:
            category = models.Category.objects.get(id=categoryId)
            category.delete()
        except ValidationError:
            messages.error(request, "Error. Deleting Category failed. ")
            return HttpResponseRedirect('pharmacy-add-new-product')
        except ValueError:
            return HttpResponseRedirect('pharmacy-add-new-product')
        messages.success(request, "Category Deleted.")
        return HttpResponseRedirect('pharmacy-add-new-product')
    messages.error(request, "Error. Deleting Category failed. ")
    return HttpResponseRedirect('pharmacy-add-new-product')


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_add_to_stock_view(request):
    if request.method == 'POST':
        productId = request.POST.get('productId')
        receivedQuantity = request.POST.get('receivedQuantity')
        product = models.Product.objects.get(id=productId)
        product.receivedQuantity += int(receivedQuantity)
        product.totalQuantity += int(receivedQuantity)
        product.save()
        messages.success(request, "Stock Added Successfully")
        return HttpResponseRedirect('pharmacy-product')
    messages.error(request, "Error. Stock Adding failed. ")
    return HttpResponseRedirect('pharmacy-product')


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_receipts_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    sales = models.Sale.objects.all().order_by('-id')
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'hospital/employee/pharmacy_receipts.html',
                  {'employee': employee, 'patients': patients, 'sales': sales})


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_receipt_details_view(request, receipt_id):
    patients = models.Patient.objects.all().filter(status=True)
    receipt = models.Sale.objects.get(id=receipt_id)
    return render(request, 'hospital/employee/pharmacy_receipt_details.html',
                  {'receipt': receipt, 'patients': patients})


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_all_sales_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    sales = models.Sale.objects.all().order_by('-id')
    return render(request, 'hospital/employee/pharmacy_all_sales.html', {'employee': employee, 'sales': sales})


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def pharmacy_cancel_sale_view(request, sale_id):
    sale = models.Sale.objects.get(id=sale_id)
    patient = models.Patient.objects.all().get(id=sale.patientId)
    patient.pendingMedicalCharge -= sale.totalPrice
    patient.save()
    sale.delete()
    return HttpResponseRedirect('pharmacy-all-sales')


# --------------- LABORATORY ----------------------

@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def laboratory_dashboard_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    return render(request, 'hospital/employee/laboratory_dashboard.html', {'employee': employee})


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def laboratory_add_new_test_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    tests = models.LabTest.objects.all()
    testForm = forms.LabTestForm()
    myDict = {'tests': tests, 'testForm': testForm, 'employee': employee}
    if request.method == 'POST':
        testForm = forms.LabTestForm(request.POST)
        if testForm.is_valid():
            testForm.save()
            messages.success(request, "Test added successfully.")
            return HttpResponseRedirect('laboratory-tests')
        messages.error(request, "Error. Test adding failed. ")
    return render(request, 'hospital/employee/laboratory_tests.html', context=myDict)


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def laboratory_delete_test_view(request, pk):
    test = models.LabTest.objects.get(id=pk)
    test.delete()
    messages.success(request, "Test deleted successfully.")
    return redirect('laboratory-tests')

@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def laboratory_save_result_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    labForm = forms.LabForm()
    myDict = {'labForm': labForm, 'employee': employee}
    if request.method == 'POST':
        labForm = forms.LabForm(request.POST)
        if labForm.is_valid():
            labResult = labForm.save(commit=False)
            labResult.patientId = request.POST.get('patientId')
            labResult.patientName = models.Patient.objects.get(id=request.POST.get('patientId')).patientName
            labResult.testId = request.POST.get('testId')
            labResult.testName = models.LabTest.objects.get(id=request.POST.get('testId')).testName
            labResult.testResult = request.POST.get('testResult')
            patient = models.Patient.objects.get(id=request.POST.get('patientId'))
            testPrice = models.LabTest.objects.get(id=request.POST.get('testId')).testPrice
            patient.pendingLabTestCharge += testPrice

            labResult.save()
            patient.save()
            messages.success(request, "Test Result saved successfully.")
            return HttpResponseRedirect('reception-book-appointment')
        messages.error(request, "Error. Test result saving failed. ")
    return render(request, 'hospital/employee/laboratory_save_result.html', context=myDict)


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def laboratory_all_tests_view(request):
    employee = models.Employee.objects.get(user_id=request.user.id)
    tests = models.LabResult.objects.all().order_by('-id')
    return render(request, 'hospital/employee/laboratory_all_tests.html', {'employee': employee, 'tests': tests})


@login_required(login_url='userlogin')
@user_passes_test(is_employee)
def laboratory_receipt_details_view(request, receipt_id):
    patients = models.Patient.objects.all().filter(status=True)
    receipt = models.LabResult.objects.get(id=receipt_id)
    return render(request, 'hospital/employee/laboratory_receipt_details.html',
                  {'receipt': receipt, 'patients': patients})


# -----------------------------------------------------------------------------
# --------------for discharge patient bill (pdf) download and printing ------
# ---------------------------------------------------------------------------

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download_pdf_view(request, pk):
    dischargeDetails = models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict = {
        'patientName': dischargeDetails[0].patientName,
        'assignedDoctorName': dischargeDetails[0].assignedDoctorName,
        'address': dischargeDetails[0].address,
        'mobile': dischargeDetails[0].mobile,
        'admitDate': dischargeDetails[0].admitDate,
        'releaseDate': dischargeDetails[0].releaseDate,
        'daySpent': dischargeDetails[0].daySpent,
        'medicineCost': dischargeDetails[0].medicineCost,
        'labTestCost': dischargeDetails[0].labTestCost,
        'roomCharge': dischargeDetails[0].roomCharge,
        'doctorFee': dischargeDetails[0].doctorFee,
        'OtherCharge': dischargeDetails[0].OtherCharge,
        'total': dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/admin/download_bill.html', dict)


# ---------------------------------------------------------------------------------
# ------------------------ ABOUT US VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request, 'hospital/aboutus.html')

