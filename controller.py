import json
from model import SynthConfig

class Controller:
    def __init__(self, file_path="presets.json"):
        self.data_storage = []  # Temporary storage for presets
        self.file_path = file_path  # Path to the file for saving/loading
        self.load_from_file(self.file_path)  # Load existing data if the file exists

    def create_preset(self, preset_name, cutoff_freq, resonance, A, D,S,R):
        data = SynthConfig(preset_name, cutoff_freq, resonance, A, D,S,R)
        self.data_storage.append(data)
        self.save_to_file(self.file_path)  # Save after creating
        return data

    def read_preset(self, preset_name):
        for data in self.data_storage:
            if data.preset_name == preset_name:
                return data
        return None

    def update_preset(self, preset_name, cutoff_freq=None, resonance=None, A=None, D=None, S=None, R=None):
        """Update a preset with new parameter values."""
        for data in self.data_storage:
            if data.preset_name == preset_name:
                if cutoff_freq is not None:
                    data.cutoff_freq = float(cutoff_freq)
                if resonance is not None:
                    data.resonance = float(resonance)
                if A is not None:
                    data.A = float(A)
                if D is not None:
                    data.D = float(D)
                if S is not None:
                    data.S = float(S)
                if R is not None:
                    data.R = float(D)
                self.save_to_file(self.file_path)  # Save after updating
                return True
        return False

    def delete_preset(self, preset_name):
        for data in self.data_storage:
            if data.preset_name == preset_name:
                self.data_storage.remove(data)
                self.save_to_file(self.file_path)  # Save after deleting
                return data
        return None

    def get_data_storage(self):
        return self.data_storage

    def initialize_defaults(self):
        """Add premade presets to data_storage."""
        self.create_preset("Default Bass", 100, 1.0, 0.8, 50, 20, 30)
        self.create_preset("Default Lead", 200, 0.5, 0.9, 40, 15, 20)
        self.create_preset("Default Pad", 150, 0.7, 0.6, 60, 30, 40)

    def save_to_file(self, file_path):
        """Save the data_storage to a file in JSON format."""
        with open(file_path, "w") as file:
            json_data = [data.to_dict() for data in self.data_storage]
            json.dump(json_data, file, indent=4)

    def load_from_file(self, file_path):
        """Load data_storage from a file."""
        try:
            with open(file_path, "r") as file:
                json_data = json.load(file)
                self.data_storage = [SynthConfig(**preset) for preset in json_data]
        except FileNotFoundError:
            print(f"File '{file_path}' not found. Starting with empty storage.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from '{file_path}'. Starting with empty storage.")

    def get_preset(self, preset_name):
        """Get a preset by name and return it as a dictionary."""
        preset = self.read_preset(preset_name)
        if preset:
            return {
                "preset_name": preset.preset_name,
                "cutoff_freq": preset.cutoff_freq,
                "resonance": preset.resonance,
                "A": preset.A,
                "D": preset.D,
                "S":preset.S,
                "R":preset.R
            }
        return None


if __name__ == "__main__":
    controller = Controller()
    controller.initialize_defaults()
    preset = controller.create_preset("preset 1", 10, 20, 30, 40)
    preset2 = controller.create_preset("preset 2", 50,60,70,80)
    controller.update_preset("preset 2", cutoff_freq=20)
    # controller.delete_preset("preset 2")
    # print(controller.get_data_storage())
    # controller.delete_preset("preset 2")
    # print(controller.read_preset("preset 2"))