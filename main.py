import smtplib
import os
from flask import Flask, render_template, request, jsonify
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()  # Load env vars from .env

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    # Compose email
    msg = EmailMessage()
    msg['Subject'] = f"New Contact Form Submission: {subject}"
    msg['From'] = os.getenv("EMAIL_USER")
    msg['To'] = os.getenv("EMAIL_USER")  # or another recipient
    msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            smtp.send_message(msg)

        return jsonify({"message": "Form submitted successfully!"})
    except Exception as e:
        print("Email send failed:", e)
        return jsonify({"message": "Failed to send email."}), 500

if __name__ == '__main__':
    app.run(debug=True)
