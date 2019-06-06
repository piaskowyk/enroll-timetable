from openpyxl import load_workbook

from config_tools.configuration import Configuration
from interface_tools.command_completion_tools import available_expressions
from spreadsheet_data.spreadsheet_data import SpreadsheetData


class Load:

    @staticmethod
    def exec_command(args):
        if len(args) < 2:
            print("Error: not enough arguments, must insert file name to load.")
            return None
        _workbook = load_workbook(filename=args[1])
        configuration = Configuration(filepath="config.json")
        data = SpreadsheetData(configuration.data, _workbook)

        available_expressions['free']['-r'] = data.room_data.data

        return data
