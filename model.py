class SynthConfig:
    def __init__(self, preset_name:str, cutoff_freq:float, resonance:float, A:float, D:float, S:float, R:float):
        self.preset_name = preset_name
        self.cutoff_freq = cutoff_freq
        self.resonance = resonance
        self.A = A
        self.D = D
        self.S = S
        self.R = R
    
    def __repr__(self):
        return (
            f"Preset Name: {self.preset_name}\n"
            f"Cutoff Frequency: {self.cutoff_freq}\n"
            f"Resonance: {self.resonance}\n"
            f"A: {self.A}\n"
            f"D: {self.D}"
            f"S: {self.S}"
            f"R: {self.R}"
        )
    
    def to_dict(self):
        return {
        "preset_name": self.preset_name,  
        "cutoff_freq": self.cutoff_freq,
        "resonance": self.resonance,
        "A": self.A,
        "D": self.D,
        "S": self.R,
        "R": self.R,
    }
    


    

    

