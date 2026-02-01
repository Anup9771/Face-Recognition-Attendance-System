import os
import datetime
import numpy as np
import cv2
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Student, Attendance, Developer
from face_utils import FaceRecognizer

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Anup@123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///face_recognition.db'
app.config['UPLOAD_FOLDER'] = 'static/images/student_photos'
app.config['DEVELOPER_FOLDER'] = 'static/images/developer_photos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DEVELOPER_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid username or password!")
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Fill both username and password!")
            return render_template("register.html")
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!")
            return render_template("register.html")
        hashed_pass = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        flash("User registered successfully! Please login.")
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

@app.route('/student_register', methods=["GET","POST"])
@login_required
def student_register():
    if request.method=="POST":
        name = request.form.get('name')
        roll_no = request.form.get('roll_no')
        class_name = request.form.get('class_name')
        photo = request.files.get('photo')
        
        if not name or not roll_no or not class_name:
            flash("All fields are required!")
            return render_template('student_register.html')
        
        if photo and allowed_file(photo.filename):
            try:
                filename = secure_filename(photo.filename)
                unique_filename = f"{roll_no}_{filename}"
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                new_student = Student(name=name, roll_no=roll_no, class_name=class_name, photo=unique_filename)
                db.session.add(new_student)
                db.session.commit()
                flash("Student Registered!")
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f"Error: {str(e)}")
        else:
            flash("Upload valid photo (jpg, jpeg, png only)!")
    return render_template('student_register.html')

@app.route('/developer', methods=["GET", "POST"])
@login_required
def developer():
    dev = Developer.query.first()
    if request.method=="POST":
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        photo = request.files.get('photo')
        
        if photo and allowed_file(photo.filename):
            try:
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config['DEVELOPER_FOLDER'], filename))
                if dev:
                    dev.name = name
                    dev.email = email
                    dev.contact = contact
                    dev.photo = filename
                else:
                    dev = Developer(name=name, email=email, contact=contact, photo=filename)
                    db.session.add(dev)
                db.session.commit()
                flash("Developer Details Updated!")
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f"Error: {str(e)}")
        else:
            flash("Upload valid photo!")
    return render_template('developer.html', dev=dev)

@app.route('/helpdesk')
@login_required
def helpdesk():
    dev = Developer.query.first()
    return render_template('helpdesk.html', dev=dev)

def load_known_faces(recognizer):
    known_encodings = []
    known_ids = []
    students = Student.query.all()
    for s in students:
        try:
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], s.photo)
            if os.path.exists(img_path):
                img = cv2.imread(img_path)
                if img is not None:
                    encoding = recognizer.get_face_encoding(img)
                    if encoding is not None:
                        known_encodings.append(encoding)
                        known_ids.append(s.id)
        except Exception as e:
            print(f"Error loading face for student {s.id}: {e}")
    return known_encodings, known_ids

@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    date_filter = request.args.get('date') or request.form.get('date')
    
    if date_filter:
        records = Attendance.query.filter(Attendance.time.like(f"{date_filter}%")).order_by(Attendance.time.desc()).all()
    else:
        records = Attendance.query.order_by(Attendance.time.desc()).all()
    
    student_ids = [r.student_id for r in records]
    students = {s.id: s for s in Student.query.filter(Student.id.in_(student_ids)).all()}
    enriched = []
    for r in records:
        s = students.get(r.student_id)
        if s:
            enriched.append({'id': r.id, 'name': s.name, 'roll_no': s.roll_no, 'time': r.time})
    return render_template('attendence.html', records=enriched, date_filter=date_filter)

@app.route('/delete_student/<int:id>')
@login_required
def delete_student(id):
    student = Student.query.get(id)
    if student:
        try:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], student.photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)
            db.session.delete(student)
            db.session.commit()
            flash("Student deleted successfully!")
        except Exception as e:
            flash(f"Error: {str(e)}")
    return redirect(url_for('dashboard'))

