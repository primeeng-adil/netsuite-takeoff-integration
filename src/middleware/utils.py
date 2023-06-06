import re
from pathlib import Path
from src.project import file_gen
from selenium.webdriver import Keys
from src.utility import list_handler, elem_handler
from src.consts import JOB_DIRS, TAKEOFF_PATH, CHECKLIST_PATH, CONFIG_PATH, QUOTE_LOG_PATH


def make_project_dirs_files(proj_data: dict) -> None:
    """
    Create project directories and files.

    :param proj_data: data for the project
    """
    if proj_data['subfac']:
        proj_dir = Path(proj_data['path'], proj_data['subfac'])
    else:
        proj_dir = Path(proj_data['path'])

    if proj_data['scope']:
        job_dir = Path(proj_dir, f"{proj_data['id']}_{proj_data['scope']}")
    else:
        job_dir = Path(proj_dir, f"{proj_data['id']}_{proj_data['type']}")

    for subdir in JOB_DIRS:
        Path(job_dir, subdir).mkdir(parents=True, exist_ok=True)

    excel_ext = ".xltm"
    takeoff_name = f"{proj_data['id']}_{proj_data['item']}_takeoff_1.0.0{excel_ext}"
    checklist_name = f"{proj_data['id']}_Job Opening Checklist_1.0.0{excel_ext}"
    config_name = f"{proj_data['id']}_CONFIGURATOR_1.0.0{excel_ext}"

    takeoff_path = Path(job_dir, takeoff_name)
    checklist_path = Path(job_dir, JOB_DIRS[1], checklist_name)
    config_path = Path(job_dir, config_name)

    file_gen.create_takeoff_file(TAKEOFF_PATH, takeoff_path, proj_data)
    file_gen.create_checklist_file(CHECKLIST_PATH, checklist_path, proj_data)
    if proj_data['config']:
        file_gen.create_config_file(CONFIG_PATH, config_path, proj_data)


def update_quote_log(proj_data):
    """
    Add the project information to the Quote Log.

    :param proj_data: ata for the project
    """
    file_gen.update_quote_log(QUOTE_LOG_PATH, proj_data)


def update_keys_for_elements(data_keys: dict):
    """
    Modify key list to meet custom requirements.

    :param data_keys: keys sent in by the user through the app interface
    """
    data_keys.update({
        'Choose': 'DONE',
        'Milestone': data_keys['Item'].replace('SALES - ', ''),
        'Quantity': '1'
    })


def generate_elements_with_keys(data: dict) -> list:
    """
    Append keys to their respective elements.

    :param data: keys sent in by the user through the app interface
    :return: elements for the project
    """
    update_keys_for_elements(data)
    elements = elem_handler.get_elements()
    list_handler.add_keys_to_elements(data, elements, start=4, term_str=Keys.TAB)
    return elements


def get_proj_id(data: list) -> str:
    """
    Find and return the id of the current project.

    :param data: data scraped by the controller
    :return: job id of the current project
    """
    proj_title = next((item for item in data if item['type'] == 'text'), None)
    if proj_title:
        proj_id = re.search(r'^\S\d+', proj_title['data-keys'])
        if proj_id:
            return proj_id.group()


def get_proj_subfac(data: list) -> str:
    """
    Find and return the subfacility of the current project.

    :param data: data scraped by the controller
    :return: subfacility name of the project
    """
    proj_subfac = next((item for item in data if item['type'] == 'attr[value]'), None)
    if proj_subfac:
        return proj_subfac['data-keys']


def get_proj_url(data: list) -> str:
    """
    Find and return the URL of the current project.

    :param data: data scraped by the controller
    :return: NetSuite URL of the project
    """
    proj_url = next((item for item in data if item['type'] == 'url'), None)
    if proj_url:
        return proj_url['data-keys']

