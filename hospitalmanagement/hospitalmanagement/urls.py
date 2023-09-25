"""hospitalmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from hospital import views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('aboutus/', views.aboutus_view),

    path('userlogin', LoginView.as_view(template_name='hospital/userlogin.html', redirect_authenticated_user=True),
         name='userlogin'),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/userlogin.html'), name='logout'),
    path('signup', views.signup_view, name='signup'),

    # -------- For ADMIN ---------------

    path('adminsignup', views.admin_signup_view, name='adminsignup'),

    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    # Admin doctor
    path('admin-doctor', views.admin_doctor_view, name='admin-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view, name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view, name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view, name='reject-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view, name='admin-view-doctor'),
    path('admin-delete-doctor/<int:pk>', views.admin_delete_doctor_view, name='admin-delete-doctor'),
    path('admin-update-doctor/<int:pk>', views.admin_update_doctor_view, name='admin-update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view, name='admin-add-doctor'),
    # Admin Employee
    path('admin-employee', views.admin_employee_view, name='admin-employee'),
    path('admin-approve-employee', views.admin_approve_employee_view, name='admin-approve-employee'),
    path('approve-employee/<int:pk>', views.approve_employee_view, name='approve-employee'),
    path('reject-employee/<int:pk>', views.reject_employee_view, name='reject-employee'),
    path('admin-view-employee', views.admin_view_employee_view, name='admin-view-employee'),
    path('admin-delete-employee/<int:pk>', views.admin_delete_employee_view, name='admin-delete-employee'),
    path('admin-update-employee/<int:pk>', views.admin_update_employee_view, name='admin-update-employee'),
    path('admin-add-employee', views.admin_add_employee_view, name='admin-add-employee'),
    # Admin Patient
    path('admin-patient', views.admin_patient_view, name='admin-patient'),
    path('admin-admit-patient',views.admin_admit_patient_view, name='admin-admit-patient'),
    path('admin-add-patient', views.admin_add_patient_view, name='admin-add-patient'),
    path('admin-update-patient/<int:pk>', views.admin_update_patient_view, name='admin-update-patient'),
    path('admin-delete-patient/<int:pk>', views.admin_delete_patient_view, name='admin-delete-patient'),
    path('admin-discharged-patients',views.admin_discharged_patients_view, name='admin-discharged-patients'),

    path('admin-discharge-patient', views.admin_discharge_patient_view, name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view, name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view, name='download-pdf'),

    path('admin-delete-discharge-record/<int:pk>', views.admin_delete_discharge_record_view, name='admin-delete-discharge-record'),
    # Admin Appointment
    path('admin-appointment', views.admin_appointment_view, name='admin-appointment'),
    path('admin-book-appointment', views.admin_book_appointment_view, name='admin-book-appointment'),
    path('admin-update-appointment/<int:pk>', views.admin_update_appointment_view, name='admin-update-appointment'),
    path('admin-delete-appointment/<int:pk>', views.admin_delete_appointment_view, name='admin-delete-appointment'),
    # Admin Pharmacy
    path('admin-pharmacy', views.admin_pharmacy_view, name='admin-pharmacy'),
    path('admin-pharmacy-receipt-details/<int:receipt_id>', views.admin_pharmacy_receipt_details_view, name='admin-pharmacy-receipt-details'),

    # Admin Laboratory
    path('admin-laboratory', views.admin_laboratory_view, name='admin-laboratory'),
    path('admin-laboratory-receipt-details/<int:receipt_id>', views.admin_laboratory_receipt_details_view, name='admin-laboratory-receipt-details'),



    # -------- For DOCTOR ---------------

    path('doctorsignup', views.doctor_signup_view, name='doctorsignup'),
    path('doctor-dashboard', views.doctor_dashboard_view, name='doctor-dashboard'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view, name='approve-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view, name='delete-appointment'),

    path('doctor-patient', views.doctor_patient_view, name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view, name='doctor-view-patient'),
    path('doctor-view-discharged-patient', views.doctor_view_discharged_patient_view, name='doctor-view-discharged-patient'),

    # -------- For EMPLOYEE ---------------

    path('employeesignup', views.employee_signup_view, name='employeesignup'),

    path('reception-dashboard', views.reception_dashboard_view, name='reception-dashboard'),
    path('reception-admit-patient',views.reception_admit_patient_view, name='reception-admit-patient'),
    path('reception-add-patient', views.reception_add_patient_view, name='reception-add-patient'),
    path('reception-book-appointment', views.reception_book_appointment_view, name='reception-book-appointment'),
    path('reception-view-appointment', views.reception_view_appointment_view, name='reception-view-appointment'),
    path('reception-discharge-patients', views.reception_discharge_patients_view, name='reception-discharge-patients'),
    path('reception-discharge-patient/<int:pk>', views.reception_discharge_patient_view, name='reception-discharge-patient'),

    # ----- Pharmacy -------
    path('pharmacy-dashboard', views.pharmacy_dashboard_view, name='pharmacy-dashboard'),
    path('pharmacy-issue-to', views.pharmacy_issue_to_view, name='pharmacy-issue-to'),
    path('pharmacy-issue-to-patient', views.pharmacy_issue_to_patient_view, name='pharmacy-issue-to-patient'),
    path('pharmacy-sale-confirm', views.pharmacy_sale_confirm_view, name='pharmacy-sale-confirm'),
    path('pharmacy-product', views.pharmacy_product_view, name='pharmacy-product'),
    path('pharmacy-delete-product/<int:pk>', views.pharmacy_delete_product_view, name='pharmacy-delete-product'),
    path('pharmacy-add-new-product', views.pharmacy_add_new_product_view, name='pharmacy-add-new-product'),
    path('pharmacy-add-new-category', views.pharmacy_add_new_category_view, name='pharmacy-add-new-category'),
    path('pharmacy-delete-category', views.pharmacy_delete_category_view, name='pharmacy-delete-category'),
    path('pharmacy-add-to-stock', views.pharmacy_add_to_stock_view, name='pharmacy-to-stock'),
    path('pharmacy-receipts', views.pharmacy_receipts_view, name='pharmacy-receipts'),
    path('pharmacy-receipt-details/<int:receipt_id>', views.pharmacy_receipt_details_view, name='pharmacy-receipt-details'),
    path('pharmacy-all-sales', views.pharmacy_all_sales_view, name='pharmacy-all-sales'),


    path('laboratory-dashboard', views.laboratory_dashboard_view, name='laboratory-dashboard'),
    path('laboratory-tests', views.laboratory_add_new_test_view, name='laboratory-tests'),
    path('laboratory-delete-test/<int:pk>',views.laboratory_delete_test_view, name='laboratory-delete-test'),
    path('laboratory-save-result', views.laboratory_save_result_view, name='laboratory-save-result'),
    path('laboratory-all-tests', views.laboratory_all_tests_view, name='laboratory-all-tests'),
    path('laboratory-receipt-details/<int:receipt_id>', views.laboratory_receipt_details_view, name='laboratory-receipt-details'),
]

if (settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)