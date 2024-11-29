from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_cors import CORS  # Import CORS
import random
import logging
from datetime import datetime
from sqlalchemy.orm import Session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Initialize Flask app
app = Flask(__name__)

# Configure CORS to support credentials
CORS(app) # Update this to match your fronten

# Configure session cookie settings
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allow cross-origin requests
app.config['SESSION_COOKIE_SECURE'] = True  # Use True if your app is served over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_PERMANENT'] = False  # Set to False to allow sessions to be temporary
app.config['SESSION_COOKIE_DOMAIN'] = ''  # Web server IP
app.config['SESSION_COOKIE_NAME'] = 'my_flask_session'

# Other configurations and route definitions here
app.secret_key = '441f6ab2f10c9580d68929df890f99eb'
app.config['SESSION_TYPE'] = 'filesystem'
# Initialize the session
Session(app)
# Configure SQLAlchemy to connect with your RDS MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root_password@db/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Flask-Mail to send emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pradeepmathew115@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'dgwv rlcv zczm ykpp'  # Replace with your email password

# Initialize SQLAlchemy and Flask-Mail
db = SQLAlchemy(app)
mail = Mail(app)

# Set up error logging
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store as plain text (not recommended)
    phone = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    otp = db.Column(db.String(6), nullable=True)

# Create tables if not exist
with app.app_context():
    db.create_all()

def generate_otp():
    """Generate a random 6-digit OTP."""
    return str(random.randint(100000, 999999))

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')  # Store as plain text (not recommended)
        phone = data.get('phone')
        gender = data.get('gender')
        dob = datetime.strptime(data.get('dob'), '%Y-%m-%d').date()

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already registered.'}), 409

        # Create a new user
        new_user = User(name=name, email=email, password=password, phone=phone, gender=gender, dob=dob)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully.'}), 201
    except Exception as e:
        logging.error(f'Error in signup: {e}')
        return jsonify({'message': 'Signup failed.'}), 500



@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logging.info(f'Received login request: {data}')

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                session['user_id'] = user.id
                logging.info(f'Session user_id set: {session["user_id"]}')

                # Return user ID along with success message
                return jsonify({'message': 'Login successful.', 'userId': user.id}), 200
            else:
                return jsonify({'message': 'Invalid email or password.'}), 401
        else:
            return jsonify({'message': 'Invalid email or password.'}), 401
    except Exception as e:
        logging.error(f'Error in login: {e}')
        return jsonify({'message': 'Login failed.'}), 500

@app.route('/get-profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    print("Incoming cookies:", request.cookies)
    print("Session before retrieval:", session)

    print("User ID from request:", user_id)

    user = User.query.get(user_id)
    if user:
        return jsonify({
            "success": True,
            "data": {
                "name": user.name,
                "dob": user.dob.strftime('%Y-%m-%d'),
                "phone": user.phone
            }
        })
    else:
        return jsonify({"message": "User not found."}), 404

@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()

        # Normalize the phone number by stripping +91 or leading zeros if present
        normalized_phone = phone.lstrip('+').lstrip('91') if phone.startswith('+91') else phone

        # Debugging: Print both original and normalized phone numbers
        print(f"Original phone: {phone}, Normalized phone: {normalized_phone}")

        # Query database with or without the country code
        user = User.query.filter(
            (User.phone == phone) | (User.phone == f'+91{normalized_phone}')
        ).first()

        if not user:
            return jsonify({'message': 'Phone number not registered.'}), 404

        # Generate OTP and update user record
        otp = generate_otp()
        print(f"Generated OTP: {otp}")  # For debugging

        user.otp = otp
        db.session.commit()

        # Send OTP via email
        msg = Message('Your OTP Code', sender='your_email@gmail.com', recipients=[user.email])
        msg.body = f'Your OTP code is: {otp}'
        mail.send(msg)

        return jsonify({'message': 'OTP sent to your registered email.'}), 200

    except Exception as e:
        logging.error(f'Error in sending OTP: {str(e)}')
        return jsonify({'message': 'Failed to send OTP.'}), 500


@app.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        phone = data.get('phone')
        otp = data.get('otp')
        new_password = data.get('newPassword')
        confirm_password = data.get('confirmPassword')

        # Normalize phone input (strip country code +91 if provided)
        normalized_phone = phone.lstrip('+91') if phone.startswith('+91') else phone

        # Search for user with either the raw or normalized phone number
        user = User.query.filter(
            (User.phone == phone) | (User.phone == normalized_phone)
        ).first()

        if not user:
            return jsonify({'message': 'Phone number not registered.'}), 404

        if user.otp != otp:
            return jsonify({'message': 'Invalid OTP.'}), 403

        if new_password != confirm_password:
            return jsonify({'message': 'Passwords do not match.'}), 400

        user.password = new_password
        user.otp = None
        db.session.commit()

        return jsonify({'message': 'Password reset successful.'}), 200
    except Exception as e:
        logging.error(f'Error in password reset: {e}')
        return jsonify({'message': 'Password reset failed.'}), 500
# Route to handle feedback submission
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Send an email to the user
    send_email(email, "Thank You for Your Feedback", f"Hello {name},\n\nThank you for your feedback!\n\nYour message:\n{message}\n\nBest,\nYour Team")

    # Send an email to the admin
    admin_email = "pradeepmathew115@gmail.com"  # Change this to your admin email
    send_email(admin_email, "New Feedback Received", f"Name: {name}\nEmail: {email}\nMessage:\n{message}")

    return jsonify({"message": "Feedback submitted successfully!"})

def send_email(to_email, subject, body):
    from_email = "pradeepmathew115@gmail.com"  # Change this to your Gmail address
    password = "dgwv rlcv zczm ykpp"  # Use your App Password here

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"Email sent to {to_email}")  # Optional: Log successful email send
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
