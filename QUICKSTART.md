# Quick Start Guide - Health Care System

## 🚀 Get Started in 5 Minutes

### 1. Activate Virtual Environment
```powershell
cd C:\Users\user\Desktop\Health-care
.\.venv\Scripts\Activate.ps1
```

### 2. Start the Server
```bash
python manage.py runserver
```

### 3. Open in Browser
Visit: **http://localhost:8000**

### 4. Access Admin Panel
Visit: **http://localhost:8000/admin**

---

## 📝 Add Sample Data

### Via Django Shell
```bash
python manage.py shell
```

Then run:
```python
from core.models import Doctor, Medicine, Blood

# Add a doctor
Doctor.objects.create(
    name="Dr. John Smith",
    specialty="Cardiology",
    email="john@example.com",
    phone="555-0123"
)

# Add a medicine
Medicine.objects.create(
    name="Aspirin",
    description="Pain reliever",
    price=5.99,
    stock=100
)

# Add blood
Blood.objects.create(
    group="O+",
    quantity=50,
    hospital="City Hospital"
)

exit()
```

### Via Admin Panel
1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Click on each model and add data

---

## 🔗 Available Routes

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/login/` | User login |
| `/register/` | User registration |
| `/doctors/` | Browse doctors |
| `/patients/` | View patients |
| `/medicines/` | Browse medicines |
| `/blood/` | Blood bank |
| `/book/` | Book appointment |
| `/admin/` | Admin panel |

---

## 🎯 Key Features to Try

### 1. Register New Account
- Click "Register"
- Fill in details
- Create account

### 2. Login
- Click "Login"
- Enter credentials
- Access dashboard

### 3. Browse Doctors
- Click "Doctors" in navigation
- View all available doctors
- Click "Book Appointment" to schedule

### 4. Book Appointment
- Select doctor
- Enter patient details
- Choose date & time
- Submit booking

### 5. View Medicines
- Browse available medicines
- See prices and stock
- Order medicines

### 6. Check Blood Availability
- View blood groups
- See available units
- Request delivery if needed

---

## 🛠️ Common Tasks

### Create Admin Account
```bash
python manage.py createsuperuser
```

### View Database Records
```bash
python manage.py shell
# Then:
from core.models import Doctor
Doctor.objects.all()
```

### Reset Everything
```bash
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

### Check for Errors
```bash
python manage.py check
```

---

## 📱 Mobile Testing

The site is fully responsive. Test on mobile by:
1. Open browser DevTools (F12)
2. Click device toolbar icon (top-left)
3. Select mobile device
4. Reload page

---

## 🎨 Customize

### Change Colors
Edit `core/static/core/style.css`:
- Scroll to `:root` section
- Modify color variables
- Save and refresh

### Change Logo/Text
Edit `core/templates/core/base.html`:
- Find the logo section
- Replace text/icon
- Update navigation links

### Add New Pages
1. Create HTML file in `core/templates/core/`
2. Add view function in `core/views.py`
3. Add URL route in `core/urls.py`
4. Add navigation link in `base.html`

---

## ⚠️ Important Notes

- Always activate virtual environment before working
- Server must be running to access the site
- Admin panel requires superuser login
- Database changes need migrations
- Static files update automatically in dev mode

---

## 🆘 Need Help?

### Server won't start?
- Check if port 8000 is free
- Try: `python manage.py runserver 8001`

### Database errors?
- Run: `python manage.py migrate`

### Static files not loading?
- Hard refresh browser (Ctrl+Shift+R)

### Form errors?
- Check browser console (F12 > Console)
- Check terminal for error messages

---

## 📚 Next Steps

1. **Explore Admin Panel** - Add real data
2. **Test Features** - Try all functionality
3. **Customize** - Change colors, text, layout
4. **Deploy** - Take to production
5. **Enhance** - Add new features

---

**Happy Coding! 💻**
