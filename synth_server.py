from flask import Flask, jsonify, request
import random
import time
import json

app = Flask(__name__)

# Global variable to store current preset data
current_preset = None
use_preset = False

def save_current_config(config):
    with open('current.json', 'w') as f:
        json.dump(config, f, indent=4)

def generate_synth_config():
    global current_preset, use_preset
    
    # If a preset has been loaded, use it instead of random values
    if use_preset and current_preset:
        # Reset the flag after using once to return to random values unless loaded again
        use_preset = False
        config = current_preset
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
    
    # Save the current configuration to file
    save_current_config(config)
    return config

@app.route('/current_config')
def get_current_config():
    return jsonify(generate_synth_config())

@app.route('/load_preset', methods=['POST'])
def load_preset():
    global current_preset, use_preset
    
    # Get the preset data from the request
    preset_data = request.get_json()
    
    if preset_data:
        current_preset = preset_data
        use_preset = True
        return jsonify({"status": "success", "message": "Preset loaded"})
    else:
        return jsonify({"status": "error", "message": "Invalid preset data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
