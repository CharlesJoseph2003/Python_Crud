from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

def generate_synth_config():
    waveforms = ["square", "triangle", "sine", "saw"]
    return {
        "cutoff_freq": round(random.uniform(20, 200), 5),
        "resonance": round(random.uniform(0.5, 6.0), 5),
        "A": round(random.uniform(0.1, 1.0), 5),
        "D": round(random.uniform(20, 60), 5),
        "S": round(random.uniform(20, 60), 5),
        "R": round(random.uniform(20, 60), 5),
        "waveform": random.choice(waveforms)
    }

@app.route('/current_config')
def get_current_config():
    return jsonify(generate_synth_config())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
