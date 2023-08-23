import datetime
import win32wnet
import pythoncom
import pywintypes
from pathlib import Path
from utility.excel_handler import *
import win32com.client as client


def create_takeoff_file(src: Path, dest: Path, proj_data: dict):
    """
    Copy the takeoff template file, add information to it and save it as xlsm.

    :param src: source path of the template file
    :param dest: destination to save the xlsm file in
    :param proj_data: object containing project information
    """
    today_date = datetime.datetime.today().strftime('%d-%m-%Y')
    key_value_pairs = [
        ['XXXX', proj_data['id']],
        ['TODAYSDATE', today_date],
        ['NAMEHERE', proj_data['rep']],
        ['CLIENT', proj_data['client']],
        ['PROJECT NAME', proj_data['name']],
        ['PROJECT TYPE', proj_data['type']],
        ['PROPOSAL-URL', proj_data['url']]
    ]
    takeoff_wb = get_excel_workbook(src)
    takeoff_ws = takeoff_wb.Worksheets(1)
    change_cells_with_values(takeoff_ws, key_value_pairs)
    save_as_xlsm(takeoff_wb, dest)


def create_checklist_file(src: Path, dest: Path, proj_data: dict):
    """
    Copy the checklist template file, add information to it and save it as xlsm.

    :param src: source path of the template file
    :param dest: destination to save the xlsm file in
    :param proj_data: object containing project information
    """
    checklist_wb = get_excel_workbook(src)
    checklist_ws = checklist_wb.Worksheets(1)
    change_adjacent_cell(checklist_ws, 'PROJECT#', proj_data['id'])
    save_as_xlsm(checklist_wb, dest)


def create_config_file(src: Path, dest: Path, proj_data: dict):
    """
    Copy the configurator template file, add information to it and save it as xlsm.

    :param src: source path of the template file
    :param dest: destination to save the xlsm file in
    :param proj_data: object containing project information
    """
    key_value_pairs = [
        ['Project Number:', proj_data['id']],
        ['Project Name:', proj_data['name']]
    ]
    config_wb = get_excel_workbook(src)
    config_ws = config_wb.Worksheets(1)
    change_adjacent_cells_with_values(config_ws, key_value_pairs)
    save_as_xlsm(config_wb, dest)


def update_quote_log(path, proj_data):
    """
    Add a row entry for the project in the Quote Log.

    :param path: full path of the Quote Log file
    :param proj_data: object containing project information
    """
    ql_wb = get_excel_workbook(path)
    ql_ws = ql_wb.Worksheets(1)
    last_row = get_last_empty_row(ql_ws, 3)
    today_date = datetime.datetime.today().strftime('%d-%m-%y')
    network_path = proj_data['job-path']
    try:
        network_path = win32wnet.WNetGetUniversalName(proj_data['job-path'], 1)
    except pywintypes.error:
        pass
    row_data = [
        today_date,
        proj_data['client'],
        network_path,
        proj_data['scope'],
        proj_data['id'],
        'TBD',
        proj_data['rep']
    ]
    fill_row_with_values(ql_ws, last_row, row_data)
    ql_wb.Save()
    ql_wb.Close()


def save_as_xlsm(wb, dest: Path):
    """
    Save the given xltm file as xlsm.

    :param wb: source Excel Workbook object
    :param dest: destination path to save the xlsm file as
    """
    filename = str(dest.parent / (dest.stem + '.xlsm'))
    wb.SaveAs(Filename=filename, FileFormat=52, CreateBackup=False)
    wb.Close()


def get_excel_workbook(src: Path):
    """
    Open and return the Excel workbook.

    :param src: path of the Excel workbook
    """
    app, command = 'Excel.Application', pythoncom.CoInitialize
    excel = client.gencache.EnsureDispatch(app, command())
    excel.DisplayAlerts = False
    return excel.Workbooks.Open(str(src), UpdateLinks=False)
