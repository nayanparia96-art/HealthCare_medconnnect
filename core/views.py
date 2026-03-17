from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient, Appointment, Medicine, Blood, Application
from .forms import ApplicationForm
from django import forms
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
import io
import numpy as np
from PIL import Image

# TensorFlow is optional at import-time to avoid breaking site if not installed.
try:
    import tensorflow as tf
except Exception:
    tf = None

# Lazy-loaded model reference
MODEL = None

def load_cancer_model():
    global MODEL
    if MODEL is not None:
        return MODEL
    if tf is None:
        return None
    model_path = os.path.join(settings.BASE_DIR, 'model', 'cancer_model.h5')
    if not os.path.exists(model_path):
        return None
    MODEL = tf.keras.models.load_model(model_path)
    return MODEL

def preprocess_image_file(file_obj, target_size=(224, 224)):
    image = Image.open(file_obj).convert('RGB')
    image = image.resize(target_size)
    arr = np.array(image).astype('float32') / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

def get_prediction(image_file):
    model = load_cancer_model()
    if model is None:
        return None, 'model-missing'
    img_arr = preprocess_image_file(image_file)
    preds = model.predict(img_arr)
    # handle different output shapes
    try:
        prob = float(preds.ravel()[0])
    except Exception:
        prob = float(np.max(preds))
    return prob, None

class AppointmentForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Select Doctor")
    patient_name = forms.CharField(max_length=100, label="Patient Name")
    patient_email = forms.EmailField(label="Patient Email")
    patient_phone = forms.CharField(max_length=15, label="Patient Phone")
    patient_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Date of Birth")
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label="Appointment Date")
    notes = forms.CharField(widget=forms.Textarea, required=False, label="Notes")

def home(request):
    context = {}
    if request.user.is_authenticated:
        context['welcome_message'] = f"Welcome back, {request.user.username}!"
    return render(request, 'core/home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'core/register.html')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data['doctor']
            patient_name = form.cleaned_data['patient_name']
            patient_email = form.cleaned_data['patient_email']
            patient_phone = form.cleaned_data['patient_phone']
            patient_date_of_birth = form.cleaned_data.get('patient_date_of_birth')
            date = form.cleaned_data['date']
            notes = form.cleaned_data['notes']
            
            # Get or create patient
            patient, created = Patient.objects.get_or_create(
                email=patient_email,
                defaults={'name': patient_name, 'phone': patient_phone, 'date_of_birth': patient_date_of_birth}
            )
            if not created:
                # Update name, phone, and date_of_birth if different
                patient.name = patient_name
                patient.phone = patient_phone
                if patient_date_of_birth:
                    patient.date_of_birth = patient_date_of_birth
                patient.save()
            
            # Create appointment
            Appointment.objects.create(doctor=doctor, patient=patient, date=date, notes=notes)
            messages.success(request, 'Appointment booked successfully!')
            return redirect('home')
    else:
        form = AppointmentForm()
    return render(request, 'core/book_appointment.html', {'form': form})

@login_required
def doctors_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'core/doctors.html', {'doctors': doctors})

@login_required
def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'core/patients.html', {'patients': patients})

@login_required
def medicines_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'core/medicines.html', {'medicines': medicines})

@login_required
def blood_list(request):
    bloods = Blood.objects.all()
    availability = {}
    for blood in bloods:
        if blood.group in availability:
            availability[blood.group] += blood.quantity
        else:
            availability[blood.group] = blood.quantity
    # Add all groups with 0 if not present
    all_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    for group in all_groups:
        if group not in availability:
            availability[group] = 0
    return render(request, 'core/blood.html', {'availability': availability})

@login_required
def my_appointments(request):
    # For demo, show all appointments. In real app, filter by user
    appointments = Appointment.objects.all().order_by('-date')
    return render(request, 'core/my_appointments.html', {'appointments': appointments})

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Update user profile
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'core/profile.html')

def feedback_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Here you can save to database or send email
        messages.success(request, 'Thank you for your feedback!')
        return redirect('home')
    return render(request, 'core/feedback.html')

def ambulance_view(request):
    return render(request, 'core/ambulance.html')


