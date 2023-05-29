import chromedriver_autoinstaller
import src.middleware.utils as utils
from pywebgo.controller import WebController
from src.consts import CHROME_USER_PROFILE, NETSUITE_URL


def execute_controller(url: list, elements: list) -> WebController:
    """
    Execute controller processes.

    :param url: URL of the landing page
    :param elements: elements for the WebController to process
    :return: instance of WebController
    """
    options = [
        f'user-data-dir={CHROME_USER_PROFILE}',
        'start-maximized'
    ]
    web_controller = WebController(url, options=options, wait=0.2)
    web_controller.run_controller(elements)
    return web_controller


def get_proj_data(controller, elements, proj_options):
    """

    :param controller: current instance of WebController
    :param elements: elements for the project
    :param proj_options: user specified options for the project
    :return: data for the project
    """
    proj_id = utils.get_proj_id(controller)
    proj_client = elements[4]['keys'][:-1]
    proj_rep = elements[7]['keys'][:-1]
    proj_item = elements[15]['keys'][:-1]
    proj_full_name = elements[18]['keys'][:-1]
    proj_type = elements[24]['keys'][:-1]
    proj_name = proj_full_name[proj_full_name.find('_') + 1:]
    proj_url = controller.data_handler.database[1]['data-keys']

    proj_data = {
        'id': proj_id,
        'name': proj_name,
        'item': proj_item,
        'type': proj_type,
        'rep': proj_rep,
        'client': proj_client,
        'url': proj_url
    }

    proj_data.update(proj_options)
    return proj_data


def get_proj_options(data_keys: list) -> dict:
    """
    Get the user specified options for the project.

    :param data_keys: keys sent in by the user through the app interface
    :return: user specified options
    """
    is_logged = data_keys.pop()
    has_config = data_keys.pop()
    proj_path = data_keys.pop()

    return {
        'path': proj_path,
        'config': has_config,
        'log': is_logged
    }


def execute_dirs_files_maker(proj_data: dict) -> None:
    """
    Create project files and directories.

    :param proj_data: data for the project
    """
    utils.make_project_dirs_files(proj_data)


def update_quote_log(proj_data):
    """
    Update the Quote Log if the user specified.

    :param proj_data: data for the project
    """
    if proj_data['log']:
        utils.update_quote_log(proj_data)


def run_middleware(app) -> None:
    """
    Run the middleware.

    :param app: current app object interacting with the user
    """
    app.start_progress()
    data_keys = app.get_data_keys()
    proj_options = get_proj_options(data_keys)

    app.update_progress('Installing Chrome Driver', 5)
    chromedriver_autoinstaller.install()
    app.update_progress('Creating controller elements', 5)
    elements = utils.generate_element_list(data_keys.copy())
    app.update_progress('Executing controller', 10)
    controller = execute_controller([NETSUITE_URL], elements)
    proj_data = get_proj_data(controller, elements, proj_options)
    app.update_progress('Creating project files and directories', 40)
    execute_dirs_files_maker(proj_data)
    app.update_progress('Updating the quote log', 20)
    update_quote_log(proj_data)
    app.update_progress('Finishing', 20)

    controller.close()
    app.stop_progress()
    app.show_success_msg()
