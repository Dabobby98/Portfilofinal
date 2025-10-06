#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
import ssl

app = Flask(__name__, static_folder='.')

ALLOWED_ORIGIN = os.environ.get('REPLIT_DEV_DOMAIN', '*')
CORS(app, origins=[f"https://{ALLOWED_ORIGIN}"] if ALLOWED_ORIGIN != '*' else ['*'])

ADMIN_EMAIL = 'lehuuphuc.ht2016@gmail.com'

def validate_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_text(text):
    """Basic HTML escaping to prevent XSS"""
    if not text:
        return ''
    return (str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#x27;'))

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'message': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json(silent=True)
        
        if data is None:
            return jsonify({
                'success': False,
                'message': 'Invalid JSON data'
            }), 400
        
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_email = os.environ.get('SMTP_EMAIL', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        
        if not smtp_email or not smtp_password:
            return jsonify({
                'success': False,
                'message': 'Email service not configured. Please contact administrator.'
            }), 500
        
        name = sanitize_text(data.get('Name', ''))
        company = sanitize_text(data.get('Company', ''))
        sender_email = data.get('E-mail', '').strip()
        phone = sanitize_text(data.get('Phone', ''))
        message = sanitize_text(data.get('Message', ''))
        
        if not name or not sender_email or not phone or not message:
            return jsonify({
                'success': False,
                'message': 'Please fill in all required fields: Name, Email, Phone, and Message.'
            }), 400
        
        if not validate_email(sender_email):
            return jsonify({
                'success': False,
                'message': 'Please provide a valid email address.'
            }), 400
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"New Contact Form Message from {name}"
        msg['From'] = smtp_email
        msg['To'] = ADMIN_EMAIL
        msg['Reply-To'] = sender_email
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #7c3aed; border-bottom: 3px solid #7c3aed; padding-bottom: 10px;">
                    📧 New Contact Form Message
                </h2>
                <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                    <tr style="background-color: #f8f8f8;">
                        <td style="padding: 12px; border: 1px solid #e9e9e9; font-weight: bold; width: 30%;">👤 Name:</td>
                        <td style="padding: 12px; border: 1px solid #e9e9e9;">{name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 12px; border: 1px solid #e9e9e9; font-weight: bold;">📧 Email:</td>
                        <td style="padding: 12px; border: 1px solid #e9e9e9;"><a href="mailto:{sender_email}">{sender_email}</a></td>
                    </tr>
                    <tr style="background-color: #f8f8f8;">
                        <td style="padding: 12px; border: 1px solid #e9e9e9; font-weight: bold;">📱 Phone:</td>
                        <td style="padding: 12px; border: 1px solid #e9e9e9;">{phone}</td>
                    </tr>
                    {f'<tr><td style="padding: 12px; border: 1px solid #e9e9e9; font-weight: bold;">🏢 Company:</td><td style="padding: 12px; border: 1px solid #e9e9e9;">{company}</td></tr>' if company else ''}
                    <tr style="background-color: #f8f8f8;">
                        <td style="padding: 12px; border: 1px solid #e9e9e9; font-weight: bold; vertical-align: top;">💬 Message:</td>
                        <td style="padding: 12px; border: 1px solid #e9e9e9; white-space: pre-wrap;">{message}</td>
                    </tr>
                </table>
                <div style="margin-top: 30px; padding: 15px; background-color: #f0f9ff; border-left: 4px solid #7c3aed; border-radius: 4px;">
                    <p style="margin: 0; color: #666; font-size: 14px;">
                        ✉️ This message was sent from your portfolio contact form.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
New Contact Form Message

Name: {name}
Email: {sender_email}
Phone: {phone}
{f'Company: {company}' if company else ''}

Message:
{message}

---
This message was sent from your portfolio contact form.
        """
        
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)
        
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls(context=context)
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
        
        return jsonify({
            'success': True,
            'message': 'Email sent successfully!'
        })
        
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: Invalid email or password")
        return jsonify({
            'success': False,
            'message': 'Email authentication failed. Please check SMTP credentials.'
        }), 500
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Email sending failed. Please try again later.'
        }), 500
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': 'Invalid data provided.'
        }), 400
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again later.'
        }), 500

if __name__ == "__main__":
    port = 5000
    print(f"Starting server on port {port}...")
    print(f"✅ Website running at http://0.0.0.0:{port}/")
    print("🎉 Your portfolio is now live with 'Le Huu Phuc' as the name!")
    
    if not os.environ.get('SMTP_EMAIL') or not os.environ.get('SMTP_PASSWORD'):
        print("⚠️  Warning: SMTP credentials not set. Email functionality will not work.")
        print("   Please set SMTP_EMAIL and SMTP_PASSWORD to enable email sending.")
    else:
        print(f"📧 Email service configured: {os.environ.get('SMTP_EMAIL')}")
        print(f"🔧 SMTP Server: {os.environ.get('SMTP_SERVER', 'smtp.gmail.com')}:{os.environ.get('SMTP_PORT', '587')}")
        print(f"📬 Emails will be sent to: {ADMIN_EMAIL}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
