import json
class JsonSeralizer:
    def __init__(self):
        pass

    def serialize (self, controller_instance):
        data_storage = controller_instance.get_data_storage()
        dict_list = []
        for data in data_storage:
            dict_data = data.to_dict()
            dict_list.append(dict_data)
        json_output = json.dumps(dict_list)
        return json_output
        