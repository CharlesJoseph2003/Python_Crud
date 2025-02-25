import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from controller import Controller
from jsonSerializer import JsonSerializer

class SynthesizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Synthesizer")
        self.root.geometry("800x480")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize controller and serializer
        self.controller = Controller()
        self.json_serializer = JsonSerializer()
        
        # To track the popup keyboard and target entry
        self.keyboard_popup = None
        self.current_target = None
        self.keyboard_display_var = None
        self.ignore_keyboard = False  # Flag to temporarily ignore focus events
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', padding=6)
        self.style.configure('Custom.TButton', padding=10)
        
        # Create notebook for tabs: Consolidated config tab and Saved Presets tab
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        self.synth_config_tab = ttk.Frame(self.notebook)
        self.saved_presets_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.synth_config_tab, text='Synthesizer Configuration')
        self.notebook.add(self.saved_presets_tab, text='Saved Presets')
        
        self.setup_synth_config_tab()
        self.setup_saved_presets_tab()
    
    def setup_synth_config_tab(self):
        # Main container with padding
        main_frame = ttk.Frame(self.synth_config_tab)
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Title label
        title_font = Font(family="Arial", size=24, weight="bold")
        title = tk.Label(main_frame, text="Synthesizer Parameters", font=title_font, bg='#f0f0f0')
        title.pack(pady=(0, 30))
        
        # Parameters frame: create editable entry fields for each parameter
        params_frame = ttk.Frame(main_frame)
        params_frame.pack(fill='x', padx=20)
        
        param_font = Font(family="Arial", size=12)
        params = [
            ("Preset Name:", "preset_name"),
            ("Filter Cutoff:", "cutoff_freq"),
            ("Resonance:", "resonance"),
            ("Amplitude:", "amplitude"),
            ("Resistance:", "resistance")
        ]
        
        # Configure grid column weights
        params_frame.grid_columnconfigure(1, weight=1)
        self.param_entries = {}
        
        for i, (label_text, param_name) in enumerate(params):
            label = tk.Label(params_frame, text=label_text, font=param_font,
                             bg='#f0f0f0', anchor='e')
            label.grid(row=i, column=0, padx=(0, 20), pady=10, sticky='e')
            
            entry = ttk.Entry(params_frame, font=param_font)
            entry.grid(row=i, column=1, sticky='ew', pady=10)
            # Bind mouse click to open the virtual keyboard
            entry.bind("<Button-1>", lambda event, e=entry: self.create_virtual_keyboard(e))
            
            if param_name == "preset_name":
                self.preset_name_entry = entry
            else:
                self.param_entries[param_name] = entry
                entry.insert(0, "0.00")
        
        # Button frame with two buttons: one for creating a new preset and one for updating
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=30)
        
        create_btn = ttk.Button(button_frame, text="Create Preset", 
                                command=self.create_preset_from_entries, style='Custom.TButton')
        create_btn.pack(side='left', padx=10)
        
        update_btn = ttk.Button(button_frame, text="Update Preset", 
                                command=self.update_preset_from_entries, style='Custom.TButton')
        update_btn.pack(side='left', padx=10)
    
    def setup_saved_presets_tab(self):
        # Main container for saved presets
        main_frame = ttk.Frame(self.saved_presets_tab)
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        title_font = Font(family="Arial", size=24, weight="bold")
        title = tk.Label(main_frame, text="Saved Presets", font=title_font, bg='#f0f0f0')
        title.pack(pady=(0, 30))
        
        # Listbox for displaying presets with a scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill='both', expand=True, padx=20)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.presets_listbox = tk.Listbox(list_frame, font=("Arial", 11),
                                          selectmode='single', activestyle='none', height=10)
        self.presets_listbox.pack(fill='both', expand=True)
        self.presets_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.presets_listbox.yview)
        
        # Buttons for loading, deleting, and refreshing presets
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        button_width = 15
        ttk.Button(btn_frame, text="Load", command=self.load_preset, width=button_width).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_preset, width=button_width).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_presets, width=button_width).pack(side='left', padx=5)
        
        self.refresh_presets()
    
    def create_virtual_keyboard(self, target_entry):
        # Only open keyboard if not ignoring events
        if self.ignore_keyboard:
            return
        # Close any existing keyboard popup before creating a new one
        if self.keyboard_popup is not None:
            self.keyboard_popup.destroy()
        
        self.current_target = target_entry
        
        # Create a full-screen keyboard popup
        self.keyboard_popup = tk.Toplevel(self.root)
        self.keyboard_popup.title("Virtual Keyboard")
        self.keyboard_popup.geometry("800x480")
        
        # Create a display textbox at the top to show current entry value
        self.keyboard_display_var = tk.StringVar(value=self.current_target.get())
        display_entry = ttk.Entry(self.keyboard_popup, textvariable=self.keyboard_display_var,
                                  font=("Arial", 16), state="readonly", justify="center")
        display_entry.pack(fill='x', padx=10, pady=10)
        
        # Frame for keyboard buttons
        kb_frame = ttk.Frame(self.keyboard_popup, padding=5)
        kb_frame.pack(expand=True, fill='both')
        
        # Define keyboard rows (letters and digits) with special keys
        keys = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M"],
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
            ["Space", "Backspace", "Clear", "Done"]
        ]
        
        for r, row_keys in enumerate(keys):
            for c, key in enumerate(row_keys):
                action = lambda char=key: self.on_keyboard_key(char)
                btn = ttk.Button(kb_frame, text=key, command=action)
                btn.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
        
        # Make the grid cells expand evenly
        for i in range(len(keys)):
            kb_frame.rowconfigure(i, weight=1)
        for i in range(max(len(row) for row in keys)):
            kb_frame.columnconfigure(i, weight=1)
        
        # When closing the window, ensure the keyboard popup is properly reset.
        self.keyboard_popup.protocol("WM_DELETE_WINDOW", self.close_keyboard)
    
    def on_keyboard_key(self, key):
        # Handle special keys first
        if key == "Space":
            self.current_target.insert(tk.END, " ")
        elif key == "Backspace":
            current_text = self.current_target.get()
            if current_text:
                self.current_target.delete(len(current_text)-1, tk.END)
        elif key == "Clear":
            self.current_target.delete(0, tk.END)
        elif key == "Done":
            self.close_keyboard()
            return
        else:
            self.current_target.insert(tk.END, key)
        
        # Update the display textbox with the new entry content
        self.keyboard_display_var.set(self.current_target.get())
    
    def close_keyboard(self):
        if self.keyboard_popup is not None:
            self.keyboard_popup.destroy()
            self.keyboard_popup = None
            self.current_target = None
            # Set flag to ignore immediate focus events, then reset after 300ms.
            self.ignore_keyboard = True
            self.root.after(300, lambda: setattr(self, 'ignore_keyboard', False))
    
    def load_preset(self):
        selection = self.presets_listbox.curselection()
        if not selection:
            return
        
        preset_name = self.presets_listbox.get(selection[0])
        try:
            preset = self.controller.get_preset(preset_name)
            # Update the entry fields with the loaded preset values
            self.preset_name_entry.delete(0, tk.END)
            self.preset_name_entry.insert(0, preset.get("preset_name", ""))
            for key in self.param_entries:
                self.param_entries[key].delete(0, tk.END)
                value = preset.get(key, "0.00")
                try:
                    self.param_entries[key].insert(0, f"{float(value):.2f}")
                except:
                    self.param_entries[key].insert(0, value)
            # When switching tabs, force focus away from the entry fields.
            self.notebook.focus_set()
            self.notebook.select(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load preset: {str(e)}")
    
    def create_preset_from_entries(self):
        name = self.preset_name_entry.get()
        if not name:
            messagebox.showerror("Error", "Preset name is required!")
            return
        try:
            cutoff = float(self.param_entries["cutoff_freq"].get())
            resonance = float(self.param_entries["resonance"].get())
            amplitude = float(self.param_entries["amplitude"].get())
            resistance = float(self.param_entries["resistance"].get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for parameters!")
            return
        
        self.send_create_request(name, cutoff, resonance, amplitude, resistance)
    
    def update_preset_from_entries(self):
        name = self.preset_name_entry.get()
        if not name:
            messagebox.showerror("Error", "Preset name is required for update!")
            return
        try:
            cutoff = float(self.param_entries["cutoff_freq"].get())
            resonance = float(self.param_entries["resonance"].get())
            amplitude = float(self.param_entries["amplitude"].get())
            resistance = float(self.param_entries["resistance"].get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for parameters!")
            return
        
        self.send_update_request(name, cutoff, resonance, amplitude, resistance)
    
    def send_create_request(self, preset_name, cutoff_freq, resonance, amplitude, resistance):
        try:
            self.controller.create_preset(preset_name, cutoff_freq, resonance, amplitude, resistance)
            messagebox.showinfo("Success", "Preset created successfully!")
            self.refresh_presets()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create preset: {str(e)}")
    
    def send_update_request(self, preset_name, cutoff_freq=None, resonance=None, amplitude=None, resistance=None):
        try:
            result = self.controller.update_preset(preset_name, cutoff_freq, resonance, amplitude, resistance)
            if result:
                messagebox.showinfo("Success", "Preset updated successfully!")
                self.refresh_presets()
            else:
                messagebox.showerror("Error", "Preset not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update preset: {str(e)}")
    
    def send_delete_request(self, preset_name):
        try:
            result = self.controller.delete_preset(preset_name)
            if result:
                messagebox.showinfo("Success", "Preset deleted successfully!")
                self.refresh_presets()
            else:
                messagebox.showerror("Error", "Preset not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete preset: {str(e)}")
    
    def refresh_presets(self):
        try:
            presets = self.json_serializer.serialize(self.controller)
            self.presets_listbox.delete(0, tk.END)
            for preset in presets:
                self.presets_listbox.insert(tk.END, preset["preset_name"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh presets: {str(e)}")
    
    def delete_preset(self):
        selection = self.presets_listbox.curselection()
        if not selection:
            return
        
        preset_name = self.presets_listbox.get(selection[0])
        self.send_delete_request(preset_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = SynthesizerGUI(root)
    root.mainloop()
