# 📖 Complete Code Reference Guide

## 🎯 Quick Code Snippets

---

## 1️⃣ APPLICATION MODEL (models.py)

```python
class Application(models.Model):
    """Model to store form submissions for various applications"""
    
    APPLICATION_TYPE_CHOICES = [
        ('job', 'Job Application'),
        ('internship', 'Internship Application'),
        ('volunteer', 'Volunteer Application'),
        ('partnership', 'Partnership Application'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    # Application Details
    position = models.CharField(max_length=200)
    application_type = models.CharField(
        max_length=20,
        choices=APPLICATION_TYPE_CHOICES,
        default='job'
    )
    
    # Content
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='applications/resumes/', blank=True, null=True)
    experience = models.TextField(help_text="Describe your relevant experience")
    skills = models.TextField(help_text="List your key skills")
    
    # Status & Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_application_type_display()}"
```

---

## 2️⃣ APPLICATION FORM (forms.py)

```python
from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    """Form for submitting applications"""
    
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'phone', 'position', 
                  'application_type', 'cover_letter', 'experience', 'skills', 'resume']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'application_type': forms.Select(attrs={'class': 'form-select'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resume': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and '@' not in email:
            raise forms.ValidationError("Invalid email address")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        digits = phone.replace('-', '').replace(' ', '').replace('+', '').replace('(', '').replace(')', '')
        if phone and len(digits) < 10:
            raise forms.ValidationError("Phone must be at least 10 digits")
        return phone
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and resume.size > 5 * 1024 * 1024:  # 5MB
            raise forms.ValidationError("File size must not exceed 5MB")
        return resume
```

---

## 3️⃣ MAIN VIEW (views.py)

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Application
from .forms import ApplicationForm

def application_form(request):
    """Handle application form submissions"""
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save to database
            application = form.save(commit=False)
            application.save()
            
            # Send confirmation email
            send_application_confirmation_email(application)
            
            # Mark as sent
            application.email_sent = True
            application.save()
            
            messages.success(request, 'Application received! Check your email for confirmation.')
            return redirect('application_success')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ApplicationForm()
    
    return render(request, 'core/application_form.html', {'form': form})
```

---

## 4️⃣ EMAIL SENDER FUNCTION (views.py)

```python
def send_application_confirmation_email(application):
    """Send confirmation email to applicant"""
    try:
        subject = 'Application Received - MEDCONNECT'
        
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
        
        print(f"✓ Email sent to {application.email}")
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False
```

---

## 5️⃣ ADMIN VIEWS (views.py)

```python
def applications_list(request):
    """Admin list view"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    applications = Application.objects.all()
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        applications = applications.filter(application_type=type_filter)
    
    context = {
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES,
        'type_choices': Application.APPLICATION_TYPE_CHOICES,
    }
    return render(request, 'core/applications_list.html', context)


def application_detail(request, id):
    """Admin detail view"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    application = Application.objects.get(id=id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, 'Status updated')
    
    context = {
        'application': application,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'core/application_detail.html', context)
```

---

## 6️⃣ EMAIL CONFIGURATION (settings.py)

### Option 1: Console (Development - Default)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@medconnect.com'
SERVER_EMAIL = 'noreply@medconnect.com'
```

### Option 2: Gmail (Production)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # 16 chars from Google
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
SERVER_EMAIL = 'your-email@gmail.com'
```

### Option 3: SendGrid
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
DEFAULT_FROM_EMAIL = 'noreply@medconnect.com'
```

---

## 7️⃣ URL ROUTES (urls.py)

```python
from django.urls import path
from . import views

urlpatterns = [
    # ... existing routes ...
    
    # Application Form URLs
    path('apply/', views.application_form, name='application_form'),
    path('application-success/', views.application_success, name='application_success'),
    path('applications/', views.applications_list, name='applications_list'),
    path('applications/<int:id>/', views.application_detail, name='application_detail'),
]
```

---

## 8️⃣ KEY TEMPLATE TAGS

### In application_form.html
```html
{% load static %}
<!-- Access form fields -->
{{ form.first_name }}
{{ form.first_name.errors }}

<!-- CSRF protection -->
{% csrf_token %}

<!-- Form submission -->
<form method="POST" enctype="multipart/form-data">
    ...
</form>
```

### In applications_list.html
```html
<!-- Loop through applications -->
{% for app in applications %}
    {{ app.first_name }}
    {{ app.get_application_type_display }}  <!-- Display label, not value -->
    {{ app.created_at|date:"M d, Y" }}      <!-- Format date -->
{% endfor %}

<!-- Conditional display -->
{% if app.status == 'approved' %}
    <span>Approved</span>
{% endif %}
```

### In application_confirmation.html
```html
<!-- Context variables -->
Dear {{ first_name }},
Your application for {{ position }} has been received.
Application Type: {{ application_type }}
```

---

## 9️⃣ COMMON QUERIES

### Get all pending applications
```python
from core.models import Application
pending = Application.objects.filter(status='pending')
```

### Get applications for specific type
```python
jobs = Application.objects.filter(application_type='job')
```

