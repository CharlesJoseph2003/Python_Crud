import requests
import time
import json
import tkinter as tk
from client import SynthesizerGUI

SERVER_URL = "http://localhost:5000/current_config"

def update_gui(gui, config):
    # Add preset name as "Live Update"
    config['preset_name'] = "Live Update"
    gui.update_synth_display(config)

def main():
    print("Starting synth client...")
    
    # Create the GUI
    root = tk.Tk()
    app = SynthesizerGUI(root)
    
    def update_loop():
        try:
            # Get the latest configuration from the server
            response = requests.get(SERVER_URL)
            if response.status_code == 200:
                config = response.json()
                update_gui(app, config)
            else:
                print("Failed to get configuration from server")
        except Exception as e:
            print(f"Error: {e}")
        
        # Schedule the next update in 1000ms (1 second)
        root.after(1000, update_loop)
    
    # Start the update loop
    update_loop()
    
    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()
