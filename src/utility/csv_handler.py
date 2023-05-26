import csv
from pathlib import Path
from tkinter import messagebox


def read_csv(path: Path | str) -> list:
    """
    Reads and returns data from a csv file.

    :param path: path of the csv to read from
    :return: a two-dimensional list containing rows and columns
    """
    try:
        with open(path, newline='') as csvfile:
            data_list = []
            reader = csv.reader(csvfile)
            for row in reader:
                data_list.append(row[0])
            return data_list

    except FileNotFoundError:
        messagebox.showerror('File not found', f'Error: cannot find file at {path}')
        raise FileNotFoundError


def write_csv(path: Path | str, data: list) -> None:
    """
    Writes data to a csv file.

    :param path: path of the csv to write to
    :param data: a two-dimensional list containing rows and columns
    """
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
