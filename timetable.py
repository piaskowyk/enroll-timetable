class Timetable:

    columnNameToIndex = {
        'studia': 0,
        'semestr': 1,
        'lokalizacja': 2,
        'przedmiot': 3,
        'obierak': 4,
        'typ': 5,
        'grupa': 6,
        'wym': 7,
        'wyk': 8,
        'prow': 9,
        'osoba': 10,
        'sala': 11,
        'tyg': 12,
        'dzien': 13,
        'godz': 14,
        'koniec': 15,
        'port': 16,
        'uwagi': 17,
    }

    def get_with_not_null_column(self, column_name, sheet):
        result = []
        column_index = self.columnNameToIndex[column_name]
        for row in sheet.rows:
            if row[column_index].value is not None:
                result.append(row)

        return result

    def get_with_column_equals(self, column_name, search_value, sheet):
        result = []
        column_index = self.columnNameToIndex[column_name]
        for row in sheet.rows:
            if row[column_index].value is search_value:
                result.append(row)

        return result

    def get_unique_value_from_column(self, column_name, sheet):
        result = set()
        column_index = self.columnNameToIndex[column_name]
        next(sheet.rows)  # first row is column name

        for row in sheet.rows:
            if row[column_index].value is not None:
                result.add(row[column_index].value)

        return result
