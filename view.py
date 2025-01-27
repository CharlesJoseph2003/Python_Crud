import tkinter as tk
from tkinter import ttk

example_presets = ["Preset 1", "Preset 2", "Preset 3"]
parameters = [
    "Oscillator 1 Freq", "Oscillator 2 Freq", "Filter Cutoff", 
    "Resonance", "Attack", "Decay", "Sustain", "Release"
]

# Create the main window
root = tk.Tk()
root.title("Synthesizer")
root.geometry("800x400")

# Create a Notebook widget (for tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Tab 1: Current Synth Configuration Tab
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Current Synth Configuration")

current_config_label = ttk.Label(frame1, text="Synthesizer Parameters", font=("Arial", 30, "bold"))
current_config_label.pack(pady=10)

# Frame for parameter columns
param_frame = ttk.Frame(frame1)
param_frame.pack(pady=10)

# Left and right columns
left_column = ttk.Frame(param_frame)
left_column.grid(row=0, column=0, padx=20)

right_column = ttk.Frame(param_frame)
right_column.grid(row=0, column=1, padx=20)

# Split parameters into two groups
left_params = parameters[:len(parameters)//2]
right_params = parameters[len(parameters)//2:]

# Add parameters to the left column
for row, param in enumerate(left_params):
    param_label = ttk.Label(left_column, text=f"{param}:", font=("Arial", 20, "italic"))
    param_label.grid(row=row, column=0, sticky="w", pady=5, padx=5)  # Label in column 0
    value_label = ttk.Label(left_column, text="0.00", font=("Arial", 20))
    value_label.grid(row=row, column=1, sticky="w", pady=5, padx=5)  # Value in column 1

# Add parameters to the right column
for row, param in enumerate(right_params):
    param_label = ttk.Label(right_column, text=f"{param}:", font=("Arial", 20, "italic"))
    param_label.grid(row=row, column=0, sticky="w", pady=5, padx=5)  # Label in column 0
    value_label = ttk.Label(right_column, text="0.00", font=("Arial", 20))
    value_label.grid(row=row, column=1, sticky="w", pady=5, padx=5)  # Value in column 1

# Save button FIXME: Add functionality
save_button = ttk.Button(frame1, text="Save")
save_button.pack(pady=20)

# Tab 2: Saved Presets Tab
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text="Saved Presets")

presets_label = ttk.Label(frame2, text="Saved Presets", font=("Arial", 30, "bold"))
presets_label.pack(pady=10)

# Listbox to display saved presets
preset_listbox = tk.Listbox(frame2, width=40, height=10)
preset_listbox.pack(pady=10)

# Add example presets to the listbox
for preset in example_presets:
    preset_listbox.insert(tk.END, preset)

# Buttons for presets
button_frame = ttk.Frame(frame2)
button_frame.pack(pady=10)

load_button = ttk.Button(button_frame, text="Load")
load_button.grid(row=0, column=0, padx=10)

delete_button = ttk.Button(button_frame, text="Delete")
delete_button.grid(row=0, column=1, padx=10)

# Tab 3: Placeholder Tab
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text="Placeholder")

placeholder_label = ttk.Label(frame3, text="More content coming soon!", font=("Arial", 12))
placeholder_label.pack(pady=20)

# Run the main loop
root.mainloop()
