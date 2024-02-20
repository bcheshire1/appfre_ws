import socket #Socket
from gpiozero import Button #GPIO zero - for Pi5
from signal import pause
import time
import datetime

# Define server address and port
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345      # Arbitrary port number

 # Define GPIO pin for the Geiger counter input
# As specified in PiGI Schematic - Physical Pin 7 - BCM pin GPIO4
GEIGER_PIN = 4

# Setup Button
geiger_button = Button(GEIGER_PIN, pull_up=True, bounce_time=0.05)  # Use Button with pull_up and bounce_time

# Create a socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print("Server listening on {}:{}".format(HOST, PORT))


    # Accept a connection
    client_socket, client_address = server_socket.accept()

    with client_socket:
        print("Connected to client:", client_address)

        # Send real-time data to the client
        while True:

            # Initialize counter - keeps track of the number of falling edges detected
            count = 0

            # Get current timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
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
          
            # Concatenate count and timestamp into a single string
            data_to_send = f"{count},{timestamp}"

            #Print to confirm on both SSH terminals
            print(f"{timestamp} Sending count:", count)
            
            # Send data to the client
            client_socket.sendall(data_to_send.encode())

            # Wait for a short interval
            time.sleep(10)  # Adjust as needed for your desired update rate

#WRITTEN BY CHATGPT
#Tested and tweaked by NL
