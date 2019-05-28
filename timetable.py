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

    days_of_week_label = {
        "Pn": "Poniedziałek",
        "Wt": "Wtorek",
        "Sr": "Środa",
        "Cz": "Czwartek",
        "Pt": "Piątek",
        "So": "Sobota",
        "Nd": "Nedziela",
    }

    days_of_week = ["Pn", "Wt", "Sr", "Cz", "Pt", "So", "Nd"]

    def get_with_not_null_column(self, column_name, data):
        result = []
        column_index = self.columnNameToIndex[column_name]
        for row in list(data)[1:]:
            if row[column_index].value is not None:
                result.append(row)

        return result

    def get_with_column_equals(self, column_name, search_value, data):
        result = []
        column_index = self.columnNameToIndex[column_name]
        for row in list(data)[1:]:
            if row[column_index].value is search_value:
                result.append(row)

        return result

    def get_unique_value_from_column(self, column_name, data):
        result = set()
        column_index = self.columnNameToIndex[column_name]
        next(data)  # first row is column name

        for row in data:
            if row[column_index].value is not None:
                result.add(row[column_index].value)

        return result
