from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from utils.timetabletools import TimetableTools
from spreadsheet_data.full_time_semester_event_data import *

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, \
    Table, TableStyle, KeepTogether


def equal_time(time_first, time_second):
    if time_first is '' or time_second is '':
        return False
    time_first_split = time_first.split(':')
    time_second_split = str(time_second).split(':')

    if int(time_first_split[0]) != int(time_second_split[0]) \
            or int(time_first_split[1]) != int(time_second_split[1]):
        return False
    return True


class RoomTable:

    def __init__(self):
        self.tools = TimetableTools()
        self.table_header = ['Czas', 'Przedmiot', 'Typ', 'Typ2', 'Prowadzący']

    def get_empty_tab(self):
        result = [self.table_header]
        for time_block in self.tools.time_blocks:
            result.append([self.tools.time_blocks[time_block], '', '', '', ''])

        return result

    def get_room_event_by_day(self, day, time_block, room, data_id, semester_data):
        event_data = None
        for event_id in room.referenced_by[data_id]:
            event = semester_data[event_id]

            if event.event_time != 0 \
                    and day == event.day_name \
                    and equal_time(time_block, event.start_time):
                print("time:", event.event_time.get_string())
                print("id:", event.course_id)
                print("week name:", event.week_name)
                print("type:", event_types[event.event_type])
                print("trainer_id:", event.trainer_id)

                print("+")
                print(event.event_time.get_string())
                event_data = [
                    self.tools.time_blocks[event.event_time.get_string().split(' ')[1]],
                    event.course_id,
                    event.week_name,
                    event_types[event.event_type],
                    event.trainer_id
                ]
                break

        return event_data

    def exec_command(self, spreadsheet_data, args):
        if len(args) < 2:
            print("You must insert output file name")
            return

        print("Generating PDF...")

        doc = SimpleDocTemplate(args[1], pagesize=letter)
        pdfmetrics.registerFont(TTFont('Standard', 'src/font.ttf'))
        pdfmetrics.registerFont(TTFont('Bold', 'src/font-bold.ttf'))
        doc.leftMargin = 5
        styles = getSampleStyleSheet()
        style_h1 = ParagraphStyle(name='Heading1',
                                  fontName='Bold',
                                  fontSize=18,
                                  leading=22,
                                  spaceAfter=2)
        style_h2 = ParagraphStyle(name='Heading2',
                                  fontName='Standard',
                                  fontSize=15,
                                  leading=22,
                                  spaceAfter=1)
        space = Spacer(1, 0.25 * inch)
        table_style = TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Standard'),
            ('ALIGN', (0, 0), (-2, 0), 'CENTER'),
            ('ALIGN', (0, 0), (0, -5), 'LEFT'),
            ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])

        elements = []

        for room_key, room in spreadsheet_data.room_data.data.items():
            print("Sala:", str(room.building_id) + ' - ' + str(room.name) + "\n")
            elements.append(Paragraph("Sala: " + str(room.building_id) + ' - ' + str(room.name), style_h1))

            for day in self.tools.days_of_week[0:5]:
                print(self.tools.days_of_week_label[day])
                elements.append(Paragraph(self.tools.days_of_week_label[day], style_h2))

                data_id = id(spreadsheet_data.full_time_first_semester_event_data)
                semester_data = spreadsheet_data.full_time_first_semester_event_data.data

                event_data = [self.table_header]
                if data_id in room.referenced_by:
                    for time_block in self.tools.time_blocks:
                        result = self.get_room_event_by_day(day, time_block, room, data_id, semester_data)
                        if result is None:
                            result = [self.tools.time_blocks[time_block], '', '', '', '']
                        event_data.append(result)

                if len(event_data) <= 1:
                    event_data = self.get_empty_tab()

                table = Table(event_data, hAlign='LEFT')
                table.setStyle(table_style)
                elements.append(table)
                elements.append(KeepTogether(Spacer(10, 20)))
            print("------------------------------------------")

        try:
            doc.build(elements)
            print("END, pdf is generated")
        except:
            print("Error while generating pdf, check correct of sheet")
