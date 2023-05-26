def get_cell_with_value(sheet, value):
    """
    Get the indices of the cell containing a given value.

    :param sheet: excel worksheet containing the cell
    :param value: value to look for in the cell
    :return: row, column indices of the cell
    """
    for i in range(1, sheet.max_row):
        for j in range(1, sheet.max_column):
            if sheet.cell(i, j).value == value:
                return i, j


def change_cell_with_value(sheet, value, new_value):
    """
    Change the value of the cell containing a certain value with a new value.

    :param sheet: excel worksheet containing the cell
    :param value: value to look for in the cell
    :param new_value: value to replace the existing value with
    """
    for i in range(1, sheet.max_row):
        for j in range(1, sheet.max_column):
            if sheet.cell(i, j).value == value:
                sheet.cell(i, j).value = new_value
                return


def change_adjacent_cell(sheet, value, new_value):
    """
    Change the value of the cell adjacent to the cell containing a certain value with a new value.

    :param sheet: excel worksheet containing the cell
    :param value: value to look for in the cell
    :param new_value: value to replace the existing value with
    """
    row, col = get_cell_with_value(sheet, value)
    sheet.cell(row, col + 1).value = new_value


def change_cells_with_values(sheet, key_value_pairs):
    """
    Change all the cells containing specific values with the new values.

    :param sheet: excel worksheet containing the cells
    :param key_value_pairs: value, new value pairs
    """
    for key_value_pair in key_value_pairs:
        change_cell_with_value(sheet, key_value_pair[0], key_value_pair[1])


def change_adjacent_cells_with_values(sheet, key_value_pairs):
    """
    Change all the cells adjacent to the cells containing specific values with the new values.

    :param sheet: excel worksheet containing the cells
    :param key_value_pairs: value, new value pairs
    """
    for key_value_pair in key_value_pairs:
        change_adjacent_cell(sheet, key_value_pair[0], key_value_pair[1])
