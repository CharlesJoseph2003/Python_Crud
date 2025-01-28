import socket
import json

# Client setup
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    
    while True:
        # User input to create a JSON object
        user_input = input("Enter a message (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        
        message = {"message": user_input}
        client_socket.sendall(json.dumps(message).encode('utf-8'))  # Send JSON message
        
        # Receive response from the server
        data = client_socket.recv(1024)
        response = json.loads(data.decode('utf-8'))
        print("Response from server:", response)
