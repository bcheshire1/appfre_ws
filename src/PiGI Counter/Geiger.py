from gpiozero import Button
from signal import pause
import time
import datetime

# Define GPIO pin for the Geiger counter input
# As specified in PiGI Schematic - Physical Pin 7 - BCM pin GPIO4
GEIGER_PIN = 4

# Setup Button
geiger_button = Button(GEIGER_PIN, pull_up=True, bounce_time=0.05)  # Use Button with pull_up and bounce_time

# Initialize counter - keeps track of the number of falling edges detected
count = 0

# Function to handle falling edge interrupt
def falling_edge_callback():
    global count
    count += 1
    
    print(f"Falling edge detected! Count: {count}")

# Attach falling edge detection event
geiger_button.when_pressed = falling_edge_callback

try:
    # Run the script indefinitely
    while True:
        # Log counts to a file with a timestamp
        with open("geiger_log.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} - Counts: {count}\n")

        # Reset the count every x amount of seconds
        if count > 0:
            print("Resetting count.")
            count = 0

        # Wait for a while before logging again
        # Divide by value to get cps or times by a different value to get cpm
        time.sleep(10)

except KeyboardInterrupt:
    print("\nScript terminated by user.")

# Test on RPi, PiGI, and Leybold detector
# Detects falling edges w/ cumulative count
# Speeds up when the lantern close to the window - def detecting radiation
# needs to be tuned

# Publish timestamp and counts to ROS topic
# RUN AS ROOT (SUDO) ON Pi TO ACCESS GPIO
pause()  # Keep the program running
