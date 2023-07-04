from pathlib import Path

import consts
import webbrowser
import chromedriver_autoinstaller
import middleware.utils as utils
from pywebgo.controller import WebController
from utility.elem_handler import set_user_pass_questions


def execute_controller(url: list, elements: list, wait: float) -> WebController:
    """
    Execute WebController processes.

    :param url: URL of the landing page
    :param elements: elements for the WebController to process
    :param wait: delay (in seconds) before executing each action
    :return: instance of WebController
    """
    chrome_profile_path = str(Path.home() / Path(consts.CHROME_USER_PROFILE))
    options = [
        f'user-data-dir={chrome_profile_path}',
        'start-maximized',
        'disable-infobars',
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-extensions'
    ]
    web_controller = WebController(url, options=options, wait=wait)
    web_controller.run_controller(elements)
    return web_controller


def get_proj_data(data_fetched, data, proj_options):
    """

    :param data_fetched: data retrieved by the controller during runtime
    :param data: keys entered by the user in the app interface
    :param proj_options: user specified options for the project
    :return: data for the project
    """
    proj_item = data['Item']
    proj_client = data['Customer']
    proj_type = data['Project Type']
    proj_scope = data['Project Scope']
    proj_rep = data['Proposal Sales Rep']
    proj_name = f"{proj_client}_{proj_scope}"
    proj_id = utils.get_proj_id(data_fetched)
    proj_url = utils.get_proj_url(data_fetched)
    proj_subfac = utils.get_proj_subfac(data_fetched)

    proj_data = {
        'id': proj_id,
        'name': proj_name,
        'scope': proj_scope,
        'type': proj_type,
        'item': proj_item,
        'rep': proj_rep,
        'client': proj_client,
        'subfac': proj_subfac,
        'url': proj_url
    }

    proj_data.update(proj_options)
    return proj_data


def get_proj_options(data: dict) -> dict:
    """
    Get the user specified options for the project.

    :param data: keys entered by the user in the app interface
    :return: user specified options
    """
    proj_path = data.pop('Project Path')
    has_config = data.pop('Configurator')
    is_logged = data.pop('Quote Log')

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
    data = app.get_data()
    set_user_pass_questions(data)
    proj_options = get_proj_options(data)

    app.update_progress('Installing Chrome Driver', 5)
    chromedriver_autoinstaller.install()

    app.update_progress('Creating controller elements', 5)
    elements = utils.generate_elements_with_keys(data)

    app.update_progress('Executing controller', 10)

    controller = execute_controller([consts.NETSUITE_URL], elements, app.settings['delay'].get())
    proj_data = get_proj_data(controller.data_handler.database, data, proj_options)

    controller.close()
    webbrowser.open(proj_data['url'])

    app.update_progress('Creating project files and directories', 40)
    execute_dirs_files_maker(proj_data)

    app.update_progress('Updating the quote log', 20)
    update_quote_log(proj_data)

    app.update_progress('Finishing', 20)
    app.stop_progress()
    app.show_success_msg()
