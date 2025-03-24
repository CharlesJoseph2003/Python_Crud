import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import json
import threading
from client import SynthesizerGUI

class LocalSynthGenerator:
    """Local replacement for the server-side synth configuration generator"""
    
    def __init__(self):
        # Global variables similar to server
        self.current_preset = None
        self.use_preset = False
        
    def save_current_config(self, config, is_preset=False):
        """Save the current configuration to current.json"""
        # Create a copy of the config to avoid modifying the original
        config_to_save = config.copy()
        
        # Remove preset_name if it exists
        if 'preset_name' in config_to_save:
            del config_to_save['preset_name']
        
        # Add the flag indicating if this is a preset
        config_to_save['is_preset'] = is_preset
        
        with open('current.json', 'w') as f:
            json.dump(config_to_save, f, indent=4)

    def generate_synth_config(self):
        """Generate a new synth configuration (either from preset or random)"""
        # If a preset has been loaded, use it instead of random values
        if self.use_preset and self.current_preset:
            # Reset the flag after using once to return to random values unless loaded again
            self.use_preset = False
            # Make a copy and remove preset_name
            config = self.current_preset.copy()
            if 'preset_name' in config:
                del config['preset_name']
            self.save_current_config(config, is_preset=True)
        else:
            # Otherwise, generate random values as before
            waveforms = ["square", "triangle", "sine", "saw"]
            config = {
                "cutoff_freq": round(random.uniform(20, 200), 5),
                "resonance": round(random.uniform(0.5, 6.0), 5),
                "A": round(random.uniform(0.1, 1.0), 5),
                "D": round(random.uniform(20, 60), 5),
                "S": round(random.uniform(20, 60), 5),
                "R": round(random.uniform(20, 60), 5),
                "waveform": random.choice(waveforms)
            }
            self.save_current_config(config, is_preset=False)
        
        return config
    
    def load_preset(self, preset_data):
        """Load a preset configuration"""
        if preset_data:
            self.current_preset = preset_data
            self.use_preset = True
            # Make a copy and remove preset_name before saving
            config = preset_data.copy()
            if 'preset_name' in config:
                del config['preset_name']
            self.save_current_config(config, is_preset=True)
            return {"status": "success", "message": "Preset loaded"}
        else:
            return {"status": "error", "message": "Invalid preset data"}


class EnhancedSynthesizerGUI(SynthesizerGUI):
    """Extends SynthesizerGUI to work with local generator instead of server"""
    
    def __init__(self, root):
        # Initialize the parent class
        super().__init__(root)
        
        # Replace server polling with local generator
        self.synth_generator = LocalSynthGenerator()
        
        # Stop the HTTP polling thread
        self.polling_active = False
        if hasattr(self, 'polling_thread') and self.polling_thread.is_alive():
            self.polling_thread.join(timeout=1.0)
        
        # Start a local update thread instead
        self.update_active = True
        self.update_thread = threading.Thread(target=self.local_update_loop, daemon=True)
        self.update_thread.start()
    
    def local_update_loop(self):
        """Generate and apply synth configurations locally instead of polling server"""
        while self.update_active:
            # Generate new configuration
            data = self.synth_generator.generate_synth_config()
            
            # Update the GUI (using the main thread)
            self.root.after(0, self.update_gui_from_server, data)
            
            # Wait before next update
            time.sleep(1.0)
    
    def load_preset(self):
        """Override to use local generator instead of server"""
        if not self.presets_listbox.curselection():
            messagebox.showerror("Error", "Please select a preset to load")
            return
            
        preset_name = self.presets_listbox.get(self.presets_listbox.curselection())
        preset_data = self.controller.get_preset(preset_name)
        
        if preset_data:
            # Update entry fields with preset data
            self.preset_name_entry.delete(0, tk.END)
            self.preset_name_entry.insert(0, preset_data["preset_name"])
            
            # Update scales
            self.param_widgets["cutoff"]["scale"].set(preset_data["cutoff_freq"])
            self.param_widgets["resonance"]["scale"].set(preset_data["resonance"])
            self.param_widgets["a"]["scale"].set(preset_data["A"])
            self.param_widgets["d"]["scale"].set(preset_data["D"])
            self.param_widgets["s"]["scale"].set(preset_data["S"])
            self.param_widgets["r"]["scale"].set(preset_data["R"])
            
            # Update waveshape
            self.waveshape_var.set(preset_data["waveform"].capitalize())
            
            # Send the preset to the local generator instead of server
            self.synth_generator.load_preset(preset_data)
            print(f"Preset '{preset_name}' loaded successfully")
            
            # Switch to the Synthesizer Configuration tab
            self.notebook.select(self.synth_config_tab)
        else:
            messagebox.showerror("Error", f"Failed to load preset '{preset_name}'")
    
    def on_closing(self):
        """Clean up when window is closed"""
        self.update_active = False
        if hasattr(self, 'update_thread') and self.update_thread.is_alive():
            self.update_thread.join(timeout=1.0)
        self.root.destroy()


def main():
    print("Starting synth application...")
    
    # Create the GUI with local synth generator
    root = tk.Tk()
    app = EnhancedSynthesizerGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI main loop
    root.mainloop()


if __name__ == "__main__":
    main()
