from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

def generate_synth_config():
    return {
        "cutoff_freq": round(random.uniform(20, 200), 1),
        "resonance": round(random.uniform(0.5, 6.0), 1),
        "amplitude": round(random.uniform(0.1, 1.0), 1),
        "resistance": round(random.uniform(20, 60), 1)
    }

@app.route('/current_config')
def get_current_config():
    return jsonify(generate_synth_config())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
