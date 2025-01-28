import socket
import json

# Server setup
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    
    conn, addr = server_socket.accept()  # Accept a single client connection
    print(f"Connected by {addr}")
    with conn:
        while True:
            # Receive data
            data = conn.recv(1024)
            if not data:
                break  # End the connection if the client disconnects
            
            # Decode and process JSON
            try:
                received_json = json.loads(data.decode('utf-8'))
                print("Received JSON:", received_json)
                
                # Send a response JSON back to the client
                response = {"status": "success", "message": "JSON received"}
                conn.sendall(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError:
                print("Invalid JSON received.")
                conn.sendall(json.dumps({"status": "error", "message": "Invalid JSON"}).encode('utf-8'))
