from model import SynthConfig
class Controller:
    def __init__(self):
        self.data_storage = [] #need to create a list to store the data temporaraly 
    
    def create_preset(self, preset_name, cutoff_freq, resonance, amplitude, resistance):
        data = SynthConfig(preset_name, cutoff_freq, resonance, amplitude, resistance) #need to make a synthconfig object that is then appended
        #to the data storage
        self.data_storage.append(data)
        return data

    def read_preset(self, preset_name):      
        for data in self.data_storage:
            if data.preset_name == preset_name:
                return data
        return None

    
    def update_preset(self, preset_name, cutoff_freq=None, resonance=None, amplitude=None, resistance=None):
        #need to pass the preset name and the new values
        #then have to loop through the storage and find the preset name and then update the values for that preset
        #return the updated data
        for data in self.data_storage:
            if data.preset_name == preset_name:
                if cutoff_freq: 
                    data.cutoff_freq = cutoff_freq
                if resonance: 
                    data.resonance = resonance
                if amplitude: 
                    data.amplitude = amplitude
                if resistance: 
                    data.resistance = resistance
                return data #returning the updated data
        return None #if preset is not found, then return None
    
    def delete_preset(self, preset_name):
        for data in self.data_storage:
            if data.preset_name == preset_name:
                self.data_storage.remove(data)
                return data
        return None

    def get_data_storage(self):
        return self.data_storage
    


if __name__ == "__main__":
    controller = Controller()
    preset = controller.create_preset("preset 1", 10, 20, 30, 40)
    preset2 = controller.create_preset("preset 2", 50,60,70,80)
    controller.update_preset("preset 2", cutoff_freq=20)
    controller.delete_preset("preset 2")
    print(controller.get_data_storage())
    # controller.delete_preset("preset 2")
    print(controller.read_preset("preset 2"))