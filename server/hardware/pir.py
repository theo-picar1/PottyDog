import RPi.GPIO as GPIO

class PIRSensor:
    def __init__(self, pin, mode=GPIO.BCM):
        self.pin = pin
        GPIO.setmode(mode)
        GPIO.setup(self.pin, GPIO.IN)

    def read(self):
        # Return raw GPIO value (0 or 1).
        return GPIO.input(self.pin)

    def motion_detected(self):
        # Return True if motion is detected.
        return GPIO.input(self.pin) == GPIO.HIGH

    def cleanup(self):
        GPIO.cleanup(self.pin)
