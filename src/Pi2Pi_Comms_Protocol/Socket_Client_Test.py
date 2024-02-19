import socket

# Define server address and port
SERVER_HOST = '192.168.0.103'  # IP address of the server Raspberry Pi - Used pigi on APPFRE network as an example
SERVER_PORT = 12345  # Same port as the server

# Create a socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Send data to the server
    client_socket.sendall(b"Hello from client!")

    # Receive a response from the server
    data = client_socket.recv(1024)
    print("Received from server:", data.decode())


#WRITTEN BY CHATGPT
