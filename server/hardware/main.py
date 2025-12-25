from .sensor_publisher import publish_motion
from .buzzer import PiezoBuzzer   
from .pir import PIRSensor 
import RPi.GPIO as GPIO
import time

# Configure PIR and Buzzer
PIR_PIN = 17   
pir = PIRSensor(PIR_PIN)
buzzer = PiezoBuzzer()

try:
    print("Starting motion detection...")
    time.sleep(2)  # Give PIR sensor time to stabilize

    while True:
        if pir.motion_detected():
            print("Motion Detected!")
            publish_motion("detected")
            buzzer.trigger_buzzer()
        else:
            print("No motion detected")
        time.sleep(1)  

except KeyboardInterrupt:
    print("Exiting program...")
    pir.cleanup()
    GPIO.cleanup()