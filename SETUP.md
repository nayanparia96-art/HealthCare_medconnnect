# Setup Instructions for Health Care System

## ✅ Complete Setup Checklist

### Prerequisites Check
- [ ] Python 3.8+ installed: `python --version`
- [ ] pip installed: `pip --version`
- [ ] Git installed (optional): `git --version`

### Initial Setup (One-Time)

#### Step 1: Navigate to Project
```bash
cd C:\Users\user\Desktop\Health-care
```

#### Step 2: Create & Activate Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (Windows Command Prompt)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate
```

#### Step 3: Install Django
```bash
pip install django
```

Verify installation:
```bash
django-admin --version
```

#### Step 4: Setup Database
```bash
python manage.py migrate
```

Expected output: "No migrations to apply."

#### Step 5: Create Admin Account
```bash
python manage.py createsuperuser
```

Follow prompts:
- Username: `admin`
- Email: `admin@example.com`
- Password: (enter secure password)
- Password (again): (confirm password)

#### Step 6: Collect Static Files (Optional)
```bash
python manage.py collectstatic --noinput
```

---

## 🚀 Running the Application

### Every Time You Want to Use the System

#### 1. Open Terminal/PowerShell
Navigate to project folder:
```bash
cd C:\Users\user\Desktop\Health-care
```

#### 2. Activate Virtual Environment
```bash
# PowerShell
.\.venv\Scripts\Activate.ps1

# Command Prompt
.venv\Scripts\activate.bat
```

You should see `(.venv)` at the start of your command line.

#### 3. Start Django Server
```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

#### 4. Open in Browser
Visit: **http://localhost:8000**

#### 5. Access Admin Panel (Optional)
Visit: **http://localhost:8000/admin**
- Username: `admin`
- Password: (your password from Step 5)

---

## 📊 Add Sample Data

### Option 1: Via Admin Panel (Recommended for Beginners)

1. Go to http://localhost:8000/admin
2. Login with admin credentials
3. Click "Doctors" → "Add Doctor"
   - Name: Dr. John Smith
   - Specialty: Cardiology
   - Email: john@hospital.com
   - Phone: 555-0123
4. Click "Medicines" → "Add Medicine"
   - Name: Aspirin
   - Description: Pain reliever
   - Price: 5.99
   - Stock: 100
5. Click "Bloods" → "Add Blood"
   - Group: O+
   - Quantity: 50
   - Hospital: City Hospital

### Option 2: Via Django Shell

```bash
python manage.py shell
```

Then type these commands:
```python
from core.models import Doctor, Medicine, Blood

# Add Doctor
Doctor.objects.create(
    name="Dr. Sarah Johnson",
    specialty="Pediatrics",
    email="sarah@hospital.com",
    phone="555-0456"
)

# Add Medicine
Medicine.objects.create(
    name="Ibuprofen",
    description="Anti-inflammatory",
    price=4.99,
    stock=150
)

# Add Blood
Blood.objects.create(
    group="A+",
    quantity=75,
    hospital="State Hospital"
)

# View all doctors
print("Doctors:", Doctor.objects.count())

# Exit
exit()
```

---

## 🧪 Testing the System

### User Registration
1. Click "Register"
2. Choose username: `testuser`
3. Email: `test@example.com`
4. Password: `TestPass123`
5. Submit

### User Login
1. Click "Login"
2. Username: `testuser`
3. Password: `TestPass123`
4. Submit

### Book Appointment
1. Click "Book Appointment"
2. Select a doctor
3. Enter patient details
4. Choose appointment date & time
5. Submit

---

## 🛠️ Maintenance Commands

### Check System Status
```bash
python manage.py check
```

### View Database Records
```bash
python manage.py shell
# Then execute Python commands
```

### Create Database Backup
```bash
# Windows
copy db.sqlite3 db.sqlite3.backup
```

### Reset Database (⚠️ Deletes all data!)
```bash
python manage.py flush
python manage.py migrate
```

### Install Additional Packages
```bash
pip install [package-name]
pip freeze > requirements.txt
```

---

## 🔧 Troubleshooting

### Issue: Port 8000 Already in Use
**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID [PID] /F
```

### Issue: Virtual Environment Not Activating
**Solution:**
```bash
# Try this instead
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

### Issue: Django Not Found
**Solution:**
```bash
# Make sure virtual environment is activated
pip install django

# Verify
python -c "import django; print(django.get_version())"
```

### Issue: Static Files Not Loading
**Solution:**
1. Hard refresh browser: `Ctrl + Shift + R`
2. Clear browser cache
3. Run: `python manage.py collectstatic --clear --no-input`

### Issue: Database Locked
**Solution:**
```bash
# Restart Django server
# Stop the server (Ctrl+C)
# Run: python manage.py migrate
# Start server again
```

### Issue: 404 Page Not Found
**Solution:**
1. Check URL spelling
2. Verify URL is in `core/urls.py`
3. Check view function exists in `core/views.py`
4. Restart server

---

## 📦 File Structure Review

Your project should have:
```
Health-care/
├── .venv/                 ✓ Virtual environment
├── core/
│   ├── templates/         ✓ HTML files
│   ├── static/            ✓ CSS, JS files
│   ├── migrations/        ✓ Database migrations
│   ├── models.py          ✓ Database models
│   ├── views.py           ✓ View functions
│   └── urls.py            ✓ URL routing
├── healthcare/
│   ├── settings.py        ✓ Configuration
│   ├── urls.py            ✓ Main URL routing
│   └── wsgi.py            ✓ WSGI config
├── db.sqlite3             ✓ Database
├── manage.py              ✓ Django management
├── README.md              ✓ Documentation
└── QUICKSTART.md          ✓ Quick guide
```

---

## 🎓 Learning Resources

### Django Documentation
- Official: https://docs.djangoproject.com/
- Getting Started: https://www.djangoproject.com/start/

### HTML/CSS Resources
- MDN Web Docs: https://developer.mozilla.org/
- W3Schools: https://www.w3schools.com/

### Python Learning
- Python.org: https://python.org
- Real Python: https://realpython.com/

---

## 🚀 Next Steps After Setup

1. **Explore Admin Panel** - Add real data
2. **Test All Features** - Try registration, login, booking
3. **Customize Design** - Change colors in CSS
4. **Add More Data** - Build realistic test data
5. **Read Documentation** - Check README.md for details
6. **Deploy** - Take application live

---

## 📞 Support & Help

- Check console errors: Press F12 in browser
- Check terminal output for Django errors
- Read error messages carefully
- Search error message online
- Check Django documentation

---

## ✨ You're All Set!

Your Health Care System is ready to use! 🎉

Start the server and enjoy! 🚀

```bash
python manage.py runserver
```

Open: http://localhost:8000

---

**Happy coding!** 💻❤️
