from .sensor_publisher import publish_motion
from .buzzer import PiezoBuzzer   
from .pir import PIRSensor 
import RPi.GPIO as GPIO
import time

# Configure PIR and Buzzer
PIR_PIN = 17   
pir = PIRSensor(PIR_PIN)
buzzer = PiezoBuzzer()

# Variables 
curr_time = time.time()
prev_time = time.time()
start_detect_time = None
detected_potty = False
INACTIVE_TIME_THRESHOLD = 30.0
WAIT_TIME_THRESHOLD = 10.0 # If motion detected this long, wants to go out

try:
    print("Starting motion detection...")
    time.sleep(5)  # Give PIR sensor time to stabilize

    while True:
        now = time.time()
        
        # No motion detected for some time
        if now - prev_time > INACTIVE_TIME_THRESHOLD:
            print("No activity for some time!")
            publish_motion("inactive")#
            start_detect_time = None
        
        # Basic motion detected
        if pir.motion_detected():
            print("Motion detected")
            publish_motion("detected")
            prev_time = now # Reset
            
            if start_detect_time is None:
                start_detect_time = now
            elif detected_potty is False and now - start_detect_time > WAIT_TIME_THRESHOLD: # Dog waiting by door
                detected_potty = True
                print("Dog wants to potty!")
                publish_motion("potty")
                start_detect_time = now
                buzzer.trigger_buzzer()
                time.sleep(10) # 10s for owner to respond before back to normal tracking
                detected_potty = False
                
        time.sleep(1)  

except KeyboardInterrupt:
    print("Exiting program...")
    pir.cleanup()
    GPIO.cleanup()