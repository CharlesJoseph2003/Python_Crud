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
        
        self.controller = Controller()
        self.json_serializer = JsonSerializer()
        
        # Initialize style
        self.style = ttk.Style(self.root)
        self.style.theme_use('default')
        
        # -- OPTIONAL STYLE TWEAKS FOR NOTEBOOK, FRAMES, BUTTONS --
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', padding=6)
        self.style.configure('Custom.TButton', padding=10)
        
        # -- CUSTOM SEGMENTED STYLE FOR WAVESHAPE (DISABLED) --
        self.style.configure(
            "Segmented.TFrame",
            background="#FFFFFF",
            borderwidth=1,
            relief="solid"
        )
        self.style.configure(
            "Segmented.TRadiobutton",
            indicatoron=0,    # Hide the typical round radio indicator
            padding=(10, 5),  # Some internal padding
            background="#FFFFFF",
            relief="flat"
        )
        # For the disabled state, we map the background to keep it white
        # so that the buttons don't appear "greyed out".
        self.style.map(
            "Segmented.TRadiobutton",
            background=[
                ("disabled", "#FFFFFF"),   # Keep background white even when disabled
                ("active", "#E0E0E0"),     # Hover
                ("selected", "#FFFFFF")    # Selected background
            ],
            foreground=[
                ("disabled", "gray"),      # Optional: grey text if desired
                ("selected", "black")
            ],
            relief=[
                ("disabled", "flat"),
                ("pressed", "sunken"),
                ("active", "groove")
            ]
        )
        
        # Waveshape variable for display only; default is "Square"
        self.waveshape_var = tk.StringVar(value="Square")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        self.synth_config_tab = ttk.Frame(self.notebook)
        self.saved_presets_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.synth_config_tab, text='Synthesizer Configuration')
        self.notebook.add(self.saved_presets_tab, text='Saved Presets')
        
        self.setup_synth_config_tab()
        self.setup_saved_presets_tab()
    
    def setup_synth_config_tab(self):
        main_frame = ttk.Frame(self.synth_config_tab)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Title label
        title_font = Font(family="Arial", size=20, weight="bold")
        title = tk.Label(main_frame, text="Synthesizer Parameters", font=title_font, bg='#f0f0f0')
        title.pack(pady=(0, 10))
        
        # Preset Name Row (editable with virtual keyboard)
        preset_frame = ttk.Frame(main_frame)
        preset_frame.pack(fill='x', padx=10, pady=5)
        preset_label = tk.Label(preset_frame, text="Preset Name:", font=("Arial", 10), bg='#f0f0f0')
        preset_label.pack(side='left', padx=(0,5))
        
        self.preset_name_entry = ttk.Entry(preset_frame, font=("Arial", 10))
        self.preset_name_entry.pack(side='left', fill='x', expand=True)
        self.preset_name_entry.bind("<Button-1>", lambda event, e=self.preset_name_entry: self.create_virtual_keyboard(e))
        
        # Parameters Frame with vertical scales arranged horizontally
        params_frame = ttk.Frame(main_frame)
        params_frame.pack(fill='both', padx=10, pady=10)
        
        # Updated list of parameters: (Display Name, key)
        params = [
            ("Cutoff", "cutoff"),
            ("Resonance", "resonance"),
            ("A", "a"),
            ("D", "d"),
            ("S", "s"),
            ("R", "r")
        ]
        
        self.param_widgets = {}
        for display_name, key in params:
            sub_frame = ttk.Frame(params_frame)
            sub_frame.pack(side='left', padx=10, fill='y', expand=True)
            
            # Label above the scale
            label = tk.Label(sub_frame, text=display_name, font=("Arial", 10), bg='#f0f0f0')
            label.pack(side='top', pady=(0,5))
            
            # Vertical scale (disabled so the user cannot interact)
            scale = tk.Scale(sub_frame, from_=0, to=100, orient=tk.VERTICAL, state='disabled',
                             showvalue=True, length=200)
            scale.pack(side='top')
            
            self.param_widgets[key] = {"scale": scale, "label": label}
        
        # WAVESHAPE: segmented control style (DISABLED)
        waveshape_container = ttk.Frame(main_frame)
        waveshape_container.pack(fill='x', padx=10, pady=(0, 10))
        
        # Optional label to identify the parameter
        waveshape_label = tk.Label(
            waveshape_container, text="Waveshape:", font=("Arial", 10), bg='#f0f0f0'
        )
        waveshape_label.pack(side='left', padx=(0,5))
        
        # Frame that holds the segmented radio buttons
        segmented_frame = ttk.Frame(waveshape_container, style="Segmented.TFrame")
        segmented_frame.pack(side='left', fill='x', expand=True)
        
        # Create the four segmented radio buttons, all disabled
        options = ["Square", "Triangle", "Sine", "Saw"]
        for idx, option in enumerate(options):
            rb = ttk.Radiobutton(
                segmented_frame,
                text=option,
                value=option,
                variable=self.waveshape_var,
                style="Segmented.TRadiobutton",
                state="disabled"  # Make the button non-interactive
            )
            rb.grid(row=0, column=idx, sticky="nsew")
            segmented_frame.columnconfigure(idx, weight=1)
        
        # Action buttons frame (Create / Update Preset)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=5)
        
        create_btn = ttk.Button(button_frame, text="Create Preset", 
                                command=self.create_preset_from_entries, style='Custom.TButton')
        create_btn.pack(side='left', padx=5, expand=True, fill='x')
        
        update_btn = ttk.Button(button_frame, text="Update Preset", 
                                command=self.update_preset_from_entries, style='Custom.TButton')
        update_btn.pack(side='left', padx=5, expand=True, fill='x')
    
    def setup_saved_presets_tab(self):
        main_frame = ttk.Frame(self.saved_presets_tab)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        title_font = Font(family="Arial", size=20, weight="bold")
        title = tk.Label(main_frame, text="Saved Presets", font=title_font, bg='#f0f0f0')
        title.pack(pady=(0, 10))
        
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.presets_listbox = tk.Listbox(list_frame, font=("Arial", 10),
                                          selectmode='single', activestyle='none', height=10)
        self.presets_listbox.pack(fill='both', expand=True)
        self.presets_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.presets_listbox.yview)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=5)
        
        button_width = 10
        ttk.Button(btn_frame, text="Load", command=self.load_preset, width=button_width).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_preset, width=button_width).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_presets, width=button_width).pack(side='left', padx=5)
        
        self.refresh_presets()
    
    def create_virtual_keyboard(self, target_entry):
        if getattr(self, 'ignore_keyboard', False):
            return
        if self.keyboard_popup is not None:
            self.keyboard_popup.destroy()
        self.current_target = target_entry
        self.keyboard_popup = tk.Toplevel(self.root)
        self.keyboard_popup.title("Virtual Keyboard")
        self.keyboard_popup.geometry("800x250")
        self.keyboard_display_var = tk.StringVar(value=self.current_target.get())
        display_entry = ttk.Entry(self.keyboard_popup, textvariable=self.keyboard_display_var,
                                  font=("Arial", 16), state="readonly", justify="center")
        display_entry.pack(fill='x', padx=10, pady=10)
        
        kb_frame = ttk.Frame(self.keyboard_popup, padding=5)
        kb_frame.pack(expand=True, fill='both')
        
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
        for i in range(len(keys)):
            kb_frame.rowconfigure(i, weight=1)
        for i in range(max(len(row) for row in keys)):
            kb_frame.columnconfigure(i, weight=1)
        
        self.keyboard_popup.protocol("WM_DELETE_WINDOW", self.close_keyboard)
    
    def on_keyboard_key(self, key):
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
        self.keyboard_display_var.set(self.current_target.get())
    
    def close_keyboard(self):
        if self.keyboard_popup is not None:
            self.keyboard_popup.destroy()
            self.keyboard_popup = None
            self.current_target = None
            self.ignore_keyboard = True
            self.root.after(300, lambda: setattr(self, 'ignore_keyboard', False))
    
    def load_preset(self):
        selection = self.presets_listbox.curselection()
        if not selection:
            return
        preset_name = self.presets_listbox.get(selection[0])
        try:
            preset = self.controller.get_preset(preset_name)
            
            # Update preset name
            self.preset_name_entry.delete(0, tk.END)
            self.preset_name_entry.insert(0, preset.get("preset_name", ""))
            
            # Update each scale
            for key in self.param_widgets:
                value = preset.get(key, "0.00")
                try:
                    float_val = float(value)
                except:
                    float_val = 0.0
                self.param_widgets[key]['scale'].config(state='normal')
                self.param_widgets[key]['scale'].set(float_val)
                self.param_widgets[key]['scale'].config(state='disabled')
            
            # Update the waveshape display (defaults to "Square" if not present)
            self.waveshape_var.set(preset.get("waveshape", "Square"))
            
            self.notebook.focus_set()
            self.notebook.select(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load preset: {str(e)}")
    
    def create_preset_from_entries(self):
        """
        The user can set name and numeric parameters, but waveshape is read-only.
        We do NOT send waveshape to the controller because the user can't set it.
        """
        name = self.preset_name_entry.get()
        if not name:
            messagebox.showerror("Error", "Preset name is required!")
            return
        try:
            cutoff = self.param_widgets["cutoff"]['scale'].get()
            resonance = self.param_widgets["resonance"]['scale'].get()
            a = self.param_widgets["a"]['scale'].get()
            d = self.param_widgets["d"]['scale'].get()
            s = self.param_widgets["s"]['scale'].get()
            r = self.param_widgets["r"]['scale'].get()
        except Exception:
            messagebox.showerror("Error", "Error retrieving parameter values!")
            return
        
        # The user can't choose waveshape here, so we won't pass it.
        self.send_create_request(name, cutoff, resonance, a, d, s, r)
    
    def update_preset_from_entries(self):
        """
        The user can update name and numeric parameters, but waveshape is read-only.
        We do NOT send waveshape to the controller because the user can't set it.
        """
        name = self.preset_name_entry.get()
        if not name:
            messagebox.showerror("Error", "Preset name is required for update!")
            return
        try:
            cutoff = self.param_widgets["cutoff"]['scale'].get()
            resonance = self.param_widgets["resonance"]['scale'].get()
            a = self.param_widgets["a"]['scale'].get()
            d = self.param_widgets["d"]['scale'].get()
            s = self.param_widgets["s"]['scale'].get()
            r = self.param_widgets["r"]['scale'].get()
        except Exception:
            messagebox.showerror("Error", "Error retrieving parameter values!")
            return
        
        self.send_update_request(name, cutoff, resonance, a, d, s, r)
    
    def send_create_request(self, preset_name, cutoff, resonance, a, d, s, r):
        try:
            # Not passing waveshape, as it's read-only from the user's perspective
            self.controller.create_preset(preset_name, cutoff, resonance, a, d, s, r)
            messagebox.showinfo("Success", "Preset created successfully!")
            self.refresh_presets()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create preset: {str(e)}")
    
    def send_update_request(self, preset_name, cutoff=None, resonance=None,
                            a=None, d=None, s=None, r=None):
        try:
            # Not passing waveshape, as it's read-only from the user's perspective
            result = self.controller.update_preset(preset_name, cutoff, resonance, a, d, s, r)
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
