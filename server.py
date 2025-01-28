import socket
import json
from controller import Controller
from jsonSerializer import JsonSerializer

# Server setup
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port for listening

controller = Controller()  # Initialize controller

def handle_request(data):
    """Process the request and perform the corresponding CRUD operation."""
    try:
        print(f"Received request data: {data}")  # Debug print
        request = json.loads(data)
        operation = request.get("operation")
        print(f"Processing operation: {operation}")  # Debug print

        if operation == "create":
            # Create a new preset
            data = request.get("data", {})
            preset_name = data.get("preset_name")
            print(f"Creating new preset: {preset_name}")  # Debug print
            cutoff_freq = data.get("cutoff_freq")
            resonance = data.get("resonance")
            amplitude = data.get("amplitude")
            resistance = data.get("resistance")
            controller.create_preset(preset_name, cutoff_freq, resonance, amplitude, resistance)
            return {"status": "success", "message": "Preset created successfully."}

        elif operation == "list":
            # List all presets
            json_serializer = JsonSerializer()
            presets = json_serializer.serialize(controller)
            return {"status": "success", "presets": presets}

        elif operation == "update":
            # Update a preset
            preset_name = request.get("preset_name")
            data = request.get("data", {})
            if controller.update_preset(preset_name, **data):
                return {"status": "success", "message": "Preset updated successfully."}
            return {"status": "error", "message": "Preset not found."}

        elif operation == "delete":
            # Delete a preset
            preset_name = request.get("preset_name")
            if controller.delete_preset(preset_name):
                return {"status": "success", "message": "Preset deleted successfully."}
            return {"status": "error", "message": "Preset not found."}

        elif operation == "exit":
            # Handle client exit
            return {"status": "success", "message": "Goodbye!"}

        else:
            return {"status": "error", "message": "Invalid operation."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Start the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                response = handle_request(data.decode('utf-8'))
                print(f"Sending response: {response}")  # Debug print
                conn.sendall(json.dumps(response).encode('utf-8'))















# import socket
# import json

# # Server setup
# HOST = '127.0.0.1'  # Localhost
# PORT = 65432        # Port to listen on

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#     server_socket.bind((HOST, PORT))
#     server_socket.listen()
#     print(f"Server is listening on {HOST}:{PORT}")
    
#     conn, addr = server_socket.accept()  # Accept a single client connection
#     print(f"Connected by {addr}")
#     with conn:
#         while True:
#             # Receive data
#             data = conn.recv(1024)
#             if not data:
#                 break  # End the connection if the client disconnects
            
#             # Decode and process JSON
#             try:
#                 received_json = json.loads(data.decode('utf-8'))
#                 print("Received JSON:", received_json)
                
#                 # Send a response JSON back to the client
#                 response = {"status": "success", "message": "JSON received"}
#                 conn.sendall(json.dumps(response).encode('utf-8'))
#             except json.JSONDecodeError:
#                 print("Invalid JSON received.")
#                 conn.sendall(json.dumps({"status": "error", "message": "Invalid JSON"}).encode('utf-8'))
