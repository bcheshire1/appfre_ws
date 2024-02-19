import socket

# Define server address and port
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345      # Arbitrary port number

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

        # Receive data from the client
        data = client_socket.recv(1024)
        print("Received:", data.decode())

        # Send a response back to the client
        client_socket.sendall(b"Hello from server!")

#WRITTEN BY CHATGPT
