import csv
from pathlib import Path


def read_csv(path: Path | str) -> list:
    """
    Reads and returns data_keys from a csv file.

    :param path: path of the csv to read from
    :return: a two-dimensional list containing rows and columns
    """
    with open(path, newline='') as csvfile:
        data_list = []
        reader = csv.reader(csvfile)
        for row in reader:
            data_list.append(row[0])
        data_list.pop(0)
        return data_list


def write_csv(path: Path | str, data: list) -> None:
    """
    Writes data_keys to a csv file.

    :param path: path of the csv to write to
    :param data: a two-dimensional list containing rows and columns
    """
    path.parent.mkdir(exist_ok=True)
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
