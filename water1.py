# SoilSensor.py - Raspberry Pi Soil Moisture Detection Script

import RPi.GPIO as GPIO
import time

# GPIO Configuration
SENSOR_CHANNEL = 4  # GPIO4 (Physical Pin 7)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_CHANNEL, GPIO.IN)

def sensor_callback(channel):
    """
    Callback function triggered when moisture state changes.
    Prints status to console.
    """
    if GPIO.input(channel):
        print("[STATUS] Soil is DRY - Water needed!")
    else:
        print("[STATUS] Soil is WET - No action required.")

# Event detection setup
GPIO.add_event_detect(SENSOR_CHANNEL, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(SENSOR_CHANNEL, sensor_callback)

try:
    print("Soil Moisture Monitoring Started (Ctrl+C to exit)...")
    while True:
        time.sleep(1)  # Reduce CPU usage
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nMonitoring stopped. GPIO cleanup complete.")