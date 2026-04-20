# app.py
from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables (create .env file for security)
load_dotenv()

app = Flask(__name__)

# Email configuration - Using environment variables for security
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "hr.nexgensoftwares@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "cwoovckcbphhnqes")  # Replace with your App Password
RECIPIENT_EMAIL = "hr.nexgensoftwares@gmail.com"

def send_email(project_data):
    """Send email with project specifications"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Reply-To'] = project_data.get('email', '')
        msg['Subject'] = f"New Project Specification from {project_data.get('name', 'Anonymous')}"

        # Email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #1a237e;">📋 New Project Specification Received</h2>
            <hr style="border: 1px solid #304ffe;">
            
            <h3 style="color: #283593;">👤 Client Information:</h3>
            <table style="border-collapse: collapse; width: 100%;">
                <tr><td style="padding: 8px;"><strong>Name:</strong></td><td>{project_data.get('name', 'Not provided')}</td></tr>
                <tr><td style="padding: 8px;"><strong>Email:</strong></td><td>{project_data.get('email', 'Not provided')}</td></tr>
                <tr><td style="padding: 8px;"><strong>Phone:</strong></td><td>{project_data.get('phone', 'Not provided')}</td></tr>
                <tr><td style="padding: 8px;"><strong>Company:</strong></td><td>{project_data.get('company', 'Not provided')}</td></tr>
            </table>
            
            <h3 style="color: #283593;">🚀 Project Details:</h3>
            <p><strong>Project Type:</strong> {project_data.get('project_type', 'Not specified')}</p>
            <p><strong>Project Title:</strong> {project_data.get('title', 'Not provided')}</p>
            <p><strong>Budget Range:</strong> {project_data.get('budget', 'Not specified')}</p>
            <p><strong>Timeline:</strong> {project_data.get('timeline', 'Not specified')}</p>
            
            <h3 style="color: #283593;">📝 Detailed Specifications:</h3>
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; border-left: 4px solid #304ffe;">
                {project_data.get('specifications', 'No specifications provided')}
            </div>
            
            <hr>
            <p style="font-size: 12px; color: #666;">This email was generated from NEX GEN SOFTWARES website contact form.</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return True, "Email sent successfully!"

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False, f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-project', methods=['POST'])
def submit_project():
    """Handle project specification submission"""
    try:
        project_data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'company': request.form.get('company', ''),
            'project_type': request.form.get('project_type', ''),
            'title': request.form.get('title', ''),
            'budget': request.form.get('budget', ''),
            'timeline': request.form.get('timeline', ''),
            'specifications': request.form.get('specifications', '')
        }

        # Basic validation
        if not project_data['name'] or not project_data['email'] or not project_data['phone'] or not project_data['specifications']:
            return jsonify({'success': False, 'message': 'Please fill in all required fields (Name, Email, Phone, Specifications).'}), 400

        # Send email
        success, message = send_email(project_data)

        if success:
            return jsonify({'success': True, 'message': 'Your project specifications have been submitted successfully! We will contact you soon.'})
        else:
            return jsonify({'success': False, 'message': message}), 500

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)