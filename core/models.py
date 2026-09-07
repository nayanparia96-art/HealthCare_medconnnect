from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name} on {self.date}"

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Blood(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    quantity = models.IntegerField()  # in units
    hospital = models.CharField(max_length=100)  # or foreign key if hospitals model

    def __str__(self):
        return f"{self.group} - {self.quantity} units"


class Application(models.Model):
    """Model to store form submissions for various applications (job, internship, etc.)"""
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
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    position = models.CharField(max_length=200)
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPE_CHOICES, default='job')
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='applications/resumes/', blank=True, null=True)
    experience = models.TextField(help_text="Describe your relevant experience")
    skills = models.TextField(help_text="List your key skills")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_sent = models.BooleanField(default=False)

    @property
    def skills_list(self):
        if not self.skills:
            return []
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_application_type_display()}"