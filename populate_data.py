import os
import django
from datetime import date, datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')
django.setup()

from core.models import Doctor, Patient, Medicine, Blood, Appointment

def populate_data():
    # Clear existing data
    Doctor.objects.all().delete()
    Patient.objects.all().delete()
    Medicine.objects.all().delete()
    Blood.objects.all().delete()
    Appointment.objects.all().delete()

    # Add Doctors
    doctors_data = [
        {'name': 'Mousam Das', 'specialty': 'Cardiology', 'email': 'mousam.das@hospital.com', 'phone': '9382029893'},
        {'name': 'Saikat Prdhan', 'specialty': 'Dermatology', 'email': 'saikat.prdhan@hospital.com', 'phone': '8436654974'},
        {'name': 'Dip Jana', 'specialty': 'Orthopedics', 'email': 'dip.jana@hospital.com', 'phone': '8001406486'},
        {'name': 'Subhadip Barik', 'specialty': 'Gynecology', 'email': 'subhadip.barik@hospital.com', 'phone': '9046341544'},
        {'name': 'Azhar Mehumad Molla', 'specialty': 'Neurology', 'email': 'azhar.molla@hospital.com', 'phone': '7679923018'},
    ]

    doctors = []
    for data in doctors_data:
        doctor = Doctor.objects.create(**data)
        doctors.append(doctor)
        print(f"Created doctor: {doctor.name}")

    # Add Patients
    patients_data = [
        {'name': 'Ujjwal Karmokar', 'email': 'ujjwal.karmokar@gmail.com', 'phone': '9876543215', 'date_of_birth': date(1985, 5, 15)},
        {'name': 'Jotirmoy Mondol', 'email': 'jotirmoy.mondol@gmail.com', 'phone': '9876543216', 'date_of_birth': date(1990, 8, 22)},
        {'name': 'Souhardya Guien', 'email': 'souhardya.guien@gmail.com', 'phone': '9876543217', 'date_of_birth': date(1978, 12, 10)},
        {'name': 'Animesh Bag', 'email': 'animesh.bag@gmail.com', 'phone': '9876543218', 'date_of_birth': date(1995, 3, 5)},
        {'name': 'Vikram Singh', 'email': 'vikram.singh@gmail.com', 'phone': '9876543219', 'date_of_birth': date(1982, 7, 18)},
    ]

    patients = []
    for data in patients_data:
        patient = Patient.objects.create(**data)
        patients.append(patient)
        print(f"Created patient: {patient.name}")

    # Add Medicines
    medicines_data = [
        {'name': 'Paracetamol', 'description': 'Pain relief and fever reducer', 'price': 25.00, 'stock': 100},
        {'name': 'Amoxicillin', 'description': 'Antibiotic for bacterial infections', 'price': 45.00, 'stock': 50},
        {'name': 'Ibuprofen', 'description': 'Anti-inflammatory pain reliever', 'price': 30.00, 'stock': 75},
        {'name': 'Aspirin', 'description': 'Blood thinner and pain reliever', 'price': 20.00, 'stock': 80},
        {'name': 'Cetirizine', 'description': 'Antihistamine for allergies', 'price': 15.00, 'stock': 60},
        {'name': 'Omeprazole', 'description': 'Acid reflux medication', 'price': 40.00, 'stock': 40},
    ]

    for data in medicines_data:
        medicine = Medicine.objects.create(**data)
        print(f"Created medicine: {medicine.name}")

    # Add Blood
    blood_data = [
        {'group': 'A+', 'quantity': 10, 'hospital': 'City Hospital'},
        {'group': 'A-', 'quantity': 5, 'hospital': 'City Hospital'},
        {'group': 'B+', 'quantity': 8, 'hospital': 'City Hospital'},
        {'group': 'B-', 'quantity': 3, 'hospital': 'City Hospital'},
        {'group': 'AB+', 'quantity': 4, 'hospital': 'City Hospital'},
        {'group': 'AB-', 'quantity': 2, 'hospital': 'City Hospital'},
        {'group': 'O+', 'quantity': 15, 'hospital': 'City Hospital'},
        {'group': 'O-', 'quantity': 6, 'hospital': 'City Hospital'},
    ]

    for data in blood_data:
        blood = Blood.objects.create(**data)
        print(f"Created blood: {blood.group} - {blood.quantity} units")

    # Add Appointments
    appointments_data = [
        {'doctor': doctors[0], 'patient': patients[0], 'date': datetime(2026, 2, 5, 10, 0), 'notes': 'Regular checkup'},
        {'doctor': doctors[1], 'patient': patients[1], 'date': datetime(2026, 2, 6, 14, 30), 'notes': 'Skin consultation'},
        {'doctor': doctors[2], 'patient': patients[2], 'date': datetime(2026, 2, 7, 11, 15), 'notes': 'Knee pain'},
        {'doctor': doctors[3], 'patient': patients[3], 'date': datetime(2026, 2, 8, 9, 45), 'notes': 'Prenatal checkup'},
        {'doctor': doctors[4], 'patient': patients[4], 'date': datetime(2026, 2, 9, 16, 0), 'notes': 'Headache consultation'},
    ]

    for data in appointments_data:
        appointment = Appointment.objects.create(**data)
        print(f"Created appointment: {appointment}")

    print("Sample data populated successfully!")

if __name__ == '__main__':
    populate_data()