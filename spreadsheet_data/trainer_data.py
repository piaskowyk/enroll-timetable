from spreadsheet_data.common_data import *
from spreadsheet_tools.sheet_data_importer import SpreadsheetDataImporter
from interface_tools.output_tools import *

# dictionary for trainer's positions - it will be updated during loading
# trainer data
positions = dict()

# dictionary of trainer's degrees
degrees = {'dr hab.': 'Habilitated doctor',
           'dr': 'Doctor',
           'inż.': 'Engineer',
           'mgr': 'Master\'s degree',
           'prof.': 'Professor'}


class TrainerInfo:
    # class for one trainer record

    # initiates object with information provided in record
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

        # if one of these columns values are not set
        if record['consultationsDay'] is None or \
                record['consultationsHours'] is None:
            self.consult_time = 0
        else:
            # make weekly time period from column values
            split_value = record['consultationsHours'].split('-')
            first = split_value[0]
            second = None
            if len(split_value) > 1:
                second = split_value[1]
            self.consult_time = WeeklyTimePeriod(record['consultationsDay'],
                                                 first,
                                                 second)
        self.comments = record['comments']

        # gets primary key of record with provided department
        self.department_id = department_data.get_department_id(
            record['departmentName'], requester_data, self.get_key())

    # returns primary key
    def get_key(self):
        return str(self.last_name) + ' ' + str(self.first_name)

    # remember object, that references to this record, from particular data
    # table
    def add_reference(self, requester_data, requester_key):
        if id(requester_data) not in self.referenced_by:
            self.referenced_by[id(requester_data)] = []
        self.referenced_by[id(requester_data)].append(requester_key)


class TrainerData:
    # class for table with records about trainers

    def __init__(self, config, workbook, department_data):
        self.data = dict()

        # prepares to import data from spreadsheet
        trainer_data_importer = SpreadsheetDataImporter(config, workbook,
                                                        'trainers')
        cur_record = trainer_data_importer.load_next_record()

        # until empty record is loaded
        while len(cur_record) > 0:
            cur_trainer = TrainerInfo(cur_record, department_data, self)

            # show errors in case of invalid data in spreadsheet row
            if len(cur_record['name'].split(' ')) != 2:
                show_error(trainer_data_importer.get_last_record_info() +
                           'Name of trainer is set in invalid format.')

            # adds record to table
            self.data[str(cur_trainer.last_name) + ' ' + str(
                cur_trainer.first_name)] = \
                cur_trainer
            cur_record = trainer_data_importer.load_next_record()

    # returns primary key of this record; if information about provided trainer
    # doesn't exist returns None
    def get_trainer_id(self, first_name, last_name, reqester_data,
                       requester_key):
        key = ''.join(last_name) + ' ' + first_name
        if key in self.data:
            self.data[key].add_reference(reqester_data, requester_key)
            return key
        else:
            return None
