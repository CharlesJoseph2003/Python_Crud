import json
from controller import Controller
from jsonSerializer import JsonSerializer

if __name__ == "__main__":

    controller = Controller()
    while True:
        json_seralizer = JsonSerializer()
        convert_to_json = json_seralizer.serialize(controller)       
        print("\nSynth Preset Manager")
        print("1. Create new preset")
        print("2. List all presets")
        print("3. Update preset")
        print("4. Delete preset")
        print("5. Exit")
        print(type(convert_to_json))
        choice = int(input("Enter choice (1-5): "))

        if choice == 1:
            preset_name = input("Name this preset: ")
            cutoff_freq = input("Enter a cutoff frequency: ")
            resonance = input("Enter a resonance: ")
            amplitude = input("Enter an amplitude: ")
            resistance = input("Enter a resistance: ")
            preset =  controller.create_preset(preset_name,cutoff_freq,resonance,amplitude,resistance)
        if choice == 2:
            print(convert_to_json)
        
        if choice == 3:
            preset = str(input("Enter preset name that you would like to update: "))
            found = False
            for key in convert_to_json:
                if key.get("preset_name")== preset:
                    found = True
                    break
            if not found:
                print('Invalid preset')
                continue
            else:
                print("Enter what you would like to update: ")
                print("1. Cutoff Frequency")
                print("2. Resonance")
                print("3. Amplitude")
                print("4. Resistance")
                choice = int(input("Enter choice 1-4: "))
                if choice not in range(0,4):
                    print("Invalid ")
                    continue
                if choice == 1:
                    cutoff_freq = input("Enter a new cutoff frequency value: ")
                    controller.update_preset(preset, cutoff_freq=cutoff_freq)
                
                if choice == 2:
                    resonance = input("Enter a new resonance value: ")
                    controller.update_preset(preset, resonance=resonance)
                
                if choice == 3:
                    amplitude = input("Enter a new amplitude value: ")
                    controller.update_preset(preset, amplitude=amplitude)
                
                if choice == 4:
                    resistance = input("Enter a new resistance value: ")
                    controller.update_preset(preset, resistance=resistance)
        
        if choice == 4:
            preset = input("Enter what preset name you would like to delete: ")
            controller.delete_preset(preset)

        if choice == 5:
            break

        


        # controller = Controller()
        # preset = controller.create_preset("preset 1", 10, 20, 30, 40)
        # preset2 = controller.create_preset("preset 2", 50,60,70,80)
        # preset3 = controller.create_preset("preset 3", 22, 25, 34, 44)
        # preset4 = controller.create_preset("preset 4", 52,67,78,82)
        # controller.update_preset("preset 2", cutoff_freq=20)
        # controller.delete_preset("preset 2")
        # json_seralizer = JsonSeralizer()
        # convert_to_json = json_seralizer.serialize(controller)
        # print(convert_to_json)
        # print(type(convert_to_json))
    # print(controller.get_data_storage())
    # # controller.delete_preset("preset 2")
    # print(controller.read_preset("preset 2"))