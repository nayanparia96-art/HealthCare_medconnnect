#!/usr/bin/env python
"""
Health Care System - URL Status Checker
Checks all pages to verify they are working correctly
"""

import os
import django
from django.test import Client
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')
django.setup()

# Initialize Django test client
client = Client()

# List of URLs to check
urls_to_check = {
    'Home': '/',
    'Login': '/login/',
    'Register': '/register/',
    'Doctors': '/doctors/',
    'Patients': '/patients/',
    'Medicines': '/medicines/',
    'Blood Bank': '/blood/',
    'Admin': '/admin/',
    'Book Appointment': '/book/',
}

print("\n" + "="*60)
print("🏥 HEALTH CARE SYSTEM - URL STATUS CHECKER")
print("="*60 + "\n")

passed = 0
failed = 0

for page_name, url in urls_to_check.items():
    try:
        response = client.get(url)
        status = response.status_code
        
        # Check if status is successful (200-299)
        if 200 <= status < 300:
            status_symbol = "✅"
            result = "WORKING"
            passed += 1
        elif status == 404:
            status_symbol = "❌"
            result = "NOT FOUND"
            failed += 1
        elif status == 302:
            status_symbol = "⚠️"
            result = "REDIRECT"
            passed += 1
        else:
            status_symbol = "⚠️"
            result = "ERROR"
            failed += 1
            
        print(f"{status_symbol} {page_name:20} | {url:20} | {status} - {result}")
        
    except Exception as e:
        print(f"❌ {page_name:20} | {url:20} | ERROR: {str(e)}")
        failed += 1

print("\n" + "="*60)
print(f"📊 SUMMARY: {passed} ✅ Working | {failed} ❌ Failed")
print("="*60)

if failed == 0:
    print("\n🎉 All pages are working correctly!")
else:
    print(f"\n⚠️  {failed} page(s) need attention")

print("\n💡 Remember to run: python manage.py runserver\n")
