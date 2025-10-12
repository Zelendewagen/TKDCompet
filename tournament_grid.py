import math
import os

from openpyxl import Workbook
from openpyxl.styles import Border, Side, Alignment

data = ["Первый", "Второй", "Третий", 'Четвертый', 'Пятый', 'Шестой', 'Седьмой', 'Восьмой',
        'Девятый', 'Десятый', 'Одиннадцатый', 'Двенадцатый', 'Тринадцатый']
data = [f'Участник {i}' for i in range(1, 6)]

first_pow2 = 2 ** math.ceil(math.log2(len(data)))
first_byes = first_pow2 - len(data)
first_round_players = len(data) - first_byes
rounds_count = math.ceil(math.log2(len(data)))

workbook = Workbook()
sheet = workbook.active
sheet.title = "Лист1"

bot_border = Border(bottom=Side(style="thin"))
right_border = Border(right=Side(style="thin"))
bot_right_border = Border(right=Side(style="thin"), bottom=Side(style="thin"))
bot_left_border = Border(left=Side(style="thin"), bottom=Side(style="thin"))

row_index = 1
last_row = 1
current_round = 0
last_column = 1
for i, name in enumerate(data):
    if first_byes and name in data[-first_byes:]:
        row_index += 1
        cell = sheet.cell(row=row_index, column=2, value=name)
        row_index += 3
        continue
    else:
        cell = sheet.cell(row=row_index, column=1, value=name)

    cell.border = bot_border
    row_index += 2
    if i % 2 == 0:
        cell = sheet.cell(row=row_index - 1, column=1)
        cell.border = right_border
    else:
        cell.border = bot_right_border

current_round += 1
row_index = 2
next_last_row_counter = 2
last_row = (first_round_players // 2 + first_byes) * 4 - next_last_row_counter
if rounds_count >= current_round:
    last_column = 2
    while row_index <= last_row:
        cell = sheet.cell(row=row_index, column=2)
        if row_index in [i for i in range(6, 800, 8)]:
            cell.border = bot_right_border
        elif row_index in [i for i in range(2, 800, 8)]:
            cell.border = bot_border
        else:
            cell.border = right_border
        row_index += 1
        if row_index in [i for i in range(7, 800, 8)]:
            row_index += 3

    current_round += 1
    row_index = 4
    last_row -= next_last_row_counter

    if rounds_count >= current_round:
        last_column = 3
        while row_index <= last_row:
            cell = sheet.cell(row=row_index, column=3)
            if row_index in [i for i in range(12, 800, 16)]:
                cell.border = bot_right_border
            elif row_index in [i for i in range(4, 800, 16)]:
                cell.border = bot_border
            else:
                cell.border = right_border
            row_index += 1
            if row_index in [i for i in range(13, 800, 16)]:
                row_index += 7

        current_round += 1
        row_index = 8
        next_last_row_counter *= 2
        last_row -= next_last_row_counter

        if rounds_count >= current_round:
            last_column = 4
            while row_index <= last_row:
                cell = sheet.cell(row=row_index, column=4)
                if row_index in [i for i in range(24, 800, 32)]:
                    cell.border = bot_right_border
                elif row_index in [i for i in range(8, 800, 32)]:
                    cell.border = bot_border
                else:
                    cell.border = right_border
                row_index += 1
                if row_index in [i for i in range(25, 800, 32)]:
                    row_index += 15

            current_round += 1
            row_index = 16
            next_last_row_counter *= 2
            last_row -= next_last_row_counter
            if rounds_count >= current_round:
                last_column = 5
                while row_index <= last_row:
                    cell = sheet.cell(row=row_index, column=5)
                    if row_index in [i for i in range(48, 800, 64)]:
                        cell.border = bot_right_border
                    elif row_index in [i for i in range(16, 800, 64)]:
                        cell.border = bot_border
                    else:
                        cell.border = right_border
                    row_index += 1
                    if row_index in [i for i in range(49, 800, 64)]:
                        row_index += 31

                current_round += 1
                row_index = 32
                next_last_row_counter *= 2
                last_row -= next_last_row_counter
                if rounds_count >= current_round:
                    last_column = 6
                    while row_index <= last_row:
                        cell = sheet.cell(row=row_index, column=6)
                        if row_index in [i for i in range(96, 800, 128)]:
                            cell.border = bot_right_border
                        elif row_index in [i for i in range(32, 800, 128)]:
                            cell.border = bot_border
                        else:
                            cell.border = right_border
                        row_index += 1
                        if row_index in [i for i in range(97, 800, 128)]:
                            row_index += 63


cell = sheet.cell(row=sheet.max_row + 1, column=last_column - 1)
cell.border = bot_border
cell = sheet.cell(row=sheet.max_row + 1, column=last_column - 1)
cell.border = right_border
cell = sheet.cell(row=sheet.max_row, column=last_column)
cell.border=bot_border
cell = sheet.cell(row=sheet.max_row + 1, column=last_column - 1)
cell.border=bot_right_border

winners = ['Первое место:', 'Второе место:', 'Третье место:']
for i, text in enumerate(['Главный судья', 'Судья', 'Секретарь']):
    cell1 = sheet.cell(row=sheet.max_row + 2, column=last_column - 1, value=text)
    cell = sheet.cell(row=sheet.max_row, column=1, value=winners[i])
    cell2 = sheet.cell(row=sheet.max_row, column=last_column, value=f'/name')
    cell2.border = bot_border
    cell2.alignment = Alignment(horizontal="right")



for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']:
    sheet.column_dimensions[i].width = 30
workbook.save("Сетка.xlsx")
os.startfile("Сетка.xlsx")
