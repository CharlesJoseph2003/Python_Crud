class SynthConfig:
    def __init__(self, preset_name:str, cutoff_freq:float, resonance:float, amplitude:float, resistance:float):
        self.preset_name = preset_name
        self.cutoff_freq = cutoff_freq
        self.resonance = resonance
        self.amplitude = amplitude
        self.resistance = resistance
    
    def __repr__(self):
        return (
            f"Preset Name: {self.preset_name}\n"
            f"Cutoff Frequency: {self.cutoff_freq}\n"
            f"Resonance: {self.resonance}\n"
            f"Amplitude: {self.amplitude}\n"
            f"Resistance: {self.resistance}"
        )
    
    def to_dict(self):
        return {
        "preset_name": self.preset_name,  
        "cutoff_frequency": self.cutoff_freq,
        "resonance": self.resonance,
        "amplitude": self.amplitude,
        "resistance": self.resistance,
    }
    


    

    

