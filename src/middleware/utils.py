import re
import consts
from pathlib import Path
from project import file_gen
from selenium.webdriver import Keys
from utility import list_handler, elem_handler


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

    proj_data['job-path'] = str(Path(job_dir))
    for subdir in consts.JOB_DIRS:
        Path(job_dir, subdir).mkdir(parents=True, exist_ok=True)

    excel_ext = ".xltm"
    takeoff_name = f"{proj_data['id']}_{proj_data['type']}_takeoff_1.0.0{excel_ext}"
    checklist_name = f"{proj_data['id']}_Job Opening Checklist_1.0.0{excel_ext}"
    config_name = f"{proj_data['id']}_CONFIGURATOR_1.0.0{excel_ext}"

    takeoff_path = Path(job_dir, takeoff_name)
    checklist_path = Path(job_dir, consts.JOB_DIRS[1], checklist_name)
    config_path = Path(job_dir, config_name)

    file_gen.create_takeoff_file(consts.TAKEOFF_PATH, takeoff_path, proj_data)
    file_gen.create_checklist_file(consts.CHECKLIST_PATH, checklist_path, proj_data)
    if proj_data['config']:
        file_gen.create_config_file(consts.CONFIG_PATH, config_path, proj_data)


def update_quote_log(proj_data):
    """
    Add the project information to the Quote Log.

    :param proj_data: data for the project
    """
    file_gen.update_quote_log(consts.QUOTE_LOG_PATH, proj_data)


def update_keys_for_elements(data_keys: dict):
    """
    Modify key list to meet custom requirements.

    :param data_keys: keys entered by the user in the app interface
    """
    data_keys.update({
        'Choose': 'DONE',
        'Milestone': data_keys['Item'].replace('SALES - ', ''),
        'Quantity': '1'
    })


def generate_elements_with_keys(data: dict) -> list:
    """
    Append keys to their respective elements.

    :param data: keys entered by the user in the app interface
    :return: elements for the project
    """
    update_keys_for_elements(data)
    elements = elem_handler.get_elements()
    list_handler.add_keys_to_elements(data, elements, start=4, term_str=Keys.TAB)
    return elements


def get_proj_id(data: list) -> str:
    """
    Find and return the id of the current project.

    :param data: data scraped by the controller during runtime
    :return: job id of the current project
    """
    proj_title = next((item for item in data if item['type'] == 'text'), None)
    if proj_title:
        proj_id = re.search(r'^\S\d+', proj_title['data-keys'])
        if proj_id:
            return proj_id.group()


def get_proj_subfac(data: dict) -> str:
    """
    Find and return the subfacility of the current project.

    :param data: data scraped by the controller during runtime
    :return: subfacility name of the project
    """
    proj_title_words = [word.strip() for word in data['Name'].split('|')]
    if len(proj_title_words) == 3:
        return proj_title_words[2]


def get_proj_url(data: list) -> str:
    """
    Find and return the URL of the current project.

    :param data: data scraped by the controller during runtime
    :return: NetSuite URL of the project
    """
    proj_url = next((item for item in data if item['type'] == 'url'), None)
    if proj_url:
        return proj_url['data-keys']

