from openpyxl import load_workbook


class Load:

    @staticmethod
    def exec_command(args):
        if len(args) < 2:
            print("Error: not enough arguments, must insert file name to load.")
            return None
        return load_workbook(filename='data/data.xlsx')
