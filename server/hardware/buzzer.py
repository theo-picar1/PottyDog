import RPi.GPIO as GPIO
import time

class PiezoBuzzer():
    def __init__(self):
        # Buzzer setup 
        self.BUZZER_PIN = 13
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)
        self.buzzer_pwm = GPIO.PWM(self.BUZZER_PIN, 4000) # 4000Hz 

    
    # Trigger buzzer
    def trigger_buzzer(self):
        self.buzzer_pwm.start(50)
        time.sleep(3)
        self.buzzer_pwm.stop()