import socket
import json

HOST = '127.0.0.1'  # Server IP
PORT = 65432        # Server Port

def send_request(request):
    """Send a JSON request to the server and receive a response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(json.dumps(request).encode('utf-8'))
        response = client_socket.recv(1024)
        return json.loads(response.decode('utf-8'))

while True:
    print("\nSynth Preset Manager")
    print("1. Create new preset")
    print("2. List all presets")
    print("3. Update preset")
    print("4. Delete preset")
    print("5. Exit")
    choice = int(input("Enter choice (1-5): "))

    if choice == 1:
        # Create new preset
        preset_name = input("Name this preset: ")
        cutoff_freq = input("Enter a cutoff frequency: ")
        resonance = input("Enter a resonance: ")
        amplitude = input("Enter an amplitude: ")
        resistance = input("Enter a resistance: ")

        request = {
            "operation": "create",
            "data": {
                "preset_name": preset_name,
                "cutoff_freq": cutoff_freq,
                "resonance": resonance,
                "amplitude": amplitude,
                "resistance": resistance
            }
        }
        response = send_request(request)
        print(response.get("message"))

    elif choice == 2:
        # List all presets
        request = {"operation": "list"}
        response = send_request(request)
        presets = response.get("presets", [])
        print("\nPresets:")
        print(presets)

    elif choice == 3:
        # Update preset
        preset_name = input("Enter preset name to update: ")
        print("What would you like to update?")
        print("1. Cutoff Frequency")
        print("2. Resonance")
        print("3. Amplitude")
        print("4. Resistance")
        sub_choice = int(input("Enter choice (1-4): "))

        update_data = {}
        if sub_choice == 1:
            update_data["cutoff_freq"] = input("Enter new cutoff frequency: ")
        elif sub_choice == 2:
            update_data["resonance"] = input("Enter new resonance: ")
        elif sub_choice == 3:
            update_data["amplitude"] = input("Enter new amplitude: ")
        elif sub_choice == 4:
            update_data["resistance"] = input("Enter new resistance: ")

        request = {
            "operation": "update",
            "preset_name": preset_name,
            "data": update_data
        }
        response = send_request(request)
        print(response.get("message"))

    elif choice == 4:
        # Delete preset
        preset_name = input("Enter preset name to delete: ")
        request = {
            "operation": "delete",
            "preset_name": preset_name
        }
        response = send_request(request)
        print(response.get("message"))

    elif choice == 5:
        # Exit
        request = {"operation": "exit"}
        response = send_request(request)
        print(response.get("message"))
        break

    else:
        print("Invalid choice. Please try again.")


















# import socket
# import json
# from controller import Controller
# from jsonSerializer import JsonSerializer

# # Client setup
# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 65432        # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#     client_socket.connect((HOST, PORT))
    
#     while True:
#         # User input to create a JSON object
#         user_input = input("Enter a message (type 'exit' to quit): ")
#         if user_input.lower() == 'exit':
#             break
        
#         message = {"message": user_input}
#         client_socket.sendall(json.dumps(message).encode('utf-8'))  # Send JSON message
        
#         # Receive response from the server
#         data = client_socket.recv(1024)
#         response = json.loads(data.decode('utf-8'))
#         print("Response from server:", response)
