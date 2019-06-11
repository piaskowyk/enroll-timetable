from reportlab.graphics.shapes import Drawing, Line
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from utils.timetabletools import TimetableTools
from spreadsheet_data.full_time_semester_event_data import *

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, \
    Table, TableStyle, KeepTogether


# check equal time format
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
        self.table_header = ['Czas', 'Przedmiot', 'Tydzień', 'Typ wydarzenia', 'Prowadzący']

    def get_empty_tab(self):
        result = [self.table_header]
        return result

    # collect data about occupancy in one time block in on day
    def get_room_event_by_day(self, day, time_block, room, data_id, semester_data):
        event_data = []
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

                event_name = event.course_id

                # break line if event name is too long
                max_len = 35
                if len(event_name) > max_len:
                    index = max_len - (event_name[:max_len])[::-1].find(' ')
                    event_name = event_name[:index-1] + '\n' + event_name[index:]
                event_data.append([
                    self.tools.time_blocks[event.event_time.get_string().split(' ')[1]],
                    event_name,
                    event.week_name,
                    event_types[event.event_type],
                    event.trainer_id
                ])
                # break

        return event_data

    def exec_command(self, spreadsheet_data, args):
        if len(args) < 2:
            print("You must insert output file name")
            return

        print("Generating PDF...")

        # creating doc template and setting up output sheet style
        doc = SimpleDocTemplate(args[1], pagesize=letter)
        pdfmetrics.registerFont(TTFont('Standard', 'src/font.ttf'))
        pdfmetrics.registerFont(TTFont('Bold', 'src/font-bold.ttf'))
        doc.leftMargin = 40
        styles = getSampleStyleSheet()
        style_h1 = ParagraphStyle(name='Heading1',
                                  fontName='Bold',
                                  fontSize=14,
                                  leading=22,
                                  spaceAfter=2)
        style_h2 = ParagraphStyle(name='Heading2',
                                  fontName='Standard',
                                  fontSize=12,
                                  leading=22,
                                  spaceAfter=1)
        space = Spacer(1, 0.20 * inch)
        table_style = TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Standard'),
            ('ALIGN', (0, 0), (-2, 0), 'CENTER'),
            ('ALIGN', (0, 0), (0, -5), 'LEFT'),
            ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])

        # collect information about room occupancy
        elements = []

        # iterate over any room
        for room_key, room in spreadsheet_data.room_data.data.items():
            print("Sala:", str(room.building_id) + ' - ' + str(room.name) + "\n")
            line = Drawing(520, 10)
            line.add(Line(0, 7, 520, 7))
            elements.append(Paragraph("Sala: " + str(room.building_id) + ' - ' + str(room.name), style_h1))
            elements.append(line)

            # for any room check occupancy for any day
            for day in self.tools.days_of_week[0:5]:
                print(self.tools.days_of_week_label[day])
                elements.append(Paragraph(self.tools.days_of_week_label[day], style_h2))

                data_id = id(spreadsheet_data.full_time_first_semester_event_data)
                semester_data = spreadsheet_data.full_time_first_semester_event_data.data

                event_data = [self.table_header]

                # for any day check occupancy in any time block
                if data_id in room.referenced_by:
                    for time_block in self.tools.time_blocks:
                        result = self.get_room_event_by_day(day, time_block, room, data_id, semester_data)
                        if len(result) == 0:
                            result = [self.tools.time_blocks[time_block], '', '', '', '']
                        else:
                            for item in result:
                                event_data.append(item)

                if len(event_data) <= 1:
                    event_data = self.get_empty_tab()

                # add new table do sheet
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
