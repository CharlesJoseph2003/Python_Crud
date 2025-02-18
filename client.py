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
        
        # Initialize controller
        self.controller = Controller()
        self.json_serializer = JsonSerializer()
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', padding=6)
        self.style.configure('Custom.TButton', padding=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        # Create tabs
        self.synth_config_tab = ttk.Frame(self.notebook)
        self.current_config_tab = ttk.Frame(self.notebook)
        self.saved_presets_tab = ttk.Frame(self.notebook)
        self.update_preset_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.synth_config_tab, text='Current Synth Configuration')
        self.notebook.add(self.current_config_tab, text='Create Preset')
        self.notebook.add(self.saved_presets_tab, text='Saved Presets')
        self.notebook.add(self.update_preset_tab, text='Update Preset')
        
        self.setup_synth_config_tab()
        self.setup_current_config_tab()
        self.setup_saved_presets_tab()
        self.setup_update_preset_tab()

    def setup_current_config_tab(self):
        # Main container with padding
        main_frame = ttk.Frame(self.current_config_tab)
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)

        # Title
        title_font = Font(family="Arial", size=24, weight="bold")
        title = tk.Label(main_frame, text="Synthesizer Parameters", 
                        font=title_font, bg='#f0f0f0')
        title.pack(pady=(0, 30))

        # Parameters frame
        params_frame = ttk.Frame(main_frame)
        params_frame.pack(fill='x', padx=20)

        # Create parameter entries with labels
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
            # Label (right-aligned)
            label = tk.Label(params_frame, text=label_text, font=param_font,
                           bg='#f0f0f0', anchor='e')
            label.grid(row=i, column=0, padx=(0, 20), pady=10, sticky='e')
            
            # Entry (left-aligned, expands to fill space)
            entry = ttk.Entry(params_frame, font=param_font)
            entry.grid(row=i, column=1, sticky='ew', pady=10)
            
            if param_name == "preset_name":
                self.preset_name_entry = entry
            else:
                self.param_entries[param_name] = entry

        # Save button container for center alignment
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=30)
        
        # Save button
        save_btn = ttk.Button(button_frame, text="Save Preset",
                            command=self.save_preset, style='Custom.TButton')
        save_btn.pack(pady=10)

    def setup_saved_presets_tab(self):
        # Main container
        main_frame = ttk.Frame(self.saved_presets_tab)
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)

        # Title
        title_font = Font(family="Arial", size=24, weight="bold")
        title = tk.Label(main_frame, text="Saved Presets", 
                        font=title_font, bg='#f0f0f0')
        title.pack(pady=(0, 30))

        # Presets listbox with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill='both', expand=True, padx=20)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.presets_listbox = tk.Listbox(list_frame, 
                                         font=("Arial", 11),
                                         selectmode='single',
                                         activestyle='none',
                                         height=10)
        self.presets_listbox.pack(fill='both', expand=True)
        
        # Connect scrollbar
        self.presets_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.presets_listbox.yview)

        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)

        # Buttons with consistent width
        button_width = 15
        ttk.Button(btn_frame, text="Load", command=self.load_preset,
                  width=button_width).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_preset,
                  width=button_width).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_presets,
                  width=button_width).pack(side='left', padx=5)

        # Initial load of presets
        self.refresh_presets()

    def setup_synth_config_tab(self):
        # Main container
        main_frame = ttk.Frame(self.synth_config_tab)
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)

        # Title
        title_font = Font(family="Arial", size=24, weight="bold")
        title = tk.Label(main_frame, text="Synthesizer Parameters", 
                        font=title_font, bg='#f0f0f0')
        title.pack(pady=(0, 30))

        # Parameters frame
        params_frame = ttk.Frame(main_frame)
        params_frame.pack(fill='x', padx=20)

        # Create labels for displaying values
        param_font = Font(family="Arial", size=14, slant="italic")
        value_font = Font(family="Arial", size=14)
        
        params = [
            ("Preset Name:", "preset_name", ""),
            ("Filter Cutoff:", "cutoff_freq", "0.00"),
            ("Resonance:", "resonance", "0.00"),
            ("Amplitude:", "amplitude", "0.00"),
            ("Resistance:", "resistance", "0.00")
        ]

        # Store labels for updating later
        self.param_labels = {}
        
        # Configure grid weights
        params_frame.grid_columnconfigure(1, weight=1)
        
        for i, (label_text, param_name, default_value) in enumerate(params):
            # Parameter label (left side)
            label = tk.Label(params_frame, text=label_text, 
                           font=param_font, bg='#f0f0f0', 
                           anchor='e', width=15)
            label.grid(row=i, column=0, padx=(0, 20), pady=15, sticky='e')
            
            # Value label (right side)
            value_label = tk.Label(params_frame, text=default_value,
                                 font=value_font, bg='#f0f0f0',
                                 anchor='w', width=10)
            value_label.grid(row=i, column=1, pady=15, sticky='w')
            
            self.param_labels[param_name] = value_label

    def update_synth_display(self, preset_data):
        """Update the placeholder tab with the loaded preset values"""
        # Update all parameters
        mapping = {
            'cutoff_freq': 'cutoff_freq',
            'resonance': 'resonance',
            'amplitude': 'amplitude',
            'resistance': 'resistance',
            'preset_name': 'preset_name'
        }
        
        for preset_param, display_param in mapping.items():
            if preset_param in preset_data and display_param in self.param_labels:
                value = preset_data[preset_param]
                if preset_param == 'preset_name':
                    self.param_labels[display_param].config(text=str(value))
                else:
                    self.param_labels[display_param].config(text=f"{float(value):.2f}")

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
        """Refresh the presets list and update dropdown if it exists."""
        try:
            presets = self.json_serializer.serialize(self.controller)
            
            # Update listbox
            self.presets_listbox.delete(0, tk.END)
            for preset in presets:
                self.presets_listbox.insert(tk.END, preset["preset_name"])
            
            # Update dropdown only if it exists
            if hasattr(self, 'preset_dropdown'):
                preset_names = [preset["preset_name"] for preset in presets]
                self.preset_dropdown['values'] = preset_names
                # If there are presets and no current selection, select the first one
                if preset_names and not self.preset_dropdown.get():
                    self.preset_dropdown.set(preset_names[0])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh presets: {str(e)}")

    def setup_update_preset_tab(self):
        # Main container
        main_frame = ttk.Frame(self.update_preset_tab)
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)

        # Title
        title_label = ttk.Label(main_frame, text="Update Preset", font=('Arial', 24, 'bold'))
        title_label.pack(pady=(0, 20))

        # Preset selection
        preset_frame = ttk.Frame(main_frame)
        preset_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(preset_frame, text="Select Preset:").pack(side='left', padx=(0, 10))
        self.preset_dropdown = ttk.Combobox(preset_frame, state='readonly', width=30)
        self.preset_dropdown.pack(side='left')
        
        # Bind selection event
        self.preset_dropdown.bind('<<ComboboxSelected>>', self.on_preset_selected)

        # Parameters frame
        params_frame = ttk.Frame(main_frame)
        params_frame.pack(fill='x')

        # Create entry fields and update buttons for each parameter
        self.update_entries = {}
        row = 0
        for param in ["cutoff_freq", "resonance", "amplitude", "resistance"]:
            param_frame = ttk.Frame(params_frame)
            param_frame.grid(row=row, column=0, pady=5, sticky='ew')
            
            # Parameter label
            ttk.Label(param_frame, text=f"{param.replace('_', ' ').title()}:").pack(side='left', padx=(0, 10))
            
            # Entry field
            entry = ttk.Entry(param_frame, width=15)
            entry.pack(side='left', padx=(0, 10))
            self.update_entries[param] = entry
            
            # Update button
            update_btn = ttk.Button(
                param_frame, 
                text="Update",
                command=lambda p=param: self.update_parameter(p)
            )
            update_btn.pack(side='left')
            
            row += 1
            
        # Initial refresh to populate the dropdown
        self.refresh_presets()

    def on_preset_selected(self, event):
        preset_name = self.preset_dropdown.get()
        try:
            preset = self.controller.get_preset(preset_name)
            # Fill in the current values
            for param_name in self.update_entries:
                if param_name in preset:
                    self.update_entries[param_name].delete(0, tk.END)
                    self.update_entries[param_name].insert(0, f"{float(preset[param_name]):.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load preset: {str(e)}")

    def update_parameter(self, param_name):
        preset_name = self.preset_dropdown.get()
        if not preset_name:
            return

        try:
            new_value = float(self.update_entries[param_name].get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        update_data = {}
        if param_name == "cutoff_freq":
            update_data["cutoff_freq"] = new_value
        elif param_name == "resonance":
            update_data["resonance"] = new_value
        elif param_name == "amplitude":
            update_data["amplitude"] = new_value
        elif param_name == "resistance":
            update_data["resistance"] = new_value

        try:
            result = self.controller.update_preset(preset_name, **update_data)
            if result:
                messagebox.showinfo("Success", f"{param_name} updated successfully!")
                self.refresh_presets()
            else:
                messagebox.showerror("Error", "Failed to update preset!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update preset: {str(e)}")

    def save_preset(self):
        name = self.preset_name_entry.get()
        if not name:
            return

        request = {
            "preset_name": name,
            "cutoff_freq": self.param_entries["cutoff_freq"].get(),
            "resonance": self.param_entries["resonance"].get(),
            "amplitude": self.param_entries["amplitude"].get(),
            "resistance": self.param_entries["resistance"].get()
        }
        
        self.send_create_request(request["preset_name"], request["cutoff_freq"], request["resonance"], request["amplitude"], request["resistance"])

    def load_preset(self):
        selection = self.presets_listbox.curselection()
        if not selection:
            return

        preset_name = self.presets_listbox.get(selection[0])
        try:
            preset = self.controller.get_preset(preset_name)
            # Update the synth display
            self.update_synth_display(preset)
            # Switch to the first tab
            self.notebook.select(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load preset: {str(e)}")

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
