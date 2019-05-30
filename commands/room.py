from utils.timetabletools import TimetableTools
from spreadsheet_data.full_time_semester_event_data import *

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, \
    Table, TableStyle


class Room:

    def __init__(self):
        self.tools = TimetableTools()

    def equal_time(self, time_first, time_second):
        if time_first is '' or time_second is '':
            return False
        time_first_split = time_first.split(':')
        time_second_split = str(time_second).split(':')

        if int(time_first_split[0]) != int(time_second_split[0]) \
                or int(time_first_split[1]) != int(time_second_split[1]):
            return False
        return True

    def get_room_event_by_day(self, day, time_block, room, data_id, semester_data):
        for event_id in room.referenced_by[data_id]:
            event = semester_data[event_id]

            if event.event_time != 0 \
                    and day == event.day_name \
                    and self.equal_time(time_block, event.start_time):

                print("time:", event.event_time.get_string())
                print("id:", event.course_id)
                print("week name:", event.week_name)
                print("type:", event_types[event.event_type])
                print("trainer_id:", event.trainer_id)

    def exec_command(self, spreadsheet_data, args):
        print("start")
        pdf_data = []
        for room_key, room in spreadsheet_data.room_data.data.items():
            print("Sala:", str(room.building_id) + ' - ' + str(room.name) + "\n")
            for day in self.tools.days_of_week[0:5]:
                print(self.tools.days_of_week_label[day])

                data_id = id(spreadsheet_data.full_time_first_semester_event_data)
                semester_data = spreadsheet_data.full_time_first_semester_event_data.data

                if data_id not in room.referenced_by:
                    continue

                for time_block in self.tools.time_blocks:
                    self.get_room_event_by_day(day, time_block, room, data_id, semester_data)

                print("+++")
            print("------------------------------------------")
            self.export_to_pdf([[1, 2, 3, 4]])

    def export_to_pdf(self, data):
        doc = SimpleDocTemplate("./data/tmp.pdf", pagesize=letter)
        doc.leftMargin = 1
        styles = getSampleStyleSheet()
        styleH = styles['Heading1']

        story = []

        story.append(Paragraph("xDDD", styleH))
        story.append(Spacer(1, 0.25 * inch))

        table = Table(data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-2, 0), 'CENTER'),
            ('ALIGN', (0, 0), (0, -5), 'LEFT'),
            ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))

        story.append(table)
        doc.build(story)
