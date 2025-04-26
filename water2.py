# send_email.py - Raspberry Pi Email Notification via SMTP

import smtplib
from email.message import EmailMessage

# Email Configuration (REPLACE THESE VALUES)
SENDER_EMAIL = "3022958276@qq.com"
SENDER_PASSWORD = "123"  # App-specific password
RECIPIENT_EMAIL = "rslinnnn@gmail.com"
SMTP_SERVER = "smtp.office365.com"  # Outlook SMTP
SMTP_PORT = 587

def send_email(subject, body):
    """
    Sends an email notification using SMTP.
    """
    # Create email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL

    # Connect to SMTP server
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("[EMAIL] Notification sent successfully.")
    except Exception as e:
        print(f"[ERROR] Email failed: {str(e)}")

# Test email (uncomment to debug)
# send_email("Test Subject", "Hello from Raspberry Pi!")