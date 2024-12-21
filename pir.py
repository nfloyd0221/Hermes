import time
from gpiozero import MotionSensor
from pynput.keyboard import Controller

# Initialize the PIR sensor and keyboard controller
pir = MotionSensor(4)  # Change to your GPIO pin
keyboard = Controller()

# Function to simulate keystroke
def on_motion():
    keyboard.press('a')  # Simulate pressing 'a'
    keyboard.release('a')

# Main loop
while True:
    pir.wait_for_motion()  # Wait for motion
    on_motion()  # Simulate keystroke
    time.sleep(600)  # Wait 10 minutes (600 seconds) before looking for another input
