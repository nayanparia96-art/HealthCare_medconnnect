from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    """
    Form for submitting applications (job, internship, volunteer, partnership)
    """
    
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'phone', 'position', 
                  'application_type', 'cover_letter', 'experience', 'skills', 'resume']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'required': True,
                'pattern': r'[0-9\-\+\s\(\)]*',
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Position you are applying for',
                'required': True
            }),
            'application_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a brief cover letter',
                'rows': 5,
                'required': True
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your relevant experience',
                'rows': 4,
                'required': True
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'List your key skills (comma-separated)',
                'rows': 3,
                'required': True
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'position': 'Position',
            'application_type': 'Application Type',
            'cover_letter': 'Cover Letter',
            'experience': 'Experience',
            'skills': 'Skills',
            'resume': 'Resume (Optional - PDF, DOC, DOCX)',
        }
    
    def clean_email(self):
        """Validate email format"""
        email = self.cleaned_data.get('email')
        if email and '@' not in email:
            raise forms.ValidationError("Please provide a valid email address.")
        return email
    
    def clean_phone(self):
        """Validate phone number"""
        phone = self.cleaned_data.get('phone')
        if phone and len(phone.replace('-', '').replace(' ', '').replace('+', '').replace('(', '').replace(')', '')) < 10:
            raise forms.ValidationError("Please provide a valid phone number (at least 10 digits).")
        return phone
    
    def clean_resume(self):
        """Validate resume file size"""
        resume = self.cleaned_data.get('resume')
        if resume:
            if resume.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Resume file size must not exceed 5MB.")
        return resume
