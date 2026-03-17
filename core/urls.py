from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('doctors/', views.doctors_list, name='doctors'),
    path('patients/', views.patients_list, name='patients'),
    path('medicines/', views.medicines_list, name='medicines'),
    path('blood/', views.blood_list, name='blood'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('profile/', views.profile_view, name='profile'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('ambulance/', views.ambulance_view, name='ambulance'),
    path('cancer-detector/', views.cancer_detector, name='cancer_detector'),
    path('cancer-result/', views.cancer_result, name='cancer_result'),
    
    # Application Form URLs
    path('apply/', views.application_form, name='application_form'),
    path('application-success/', views.application_success, name='application_success'),
    path('applications/', views.applications_list, name='applications_list'),
    path('applications/<int:id>/', views.application_detail, name='application_detail'),
]
