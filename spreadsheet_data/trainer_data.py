from spreadsheet_data.common_data import *
from spreadsheet_tools.sheet_data_importer import SpreadsheetDataImporter

positions = dict()
degrees = {'0': 'Undefined degree',
           'dr hab.': 'Habilitated doctor',
           'dr': 'Doctor',
           'inż.': 'Engineer',
           'mgr': 'Master\'s degree',
           'prof.': 'Professor'}


class TrainerInfo:
    first_name = ''
    last_name = ''
    department_id = 0
    position = ''
    degree = ''
    extra_info = ''
    pensum = 0
    pensum_discount = 0
    email = ''
    consult_room = ''
    consult_time = 0
    comments = ""
    referenced_by = dict()

    def __init__(self, record, department_data, requester_data):
        self.referenced_by = dict()
        self.first_name = record['name'].split()[-1]
        self.last_name = ''.join(record['name'].split()[0: -1])
        self.position = record['position']
        positions[self.position] = self.position
        self.degree = record['degree']
        self.extra_info = record['extraInfo']
        self.pensum = record['pensum']
        self.pensum_discount = record['pensumDiscount']
        self.email = record['email']
        self.consult_room = record['consultationsRoom']
        if record['consultationsDay'] is None or \
                record['consultationsHours'] is None:
            self.consult_time = 0
        else:
            split_value = record['consultationsHours'].split('-')
            first = split_value[0]
            second = None
            if len(split_value) > 1:
                second = split_value[1]
            self.consult_time = WeeklyTimePeriod(record['consultationsDay'],
                                                 first,
                                                 second)
        self.comments = record['comments']
        self.department_id = department_data.get_department_id(
            record['departmentName'], requester_data, self.get_key())

    def get_key(self):
        return str(self.last_name) + ' ' + str(self.first_name)

    def add_reference(self, requester_data, requester_key):
        if id(requester_data) not in self.referenced_by:
            self.referenced_by[id(requester_data)] = []
        self.referenced_by[id(requester_data)].append(requester_key)


class TrainerData:
    data = dict()

    def __init__(self, config, workbook, department_data):
        trainer_data_importer = SpreadsheetDataImporter(config, workbook,
                                                        "trainers")
        cur_record = trainer_data_importer.load_next_record()
        while len(cur_record) > 0:
            cur_trainer = TrainerInfo(cur_record, department_data, self)
            self.data[str(cur_trainer.last_name) + ' ' + str(
                cur_trainer.first_name)] = \
                cur_trainer
            cur_record = trainer_data_importer.load_next_record()

    def get_trainer_id(self, first_name, last_name, reqester_data,
                       requester_key):
        key = ''.join(last_name) + ' ' + first_name
        if key in self.data:
            self.data[key].add_reference(reqester_data, requester_key)
            return key
        else:
            return 0
            # raise NameError(
            #     'Trainer ' + first_name + ' ' + ''.join(
            #         last_name) + ' not found!\n')
