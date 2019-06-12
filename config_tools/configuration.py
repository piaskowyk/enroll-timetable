import json


class Configuration:
    # class of configuration data

    # loads configuration from JSON file from provided path
    def __init__(self, filepath):
        self.data = None
        with open(filepath) as json_file:
            self.data = json.load(json_file)
