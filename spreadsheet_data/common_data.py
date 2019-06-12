import datetime

# a dictionary with day of week shortcuts used in spreadsheet
days_of_week = {'Pn': 'Monday',
                'Wt': 'Tuesday',
                'Sr': 'Wednesday',
                'Cz': 'Thursday',
                'Pt': 'Friday',
                'So': 'Saturday',
                'Nd': "Sunday"}

# indexed table with days of week (used to get index of particular day of week)
days_of_week_indexed = ["Pn", "Wt", "Sr", "Cz", "Pt", "So", "Nd"]


class WeeklyTimePeriod:
    # class of weekly time period contains information about weekly time period

    def __init__(self, day_of_week, start_time, end_time=-1):
        self.day_of_week = 0
        self.start_time = 0
        self.end_time = 0

        # processes day_of_week argument
        if isinstance(day_of_week, str):
            self.day_of_week = day_of_week
        else:
            self.day_of_week = days_of_week_indexed[day_of_week - 1]
        time_delim = ':'

        # processes start_time argument
        if isinstance(start_time, str):
            self.start_time = 60 * int(start_time.split(time_delim)[0]) + \
                              int(start_time.split(time_delim)[1])
        elif isinstance(start_time, datetime.time):
            self.start_time = 60 * start_time.hour + start_time.minute
        else:
            self.start_time = start_time

        # processes end_time_argument (if provided)
        if end_time == -1:
            self.end_time = self.start_time + 90
        else:
            if isinstance(end_time, str):
                self.end_time = 60 * int(end_time.split(time_delim)[0]) + \
                                int(end_time.split(time_delim)[1])
            elif isinstance(end_time, datetime.time):
                self.end_time = 60 * end_time.hour + end_time.minute
            else:
                self.end_time = end_time

    # returns string of weekly time period
    def get_string(self):
        return '{0}: {1}:{2:02d} - {3}:{4:02d}'.format(days_of_week[
                                                           self.day_of_week],
                                                       self.start_time // 60,
                                                       self.start_time % 60,
                                                       self.end_time // 60,
                                                       self.end_time % 60)
