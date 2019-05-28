import json


class Configuration:
    data = 0

    def __init__(self, filepath):
        with open(filepath) as json_file:
            self.data = json.load(json_file)
