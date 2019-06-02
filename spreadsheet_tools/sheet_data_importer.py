

class SpreadsheetDataImporter:
    sheet = 0
    table_name = ''
    header_row = 0
    last_row = 0
    column_headers = dict()
    cur_record_id = 1

    def __init__(self, config, workbook, table_name):
        self.table_name = table_name
        self.sheet = workbook[config['tables'][table_name]['sheetName']]
        self.header_row = config['tables'][table_name]['headerRow']
        self.last_row = config['tables'][table_name]['lastRow']
        columns_range = range(ord(config['tables'][table_name]['firstColumn']),
                              ord(config['tables'][table_name][
                                      'lastColumn']) + 1)

        for atr in config['tables'][table_name]['columnNames']:
            value = config['tables'][table_name]['columnNames'][atr]
            for cur_char in columns_range:
                if self.sheet[chr(cur_char) + str(self.header_row)].value == \
                        value:
                    self.column_headers[atr] = cur_char
                    break
            else:
                raise NameError('Column with name \"' + str(value)
                                + '\" not found!\n')

    def rewind(self):
        self.cur_record_id = 1

    def load_next_record(self):
        record = dict()
        if self.last_row != -1 and \
                self.header_row+self.cur_record_id > self.last_row:
            return record
        not_null = False
        for key, value in self.column_headers.items():
            cell_value = self.sheet[
                chr(value) + str(self.header_row + self.cur_record_id)].value
            if cell_value is not None:
                not_null = True
            record[key] = cell_value
        self.cur_record_id += 1
        if not not_null:
            record = dict()
            return record
        else:
            return record

    def finish(self):
        self.sheet = 0
        self.table_name = ''
        self.header_row = 0
        self.last_row = 0
        self.column_headers = dict()
        self.cur_record_id = 1
