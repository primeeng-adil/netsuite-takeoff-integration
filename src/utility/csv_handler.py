import csv
from pathlib import Path


def read_csv(path: Path | str, header: bool = False) -> list:
    """
    Reads and returns data from a csv file.

    :param path: path of the csv to read from
    :param header: flag to check if header row exists
    :return: a two-dimensional list containing rows and columns
    """
    with open(path, newline='') as csvfile:
        data_list = []
        reader = csv.reader(csvfile)
        for row in reader:
            data_list.append(row)
        if header:
            data_list.pop(0)
        return data_list


def read_csv_column(path: Path | str, column: int = 0, header: bool = False) -> list:
    """
    Reads and returns data from a csv file.

    :param path: path of the csv to read from
    :param column: index of the column to be retrieved
    :param header: flag to check if header row exists
    :return: a two-dimensional list containing rows and columns
    """
    return [row[column] for row in read_csv(path, header)]


def write_csv(path: Path | str, data: list) -> None:
    """
    Writes data to a csv file.

    :param path: path of the csv to write to
    :param data: a two-dimensional list containing rows and columns
    """
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
