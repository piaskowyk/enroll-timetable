class SpreadsheetDataImporter:
    # class of spreadsheet data importer, that basics on configuration for
    # current table (table_name) streams (loads) next records from particular
    # position of provided workbook

    def __init__(self, config, workbook, table_name):
        self.column_headers = dict()
        self.cur_record_id = 1
        self.table_name = table_name

        # gets wanted information from configuration
        self.sheet = workbook[config['tables'][table_name]['sheetName']]
        self.header_row = config['tables'][table_name]['headerRow']
        self.last_row = config['tables'][table_name]['lastRow']
        columns_range = range(ord(config['tables'][table_name]['firstColumn']),
                              ord(config['tables'][table_name][
                                      'lastColumn']) + 1)

        # searches for particular columns defined in configuration,
        # in particular workbook place
        for atr in config['tables'][table_name]['columnNames']:
            value = config['tables'][table_name]['columnNames'][atr]
            # searches for particular column
            for cur_char in columns_range:
                if self.sheet[chr(cur_char) + str(self.header_row)].value == \
                        value:
                    # if current column is the right column
                    self.column_headers[atr] = cur_char
                    break
            else:
                # if defined column in configuration couldn't be found
                raise NameError('Column with name \"' + str(value)
                                + '\" not found!\n')

    # move read cursor to beginning of table
    def rewind(self):
        self.cur_record_id = 1

    # loads next record from particular table on current position, returns
    # dictionary in which keys are table column names, and values are values
    # that are in particular columns of currently loaded row
    def load_next_record(self):
        record = dict()

        # if whole table was read
        if self.last_row != -1 and \
                self.header_row + self.cur_record_id > self.last_row:
            return record
        not_null = False

        # get values from all defined columns
        for key, value in self.column_headers.items():
            cell = self.sheet[
                chr(value) + str(self.header_row + self.cur_record_id)]
            cell_value = cell.value

            # check if ceil content isn't striked out
            if cell.font.strike:
                cell_value = None
            if cell_value is not None:
                not_null = True
            record[key] = cell_value
        self.cur_record_id += 1
        if not not_null:
            # if all column values are empty => return empty dictionary
            record = dict()
            return record
        else:
            return record

    # returns information about lastly read row as string
    def get_last_record_info(self):
        return str(self.sheet.title) + ':' + \
               str(self.header_row + self.cur_record_id - 1)

    # finishes working with object
    def finish(self):
        self.sheet = 0
        self.table_name = ''
        self.header_row = 0
        self.last_row = 0
        self.column_headers = dict()
        self.cur_record_id = 1