@app.route('/delete_attendance/<int:id>', methods=['POST'])
@login_required
def delete_attendance(id):
    password = request.form.get('password')
    
    # Admin password check
    if password != 'admin@123':
        flash("Incorrect password! Only admin can delete attendance.")
        return redirect(url_for('attendance'))
    
    record = Attendance.query.get(id)
    if record:
        try:
            db.session.delete(record)
            db.session.commit()
            flash("Attendance record deleted!")
        except Exception as e:
            flash(f"Error: {str(e)}")
    return redirect(url_for('attendance'))

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get(id)
    if not student:
        flash("Student not found!")
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        student.name = request.form.get('name')
        student.roll_no = request.form.get('roll_no')
        student.class_name = request.form.get('class_name')
        photo = request.files.get('photo')
        
        if photo and allowed_file(photo.filename):
            try:
                old_photo = os.path.join(app.config['UPLOAD_FOLDER'], student.photo)
                if os.path.exists(old_photo):
                    os.remove(old_photo)
                filename = secure_filename(photo.filename)
                unique_filename = f"{student.roll_no}_{filename}"
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                student.photo = unique_filename
            except Exception as e:
                flash(f"Error: {str(e)}")
        
        db.session.commit()
        flash("Student updated successfully!")
        return redirect(url_for('dashboard'))
    
    return render_template('edit_student.html', student=student)

@app.route('/face_recognition')
@login_required
def face_recognition_page():
    return render_template('face_recognition.html')

@app.route('/video_feed')
@login_required
def video_feed():
    def gen():
        cam = None
        recognizer = None
        try:
            with app.app_context():
                recognizer = FaceRecognizer()
                known_encodings, known_ids = load_known_faces(recognizer)
                app.logger.info(f"Loaded {len(known_encodings)} student faces")
                
                cam = cv2.VideoCapture(0)
                if not cam.isOpened():
                    app.logger.error("Camera not opened")
                    return
                
                today = datetime.datetime.now().date()
                marked_today = {a.student_id for a in Attendance.query.filter(
                    Attendance.time.like(f"{today}%")
                ).all()}
                
                frame_count = 0
                attendance_marked = False

                while True:
                    ret, frame = cam.read()
                    if not ret:
                        break
                    
                    frame_count += 1
                    
                    # Process every 3rd frame for performance
                    if frame_count % 3 == 0 and not attendance_marked:
                        face_locations = recognizer.detect_faces(frame)
                        face_encodings = recognizer.get_face_encodings(frame, face_locations)
                        
                        if len(face_locations) > 0:
                            app.logger.info(f"Detected {len(face_locations)} faces")
                            cv2.putText(frame, "Face Detected!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                        for face_encoding, loc in zip(face_encodings, face_locations):
                            top, right, bottom, left = loc
                            
                            name = "Unknown"
                            color = (0, 0, 255)
                            
                            if known_encodings:
                                matches = recognizer.compare_faces(known_encodings, face_encoding, tolerance=0.85)
                                face_distances = recognizer.face_distance(known_encodings, face_encoding)
                                best_index = np.argmin(face_distances)
                                
                                if matches[best_index] and face_distances[best_index] < 0.15:
                                    student_id = known_ids[best_index]
                                    s = Student.query.get(student_id)
                                    if s:
                                        name = s.name
                                        color = (0, 255, 0)
                                        
                                        if student_id not in marked_today:
                                            try:
                                                time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                att = Attendance(student_id=student_id, time=time_str)
                                                db.session.add(att)
                                                db.session.commit()
                                                marked_today.add(student_id)
                                                attendance_marked = True
                                                app.logger.info(f"Attendance marked for {name}")
                                            except Exception as e:
                                                app.logger.error(f"Attendance error: {e}")
                            
                            cv2.rectangle(frame, (left,top), (right,bottom), color, 3)
                            cv2.rectangle(frame, (left,bottom-35), (right,bottom), color, cv2.FILLED)
                            cv2.putText(frame, name, (left+6,bottom-6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2)
                    
                    if attendance_marked:
                        cv2.putText(frame, "Attendance Marked! Closing...", (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    else:
                        cv2.putText(frame, "Press 'Enter' to Exit", (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
                    if cv2.waitKey(1) & 0xFF == 13:
                        break

                    ret, jpeg = cv2.imencode('.jpg', frame)
                    if ret:
                        frame_bytes = jpeg.tobytes()
                        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                    
                    # Auto close after attendance marked
                    if attendance_marked:
                        import time
                        time.sleep(2)
                        break
                        
        except Exception as e:
            app.logger.error(f"Video feed error: {e}")
        finally:
            if cam is not None:
                cam.release()
            if recognizer is not None:
                recognizer.release()

    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