### Count approved applications
```python
approved_count = Application.objects.filter(status='approved').count()
```

### Get applications submitted today
```python
from django.utils import timezone
today = timezone.now().date()
today_apps = Application.objects.filter(created_at__date=today)
```

### Get all emails from applications
```python
emails = Application.objects.values_list('email', flat=True)
# emails = ['test1@example.com', 'test2@example.com', ...]
```

### Get applications sorted by newest
```python
latest = Application.objects.all().order_by('-created_at')[:10]  # Last 10
```

### Update all pending to reviewed
```python
Application.objects.filter(status='pending').update(status='reviewed')
```

### Delete rejected applications older than 30 days
```python
from django.utils import timezone
from datetime import timedelta

cutoff_date = timezone.now() - timedelta(days=30)
Application.objects.filter(
    status='rejected',
    created_at__lt=cutoff_date
).delete()
```

---

## 🔟 MANUAL EMAIL SENDING

```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    subject='Hello!',
    message='This is the plain text message',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['user@example.com'],
    html_message='<p>This is <strong>HTML</strong> message</p>',
)
```

### Send to multiple recipients
```python
send_mail(
    subject='Newsletter',
    message='Monthly update',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['user1@example.com', 'user2@example.com', 'user3@example.com'],
)
```

### Send with attachment
```python
from django.core.mail import EmailMessage

email = EmailMessage(
    subject='Application Confirmation',
    body='See attached files',
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=['user@example.com']
)
email.attach_file('path/to/file.pdf')
email.send()
```

---

## 1️⃣1️⃣ DATABASE OPERATIONS

### Create new application
```python
from core.models import Application

app = Application.objects.create(
    first_name='John',
    last_name='Doe',
    email='john@example.com',
    phone='5551234567',
    position='Senior Doctor',
    application_type='job',
    cover_letter='I am interested...',
    experience='5 years',
    skills='Surgery, Patient Care'
)
```

### Update application status
```python
app = Application.objects.get(id=1)
app.status = 'approved'
app.save()
```

### Bulk update
```python
Application.objects.filter(
    application_type='internship'
).update(status='reviewed')
```

### Delete application
```python
app = Application.objects.get(id=1)
app.delete()
```

### Export to CSV
```python
import csv

with open('applications.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Email', 'Position', 'Status'])
    
    for app in Application.objects.all():
        writer.writerow([
            f"{app.first_name} {app.last_name}",
            app.email,
            app.position,
            app.status
        ])
```

---

## 1️⃣2️⃣ FORM VALIDATION EXAMPLES

```python
class ApplicationForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        
        # Validate email uniqueness (optional)
        if email and Application.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        
        return cleaned_data
    
    def clean_cover_letter(self):
        cover_letter = self.cleaned_data.get('cover_letter')
        if cover_letter and len(cover_letter) < 50:
            raise forms.ValidationError("Cover letter must be at least 50 characters")
        return cover_letter
```

---

## 1️⃣3️⃣ PAGINATION IN ADMIN LIST

```python
from django.core.paginator import Paginator

def applications_list(request):
    all_apps = Application.objects.all()
    paginator = Paginator(all_apps, 10)  # 10 apps per page
    page_number = request.GET.get('page')
    applications = paginator.get_page(page_number)
    
    context = {
        'applications': applications,
        'page_obj': applications,
    }
    return render(request, 'core/applications_list.html', context)
```

In template:
```html
{% if page_obj.has_other_pages %}
    <nav>
        {% if page_obj.has_previous %}
            <a href="?page=1">First</a>
            <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
        {% endif %}
        
        Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
        
        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">Next</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
        {% endif %}
    </nav>
{% endif %}
```

---

## 1️⃣4️⃣ USEFUL DECORATORS

```python
from django.contrib.auth.decorators import login_required, user_passes_test

# Require login
@login_required
def applications_list(request):
    ...

# Require staff
def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def applications_list(request):
    ...

# Custom decorator
def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

@staff_required
def applications_list(request):
    ...
```

---

## 1️⃣5️⃣ TROUBLESHOOTING CODE

```python
# Debug: Print form errors
form = ApplicationForm(request.POST)
if not form.is_valid():
    print("Form errors:", form.errors)
    print("Non-field errors:", form.non_field_errors())

# Debug: Check object exists
try:
    app = Application.objects.get(id=999)
except Application.DoesNotExist:
    print("Application not found!")

# Debug: Check email settings
from django.conf import settings
print("EMAIL_BACKEND:", settings.EMAIL_BACKEND)
print("DEFAULT_FROM_EMAIL:", settings.DEFAULT_FROM_EMAIL)

# Debug: Send test email
from django.core.mail import send_mail
result = send_mail(
    'Test',
    'Test message',
    settings.DEFAULT_FROM_EMAIL,
    ['test@example.com'],
)
print("Email sent:", result)  # 1 = success, 0 = failed
```

---

**Use this as a reference while coding!** 🚀

For detailed explanations, see `FORM_SUBMISSION_GUIDE.md`
