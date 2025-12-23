import time
from pir import PIRSensor  
from buzzer import PiezoBuzzer   

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
            buzzer.trigger_buzzer()
        else:
            print("No motion detected")
        time.sleep(0.5)  

except KeyboardInterrupt:
    print("Exiting program...")
    pir.cleanup()
    GPIO.cleanup()