def cancer_detector(request):
    error = None
    result = None
    probability = None
    advice = None
    if request.method == 'POST':
        uploaded = request.FILES.get('image')
        if not uploaded:
            error = 'Please upload an image file.'
        else:
            try:
                # Read into BytesIO so PIL can open it
                img_bytes = io.BytesIO(uploaded.read())
                prob, err = get_prediction(img_bytes)
                if err == 'model-missing':
                    error = 'AI model not found. Please place cancer_model.h5 in the project /model folder.'
                else:
                    probability = round(prob * 100, 2)
                    detected = prob >= 0.5
                    if detected:
                        result = 'Cancer Detected'
                        advice = {
                            'title': 'Recommended Actions',
                            'items': [
                                'Consult a qualified medical professional or oncologist immediately.',
                                'Avoid self-medication; seek clinical diagnostic tests (biopsy, imaging).',
                                'Bring previous medical reports to your consultation.'
                            ]
                        }
                    else:
                        result = 'No Cancer Detected'
                        advice = {
                            'title': 'Prevention Tips',
                            'items': [
                                'Maintain a healthy lifestyle: balanced diet and regular exercise.',
                                'Schedule regular screenings as recommended for your age and risk factors.',
                                'Protect skin from excessive sun exposure and follow safety guidelines.'
                            ]
                        }
            except Exception as e:
                error = f'Error processing image: {str(e)}'

    return render(request, 'core/cancer_detector.html', {
        'error': error,
        'result': result,
        'probability': probability,
        'advice': advice,
    })


def cancer_result(request):
    # This view can display results if you want a separate page; currently handled in cancer_detector template.
    return redirect('cancer_detector')


# ===============================================
# APPLICATION FORM SUBMISSION VIEWS
# ===============================================

def application_form(request):
    """
    View to handle application form submissions with automatic email confirmation.
    Supports job, internship, volunteer, and partnership applications.
    """
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the application to database
            application = form.save(commit=False)
            application.save()
            
            # Send confirmation email
            send_application_confirmation_email(application)
            
            # Mark email as sent
            application.email_sent = True
            application.save()
            
            # Display success message
            messages.success(request, 'Your application has been received successfully! Check your email for confirmation.')
            return redirect('application_success')
        else:
            # Form has errors, display them
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ApplicationForm()
    
    context = {
        'form': form,
        'page_title': 'Application Form - MEDCONNECT'
    }
    return render(request, 'core/application_form.html', context)


def send_application_confirmation_email(application):
    """
    Send confirmation email to applicant when form is submitted.
    
    Args:
        application: Application model instance
    """
    try:
        subject = 'Application Received - MEDCONNECT'
        
        # Email context
        context = {
            'first_name': application.first_name,
            'last_name': application.last_name,
            'position': application.position,
            'application_type': application.get_application_type_display(),
            'email': application.email,
            'site_name': 'MEDCONNECT',
        }
        
        # Render email template
        html_message = render_to_string('core/email/application_confirmation.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"✓ Confirmation email sent to {application.email}")
        return True
        
    except Exception as e:
        print(f"✗ Error sending email to {application.email}: {str(e)}")
        return False


def application_success(request):
    """
    Display success page after application submission.
    """
    context = {
        'page_title': 'Application Submitted - MEDCONNECT',
        'message': 'Thank you for your application!'
    }
    return render(request, 'core/application_success.html', context)


def applications_list(request):
    """
    Admin view to list all applications (login required).
    """
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('home')
    
    applications = Application.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Filter by application type if provided
    type_filter = request.GET.get('type')
    if type_filter:
        applications = applications.filter(application_type=type_filter)
    
    context = {
        'applications': applications,
        'page_title': 'All Applications - MEDCONNECT',
        'status_choices': Application.STATUS_CHOICES,
        'type_choices': Application.APPLICATION_TYPE_CHOICES,
    }
    return render(request, 'core/applications_list.html', context)


def application_detail(request, id):
    """
    View application details and update status (login required).
    """
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('home')
    
    try:
        application = Application.objects.get(id=id)
    except Application.DoesNotExist:
        messages.error(request, 'Application not found.')
        return redirect('applications_list')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {new_status}.')
    
    context = {
        'application': application,
        'page_title': f'Application Detail - MEDCONNECT',
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'core/application_detail.html', context)
