days_of_week = {'Pn': 'Monday',
                'Wt': 'Tuesday',
                'Sr': 'Wednesday',
                'Cz': 'Thursday',
                'Pt': 'Friday',
                'So': 'Saturday',
                'Nd': "Sunday"}
days_of_week_indexed = ["Pn", "Wt", "Sr", "Cz", "Pt", "So", "Nd"]


class WeeklyTimePeriod:
    day_of_week = 0
    start_time = 0
    end_time = 0

    def __init__(self, day_of_week, start_time, end_time=-1):
        if isinstance(day_of_week, str):
            self.day_of_week = day_of_week
        else:
            self.day_of_week = days_of_week_indexed[day_of_week-1]
        time_delim = ':'
        if isinstance(start_time, str):
            self.start_time = 60*int(start_time.split(time_delim)[0]) + \
                int(start_time.split(time_delim)[1])
        else:
            self.start_time = start_time
        if end_time == -1:
            self.end_time = self.start_time + 90
        else:
            if isinstance(end_time, str):
                self.end_time = 60*int(end_time.split(time_delim)[0]) + \
                    int(end_time.split(time_delim)[1])
            else:
                self.end_time = end_time
