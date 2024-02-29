from gpiozero import Button
from signal import pause
import time
import datetime
import threading

# Define GPIO pin for the Geiger counter input
# As specified in PiGI Schematic - Physical Pin 7 - BCM pin GPIO4
GEIGER_PIN = 4

# Setup Button
geiger_button = Button(GEIGER_PIN, pull_up=False, bounce_time=0.0001)  # Use Button with pull_down and bounce_time

# Initialize counter - keeps track of the number of falling edges detected
count = 0

# Flag to control counting
counting_enabled = True

# Function to handle falling edge interrupt
def falling_edge_callback():
    global count, counting_enabled
    if counting_enabled:
        count += 1
        print(f"Falling edge detected! Count: {count}")

# Attach falling edge detection event
geiger_button.when_released = falling_edge_callback

# Function to pause/unpause counting
def toggle_counting():
    global counting_enabled
    counting_enabled = not counting_enabled
    if counting_enabled:
        print("Counting resumed.")
    else:
        print("Counting paused.")

# Thread function to listen for Enter key press
def key_listener():
    global counting_enabled
    while True:
        input()  # Wait for Enter key press
        toggle_counting()

# Start the key listener thread
key_listener_thread = threading.Thread(target=key_listener)
key_listener_thread.start()

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
