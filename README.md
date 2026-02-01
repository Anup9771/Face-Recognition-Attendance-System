# 🎓 Smart Face Recognition Attendance System

## 📋 Project Overview
A web-based attendance management system using facial recognition technology built with Flask, OpenCV, and MediaPipe library. This system automates the attendance marking process by detecting and recognizing student faces in real-time.

**✨ Now Dlib-Free - Deploy on Free Hosting Platforms!**

## ✨ Features

### Core Features
- 🔐 **User Authentication** - Secure login/register system
- 👤 **Student Management** - Add, Edit, Delete student records
- 📸 **Face Recognition** - Real-time face detection and recognition
- 📊 **Attendance Tracking** - Automatic attendance marking (once per day)
- 📅 **Date Filter** - View attendance by specific dates
- 🗑️ **Secure Delete** - Password-protected attendance deletion
- 👨‍💻 **Developer Info** - Password-protected developer details management
- ❓ **Help Desk** - Comprehensive user guide

### Technical Features
- Glass morphism UI design
- Auto-hiding flash messages
- Responsive navigation bar
- Dashboard statistics
- Face detection notifications
- Enter key to exit face recognition

## 🛠️ Technologies Used

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **Flask-Login** - User session management
- **Werkzeug** - Password hashing

### Face Recognition
- **OpenCV (cv2)** - Computer vision
- **MediaPipe** - Google's face detection and recognition
- **Scikit-learn** - Face matching algorithms
- **NumPy** - Numerical operations

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (Glass morphism, Gradients)
- **JavaScript** - Interactivity

### Database
- **SQLite** - Lightweight database

## 📁 Project Structure
```
FaceRecognitionApp/
│
├── app.py                          # Main application file
├── models.py                       # Database models
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── dashboard.html             # Dashboard
│   ├── student_register.html      # Student registration
│   ├── edit_student.html          # Edit student
│   ├── attendence.html            # Attendance records
│   ├── face_recognition.html      # Face recognition page
│   ├── developer.html             # Developer info
│   └── helpdesk.html              # Help desk
│
├── static/                         # Static files
│   ├── styles.css                 # Main stylesheet
│   └── images/                    # Image storage
│       ├── student_photos/        # Student photos
│       ├── developer_photos/      # Developer photos
│       └── collage_bg.jpg/        # Background images
│
└── instance/                       # Instance folder
    └── face_recognition.db        # SQLite database
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Webcam/Camera
- pip (Python package manager)

### Step 1: Clone/Download Project
```bash
cd FaceRecognitionApp
```

### Step 2: Install Dependencies
```bash
# Test setup first (optional)
python test_setup.py

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run Application
```bash
python app.py
```

### Step 4: Access Application
Open browser and go to: `http://localhost:5000`

## 📦 Dependencies
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
opencv-python-headless==4.8.1.78
mediapipe==0.10.9
scikit-learn==1.3.2
numpy==1.24.3
gunicorn==21.2.0
```

## ✨ MediaPipe Advantages
- ✅ **No Dlib** - Easy deployment on free hosting
- ✅ **Faster** - Optimized performance
- ✅ **Smaller** - ~50MB vs ~100MB
- ✅ **Free Deploy Ready** - Render, Railway, PythonAnywhere

## 👥 Database Models

### User Model
- id (Primary Key)
- username (Unique)
- password (Hashed)

### Student Model
- id (Primary Key)
- name
- roll_no
- class_name
- photo (filename)

### Attendance Model
- id (Primary Key)
- student_id (Foreign Key)
- time (DateTime)

### Developer Model
- id (Primary Key)
- name
- email
- contact
- photo (filename)

## 🔑 Default Credentials

### Admin Passwords
- **Attendance Delete Password:** `admin@123`
- **Developer Edit Password:** `dev@123`

### First Time Setup
1. Register a new user account
2. Login with credentials
3. Add students with photos
4. Start face recognition

## 📖 User Guide

### For Students
1. Admin will register you with photo, name, roll number, and class
2. Stand in front of camera during attendance
3. Ensure face is clearly visible and well-lit
4. Green box with name = attendance marked successfully

### For Admin/Teachers
1. **Register Student:** Navigate to Register → Fill details → Upload photo
2. **Start Attendance:** Click Face Recognition in navbar
3. **View Records:** Go to Attendance page
4. **Filter by Date:** Use date picker on attendance page
5. **Edit Student:** Click Edit button on dashboard
6. **Delete Records:** Use delete button (requires password)

## 🎨 UI Features
- Dark theme with glass morphism
- Gradient buttons and navigation
- Smooth animations and transitions
- Auto-hiding notifications
- Responsive design
- Professional color scheme

## 🔒 Security Features
- Password hashing (Werkzeug)
- Login required decorators
- Session management
- Password-protected deletions
- Secure file uploads
- SQL injection prevention (SQLAlchemy ORM)

## ⚙️ Configuration
Edit `app.py` for configuration:
```python
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///face_recognition.db'
app.config['UPLOAD_FOLDER'] = 'static/images/student_photos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
```

## 🐛 Troubleshooting

### Camera Not Working
- Check camera permissions in browser
- Ensure no other application is using camera
- Try different browser

### Face Not Detected
- Improve lighting
- Face camera directly
- Remove glasses/mask
- Stand 2-3 feet away

### Installation Issues
```bash
# For MediaPipe issues
pip install --upgrade pip
pip install mediapipe --no-cache-dir

# For OpenCV issues
pip install opencv-python-headless
```

## 🚀 Free Deployment Guide

This project can now be deployed on **FREE hosting platforms**!

### Recommended Platforms:
1. **Render.com** ⭐ - Best for Flask apps
2. **Railway.app** - Fast deployment  
3. **PythonAnywhere** - Python-specific
4. **Fly.io** - Good free tier

### Quick Deploy Steps:
1. Push code to GitHub
2. Connect to hosting platform
3. Auto-deploy with requirements.txt
4. Done! 🎉

**📖 Detailed Guide:** Check [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📊 Performance Optimization
- Processes every 3rd frame for better performance
- HOG model for faster face detection
- Tolerance set to 0.6 for accuracy
- One attendance per day per student

## 🎯 Future Enhancements
- Export attendance to Excel/CSV
- Email notifications
- Multiple photo support per student
- Attendance reports and analytics
- Bulk student upload
- Mobile responsive improvements

## 👨‍💻 Developer Information
**Project Type:** College Project  
**Technology Stack:** Flask + OpenCV + MediaPipe  
**Database:** SQLite  
**UI Framework:** Custom CSS (Glass Morphism)

## 📝 License
This project is created for educational purposes.

## 🙏 Acknowledgments
- Flask Documentation
- MediaPipe by Google
- OpenCV Community
- Stack Overflow Community

## 📞 Support
For issues or questions, refer to the Help Desk section in the application.

---
**Made with ❤️ for College Project Submission**
