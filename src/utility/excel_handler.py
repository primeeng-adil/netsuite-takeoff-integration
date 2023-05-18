def get_cell_with_value(sheet, value):
    for i in range(1, sheet.max_row):
        for j in range(1, sheet.max_column):
            if sheet.cell(i, j).value == value:
                return i, j


def change_cell_with_value(sheet, value, new_value):
    for i in range(1, sheet.max_row):
        for j in range(1, sheet.max_column):
            if sheet.cell(i, j).value == value:
                sheet.cell(i, j).value = new_value
                return


def change_adjacent_cell(sheet, value, new_value):
    row, col = get_cell_with_value(sheet, value)
    sheet.cell(row, col + 1).value = new_value


def change_cells_with_values(sheet, key_value_pairs):
    for key_value_pair in key_value_pairs:
        change_cell_with_value(sheet, key_value_pair[0], key_value_pair[1])


def change_adjacent_cells_with_values(sheet, key_value_pairs):
    for key_value_pair in key_value_pairs:
        change_adjacent_cell(sheet, key_value_pair[0], key_value_pair[1])
