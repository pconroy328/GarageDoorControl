##import RPi.GPIO as GPIO
from time import sleep

class Relay:
    def __init__(self):
        print 'Creating and initializing relay class'
        #GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BCM)

        # I've wired door 1 to relay 1 to GPIO pin 23
        # door 2 is relay 2 on GPIO pin 24
        # sleep 0.25 seconds between relay trigger low/high to simulate button press
        self.door1_pin_number = 23
        self.door2_pin_number = 24
        self.latch_time = 0.25
        # Set relay pins as output
        #GPIO.setup(self.door1_pin_number, GPIO.OUT, initial=GPIO.HIGH)
        #GPIO.setup(self.door2_pin_number, GPIO.OUT, initial=GPIO.HIGH)

    def trigger(self, door_id=1):
        if door_id == 1:
            pin_number = self.door1_pin_number
        else:
            pin_number = self.door2_pin_number
        print 'Relay Trigger invoked on pin number', pin_number
        #GPIO.output(pin_number, GPIO.LOW)
        sleep(self.latch_time)
        #GPIO.output(pin_number, GPIO.HIGH)

    def cleanup(self):
        print 'Cleaning up relay'
        #GPIO.output(self.door1_pin_number, GPIO.HIGH)
        #GPIO.output(self.door2_pin_number, GPIO.HIGH)
        #GPIO.cleanup(self.door1_pin_number)
        #GPIO.cleanup(self.door2_pin_number)

