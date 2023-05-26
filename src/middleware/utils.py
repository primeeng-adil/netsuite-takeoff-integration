import re
from pathlib import Path
from pywebgo.controller import WebController
from src.project import file_gen
from selenium.webdriver import Keys
from src.utility import list_handler
from .elements import get_elements, set_user_pass_questions
from src.consts import JOB_DIRS, TAKEOFF_PATH, CHECKLIST_PATH, CONFIG_PATH, QUOTE_LOG_PATH


def make_project_dirs_files(proj_data: dict) -> None:
    """
    Create project directories and files.

    :param proj_data: data for the project
    """

    proj_dir = Path(proj_data['path'], proj_data['name'])
    job_dir = Path(proj_dir, f"{proj_data['id']}_{proj_data['item']}")

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


def modify_data_keys(data_keys: list) -> None:
    """
    Modify key list to meet custom requirements.

    :param data_keys: keys sent in by the user through the app interface
    """
    data_keys[7] += '_' + data_keys.pop(8) + '_' + data_keys.pop(8)
    data_keys.insert(7, data_keys[6].replace('SALES - ', ''))
    for i in range(len(data_keys)):
        data_keys[i] += Keys.TAB
    data_keys.insert(7, Keys.TAB)
    data_keys.insert(11, 'DONE')
    data_keys[-1] += Keys.TAB


def generate_element_list(data_keys: list) -> list:
    """
    Append keys to their respective elements.

    :param data_keys: keys sent in by the user through the app interface
    :return: elements for the project
    """
    set_user_pass_questions(data_keys)
    modify_data_keys(data_keys)
    elements = get_elements()
    list_handler.add_keys_to_elements(data_keys, elements, start=4)
    return elements


def get_proj_id(controller: WebController) -> str:
    """
    Find and return the project id of the current project.

    :param controller: current instance of WebController
    :return: job id of the current project
    """
    proj_id = None
    if controller.data_handler.retrieve_data():
        proj_title = controller.data_handler.retrieve_data()[0]['data-keys']
        proj_id = re.search(r'^\S\d+', proj_title)
    if proj_id:
        return proj_id.group()
