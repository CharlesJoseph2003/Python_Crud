import json
class JsonSerializer:
    def __init__(self):
        pass

    def serialize(self, controller_instance):
        data_storage = controller_instance.get_data_storage()
        dict_list = []
        for data in data_storage:
            dict_data = data.to_dict()
            dict_list.append(dict_data)
        return dict_list  # Return the list of dictionaries directly
        