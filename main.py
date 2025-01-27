from controller import Controller
from jsonSerializer import JsonSeralizer

if __name__ == "__main__":
    controller = Controller()
    preset = controller.create_preset("preset 1", 10, 20, 30, 40)
    preset2 = controller.create_preset("preset 2", 50,60,70,80)
    preset3 = controller.create_preset("preset 3", 22, 25, 34, 44)
    preset4 = controller.create_preset("preset 4", 52,67,78,82)
    controller.update_preset("preset 2", cutoff_freq=20)
    controller.delete_preset("preset 2")
    json_seralizer = JsonSeralizer()
    convert_to_json = json_seralizer.serialize(controller)
    print(convert_to_json)
    print(type(convert_to_json))
    # print(controller.get_data_storage())
    # # controller.delete_preset("preset 2")
    # print(controller.read_preset("preset 2"))