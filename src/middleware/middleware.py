import re
from pathlib import Path
from selenium.webdriver import Keys
from src.sharepoint.dir_handler import DirHandler
from src.utility import list_handler
from pywebgo.controller import WebController
from .elements import get_elements, set_user_pass_questions
from src.consts import *


def modify_data_keys(data_keys: list) -> None:
    """
    Modify keys list to meet custom requirements.

    :param data_keys: keys sent in by the user through the app interface
    """
    data_keys[7] += '_' + data_keys.pop(8) + '_' + data_keys.pop(8)
    data_keys.insert(7, data_keys[6].replace('SALES - ', ''))
    for i in range(len(data_keys)):
        data_keys[i] += Keys.TAB
    data_keys.insert(7, Keys.TAB)
    data_keys.insert(11, 'DONE')
    data_keys[-1] += Keys.TAB


def get_proj_id(controller: WebController) -> str:
    """
    Find and return the job id of the current project.

    :param controller: WebController instance containing the current elements list
    :return: job id of the current project
    """
    proj_id = None
    if controller.data_handler.retrieve_data():
        proj_title = controller.data_handler.retrieve_data()[0]['data-keys']
        proj_id = re.search(r'^\S\d+', proj_title)
    if proj_id:
        return proj_id.group()


def generate_element_list(data_keys: list) -> tuple:
    """
    Append keys to their respective elements and return elements and sharepoint path.

    :param data_keys: keys sent in by the user through the app interface
    :return: elements for WebController and relative sharepoint path for the project
    """
    set_user_pass_questions(data_keys)
    sharepoint_path = data_keys.pop(14)
    modify_data_keys(data_keys)
    elements = get_elements()
    list_handler.add_keys_to_elements(data_keys, elements, start=4)
    return elements, sharepoint_path


def make_sharepoint_dirs(sharepoint_path: str, proj_id: str, proj_name: str, proj_item: str, creds: tuple) -> None:
    """
    Create project directories and files in SharePoint.

    :param sharepoint_path: relative SharePoint path to create site directory in
    :param proj_id: job id of the current project
    :param proj_name: job name of the current project
    :param proj_item: item type of the current project
    :param creds: username and password of the current user
    """
    root_url = "/sites/InternalDev/"
    site_url = f"{sharepoint_path}/{proj_name}"
    proj_url = f"{site_url}/{proj_id}_{proj_item}"
    takeoff_new_name = Path(TAKEOFF_URL).parts[-1].replace('XXXX-', f'{proj_id}_{proj_item}_')
    checklist_new_name = f'{proj_id}_Job Opening Checklist_1.0.0.xltm'
    dirs = ['Correspondence', 'Info to B drive', 'Purchase Order', 'RFQ', 'Specifications', 'Submittal']

    dir_handler = DirHandler(SHAREPOINT_URL, creds)
    proj_url = Path(dir_handler.make_proj_dir(proj_url))
    proj_rel_url = str(proj_url.relative_to(Path(root_url)))
    dir_handler.make_proj_subdir(dirs, proj_rel_url)
    takeoff_dest_url = str(Path(proj_rel_url, takeoff_new_name))
    checklist_dest_url = str(Path(proj_rel_url, 'Info to B drive', checklist_new_name))
    dir_handler.copy_file(TAKEOFF_URL, takeoff_dest_url)
    dir_handler.copy_file(CHECKLIST_URL, checklist_dest_url)


def execute_controller(url: list, elements: list) -> WebController:
    """
    Execute WebController processes.

    :param url: URL of the landing page
    :param elements: elements for the WebController to process
    :return: instance of WebController
    """
    web_controller = WebController(url, wait=0.3)
    web_controller.run_controller(elements)
    return web_controller


def execute_sharepoint(sharepoint_path: str, controller: WebController, elements: list) -> None:
    """
    Execute SharePoint processes.

    :param sharepoint_path: relative sharepoint path to save the current project to
    :param controller: WebController instance containing the current elements list
    :param elements: elements passed into the WebController classed
    """
    proj_id = get_proj_id(controller)
    username = elements[0]['keys']
    password = elements[1]['keys'][:-1]
    proj_item = elements[15]['keys'][:-1]
    proj_full_name = elements[18]['keys'][:-1]
    proj_name = proj_full_name[proj_full_name.find('_') + 1:]
    make_sharepoint_dirs(sharepoint_path, proj_id, proj_name, proj_item, (username, password))


def run_middleware(app) -> None:
    """
    Run the middleware.

    :param app: current app object interacting with the user
    """
    app.start_progress()
    data = app.get_data()
    app.update_progress('Creating elements', 10)
    elements, sharepoint_path = generate_element_list(data)
    app.update_progress('Executing controller', 10)
    controller = execute_controller([NETSUITE_URL], elements)
    app.update_progress('Creating SharePoint directories', 60)
    execute_sharepoint(sharepoint_path, controller, elements)
    app.update_progress('Finishing', 20)
    controller.close()
    app.stop_progress()
    app.show_success_msg()
