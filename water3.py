# SoilSensorEmail.py - Integrated Soil Monitoring & Email Alerts

import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Configuration
SENSOR_CHANNEL = 4  # GPIO4
SENDER_EMAIL = "3022958276@qq.com"
SENDER_PASSWORD = "123"
RECIPIENT_EMAIL = "rslinnnn@gmail.com"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
CHECK_INTERVAL = 21600  # 6 hours (4x daily)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_CHANNEL, GPIO.IN)

# Email function (reusable)
def send_alert(status):
    """Sends formatted email based on soil status."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Plant Alert: {status}"
    body = f"""\
    Plant Status Update ({timestamp})
    -------------------------------
    Soil moisture level: {status}
    Action required: {"Water the plant!" if "DRY" in status else "No action needed."}
    """
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"[{timestamp}] Email sent: {status}")
    except Exception as e:
        print(f"[ERROR] Email failed: {str(e)}")

# Main monitoring loop
try:
    print("Starting integrated soil monitoring...")
    last_check = time.time()
    
    while True:
        current_state = GPIO.input(SENSOR_CHANNEL)
        status = "DRY" if current_state else "WET"
        
        # Send email at scheduled intervals
        if (time.time() - last_check) >= CHECK_INTERVAL:
            send_alert(status)
            last_check = time.time()
            
        time.sleep(60)  # Check every minute
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nMonitoring stopped. GPIO cleanup complete.")