from flask import Flask, request, jsonify, session
from flask_mail import Mail, Message
from flask_cors import CORS  # Import CORS
import random
import logging
from datetime import datetime
import pymysql
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Initialize Flask app
app = Flask(__name__)

# Configure CORS to support credentials
CORS(app, supports_credentials=True)
# Other configurations and route definitions here
app.secret_key = '441f6ab2f10c9580d68929df890f99eb'
app.config['SESSION_TYPE'] = 'filesystem'
# Initialize the session
Session(app)

# Configure Flask-Mail to send emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pradeepmathew115@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'dgwv rlcv zczm ykpp'  # Replace with your email password
mail = Mail(app)

# Set up error logging
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'mysql'),
        user=os.getenv('MYSQL_USER', 'user'),
        password=os.getenv('MYSQL_PASSWORD', 'userpassword'),
        database=os.getenv('MYSQL_DATABASE', 'tcs')
    )

# Define the User model
def create_user_table():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    phone VARCHAR(15) NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    dob DATE NOT NULL,
                    otp VARCHAR(6)
                )
            """)
        connection.commit()
        connection.close()
    except Exception as e:
        logging.error(f"Error creating table: {e}")
        return jsonify({'message': 'Error creating table.'}), 500

# Create tables if not exist
with app.app_context():
    create_user_table()

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
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({'message': 'Email already registered.'}), 409

            # Insert new user into the database
            cursor.execute("""
                INSERT INTO users (name, email, password, phone, gender, dob) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, email, password, phone, gender, dob))
            connection.commit()
        connection.close()

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

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                if user[1] == password:  # Compare the passwords
                    session['user_id'] = user[0]
                    logging.info(f'Session user_id set: {session["user_id"]}')
                    return jsonify({'message': 'Login successful.', 'userId': user[0]}), 200
                else:
                    return jsonify({'message': 'Invalid email or password.'}), 401
            else:
                return jsonify({'message': 'Invalid email or password.'}), 401
        connection.close()
    except Exception as e:
        logging.error(f'Error in login: {e}')
        return jsonify({'message': 'Login failed.'}), 500

@app.route('/get-profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, dob, phone FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

            if user:
                return jsonify({
                    "success": True,
                    "data": {
                        "name": user[0],
                        "dob": user[1].strftime('%Y-%m-%d'),
                        "phone": user[2]
                    }
                })
            else:
                return jsonify({"message": "User not found."}), 404
        connection.close()
    except Exception as e:
        logging.error(f'Error in retrieving profile: {e}')
        return jsonify({'message': 'Profile retrieval failed.'}), 500

@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()

        # Normalize the phone number by stripping +91 or leading zeros if present
        normalized_phone = phone.lstrip('+').lstrip('91') if phone.startswith('+91') else phone

        # Debugging: Print both original and normalized phone numbers
        print(f"Original phone: {phone}, Normalized phone: {normalized_phone}")

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, email FROM users WHERE phone = %s OR phone = %s", 
                (phone, f'+91{normalized_phone}')
            )
            user = cursor.fetchone()

            if not user:
                return jsonify({'message': 'Phone number not registered.'}), 404

            # Generate OTP and update user record
            otp = generate_otp()
            print(f"Generated OTP: {otp}")  # For debugging

            cursor.execute("UPDATE users SET otp = %s WHERE id = %s", (otp, user[0]))
            connection.commit()

        connection.close()

        # Send OTP via email
        msg = Message('Your OTP Code', sender='your_email@gmail.com', recipients=[user[1]])
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

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, otp FROM users WHERE phone = %s OR phone = %s", 
                (phone, normalized_phone)
            )
            user = cursor.fetchone()

            if not user:
                return jsonify({'message': 'Phone number not registered.'}), 404

            if user[1] != otp:
                return jsonify({'message': 'Invalid OTP.'}), 403

            if new_password != confirm_password:
                return jsonify({'message': 'Passwords do not match.'}), 400

            cursor.execute("UPDATE users SET password = %s, otp = NULL WHERE id = %s", (new_password, user[0]))
            connection.commit()

        connection.close()

        return jsonify({'message': 'Password reset successful.'}), 200
    except Exception as e:
        logging.error(f'Error in password reset: {e}')
        return jsonify({'message': 'Password reset failed.'}), 500

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Send an email to the user
    send_email(email, "Thank You for Your Feedback", f"Hello {name},\n\nThank you for your feedback!\n\nYour message:\n{message}\n\nBest,\nYour Team")

    # Send an email to the admin
    send_email("admin@domain.com", "User Feedback Received", f"Feedback from {name} ({email}):\n\n{message}")

    return jsonify({'message': 'Thank you for your feedback!'}), 200

def send_email(to, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = 'no-reply@domain.com'
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('your_email@gmail.com', 'your_password')
            text = msg.as_string()
            server.sendmail('your_email@gmail.com', to, text)
    except Exception as e:
        logging.error(f"Error in sending email: {e}")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
