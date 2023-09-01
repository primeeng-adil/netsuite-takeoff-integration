from pathlib import Path


def get_max_row_col(sheet):
    """
    Get the indices of the max row and column.

    :param sheet: excel worksheet containing data
    :return: row, column indices of the max row and column
    """
    max_row = sheet.Cells(sheet.Rows.Count, 2).End(-4162).Row + 1
    max_col = sheet.Cells(2, sheet.Columns.Count).End(-4159).Column + 1
    return max_row, max_col


def get_cell_with_value(sheet, value):
    """
    Get the indices of the cell containing a given value.

    :param sheet: excel worksheet containing the cell
    :param value: value to look for in the cell
    :return: row, column indices of the cell
    """
    max_row, max_col = get_max_row_col(sheet)
    for i in range(1, max_row):
        for j in range(1, max_col):
            if sheet.Cells(i, j).Value == value:
                return i, j


def change_cell_with_value(sheet, value, new_value):
    """
    Change the value of the cell containing a certain value with a new value.

    :param sheet: excel worksheet containing the cell
    :param value: value to look for in the cell
    :param new_value: value to replace the existing value with
    """
    max_row, max_col = get_max_row_col(sheet)
    for i in range(1, max_row):
        for j in range(1, max_col):
            if sheet.Cells(i, j).Value == value:
                sheet.Cells(i, j).Value = new_value
                return


def change_adjacent_cell(sheet, value, new_value):
    """
    Change the value of the cell adjacent to the cell containing a certain value with a new value.

    :param sheet: excel worksheet containing the cell
    :param value: value to look for in the cell
    :param new_value: value to replace the existing value with
    """
    row, col = get_cell_with_value(sheet, value)
    sheet.Cells(row, col + 1).Value = new_value


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


def get_last_empty_row(sheet, column):
    """
    Find and return the row index of the first empty cell in a column.

    :param sheet: excel worksheet containing the cells
    :param column: column used to identify the last row
    :return: row index of the first empty cell
    """
    max_row, max_col = get_max_row_col(sheet)
    for i in range(max_row, 1, -1):
        if sheet.Cells(i, column).Value is not None:
            return sheet.Cells(i, column).Row + 1


def fill_row_with_values(sheet, row, values):
    """
    Populate the given row with the given values.

    :param sheet: excel worksheet containing the cells
    :param row: index of the row to be populated
    :param values: values that the row is to be populated with
    """
    for value in values:
        sheet.Cells(row, values.index(value) + 2).Value = value
        if Path(str(value)).is_dir():
            sheet.Hyperlinks.Add(Anchor=sheet.Cells(row, values.index(value) + 2),
                                 Address=value, TextToDisplay=str(value))
