import datetime
import os
from openpyxl import load_workbook
from src.utility.excel_handler import *
import win32com.client as client
import pythoncom
from pathlib import Path
from src.consts import CHECKLIST_PATH


def create_takeoff_file(src, dest, proj_data):
    today_date = datetime.datetime.today().strftime('%d-%m-%Y')
    key_value_pairs = [
        ['XXXX', proj_data['id']],
        ['TODAYSDATE', today_date],
        ['CLIENT', proj_data['client']],
        ['PROJECT NAME', proj_data['name']],
        ['PROJECT TYPE', proj_data['item']],
        ['PROPOSAL-URL', proj_data['url']]
    ]
    takeoff_wb = load_workbook(src, read_only=False, keep_vba=True)
    takeoff_ws = takeoff_wb.worksheets[0]
    change_cells_with_values(takeoff_ws, key_value_pairs)
    takeoff_wb.save(dest)
    save_as_xlsm(dest, dest)
    os.remove(dest)


def create_checklist_file(src, dest, proj_data):
    checklist_wb = load_workbook(src, read_only=False, keep_vba=True)
    checklist_ws = checklist_wb.worksheets[0]
    change_adjacent_cell(checklist_ws, 'PROJECT#', proj_data['id'])
    checklist_wb.save(dest)
    save_as_xlsm(dest, dest)
    os.remove(dest)


def create_config_file(src, dest, proj_data):
    key_value_pairs = [
        ['Project Number:', proj_data['id']],
        ['Project Name:', proj_data['name']]
    ]
    config_wb = load_workbook(src, read_only=False, keep_vba=True)
    config_ws = config_wb.worksheets[0]
    change_adjacent_cells_with_values(config_ws, key_value_pairs)
    config_wb.save(dest)
    save_as_xlsm(dest, dest)
    os.remove(dest)


def save_as_xlsm(src, dest):
    app, command = 'Excel.Application', pythoncom.CoInitialize
    excel = client.DispatchEx(app, command())
    excel.DisplayAlerts = False
    wb = excel.Workbooks.Open(str(src))
    filename = str(dest.parent / (dest.stem + '.xlsm'))
    wb.SaveAs(Filename=filename, FileFormat=52, CreateBackup=False)
    wb.Close()

# proj_data = {
#     'id': '1234',
#     'client': 'Adil',
#     'type': 'Neww',
#     'name': 'HELLO WORLD',
#     'url': 'www.google.com'
# }
# create_checklist_file(CHECKLIST_PATH, Path(r"D:\Quotes\Template_Job Opening Checklist_latest.xltm"), proj_data)
