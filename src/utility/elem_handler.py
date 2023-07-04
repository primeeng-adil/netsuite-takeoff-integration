from selenium.webdriver import Keys
from pywebgo import utils

"""
Variables to store NetSuite username, password and security questions.
"""
questions = {}
username = ''
password = ''


def set_user_pass_questions(data):
    """
    Sets username, password and security questions for NetSuite.

    :param data: input keys from the user in the app
    """
    global username
    global password
    username = data.pop('Username')
    password = data.pop('Password')
    questions.update({
        data.pop('Question 1'): data.pop('Answer 1'),
        data.pop('Question 2'): data.pop('Answer 2'),
        data.pop('Question 3'): data.pop('Answer 3')
    })


def validate_func(*argv):
    """
    Answers the security question in NetSuite if prompted.

    :param argv: controller, element
    """
    controller, element = argv[0], argv[1]
    if controller.element_exists(controller.elem_handler.elements[4]):
        index = controller.elem_handler.elements.index(element)
        answer_element = controller.elem_handler.elements[index + 1]
        controller.elem_handler.elements.remove(answer_element)
        return

    webelement = controller.get_element(element, timeout=5)
    answer = questions[webelement.text]
    index = controller.elem_handler.elements.index(element)
    controller.elem_handler.elements[index + 1]['keys'] = answer + Keys.ENTER


def popup_handler(controller, element):
    """
    Handle any pop-up prompts that come along during runtime.

    :param controller: current instance of the controller
    :param element: current element in execution
    """
    if controller.element_exists(element, 1):
        identifiers = utils.get_element_identifiers(element)
        (strategy, locator) = (identifiers['strategy'], identifiers['locator'])
        web_element = controller.find_element(strategy, locator)
        controller.execute_actions(web_element, element)


def check_for_auto_populate(*argv):
    """
    Fill username and password fields only if they are not autopopulated.

    :param argv: controller, element
    """
    controller, element = argv[0], argv[1]
    web_element = controller.get_element(element, timeout=5)
    web_element.click()
    if web_element.get_attribute('value') != '':
        if web_element.get_attribute('id') == 'password':
            web_element.send_keys(Keys.ENTER)
        return

    if web_element.get_attribute('id') == 'email':
        web_element.send_keys(username)
    if web_element.get_attribute('id') == 'password':
        web_element.send_keys(password + Keys.ENTER)


def fetch_current_url(*argv):
    """
    Get the url of the current web page.

    :param argv: controller, element
    """
    controller, element = argv[0], argv[1]
    index = controller.elem_handler.elements.index(element)
    controller.data_handler.add_data(index, element['retrieve'], controller.current_url)


def get_elements() -> list:
    """
    Return a list of elements.

    :return: static element list for WebController
    """
    return [
        {'loc': 'id', 'value': 'email', 'custom': check_for_auto_populate},
        {'loc': 'id', 'value': 'password', 'custom': check_for_auto_populate},
        {'loc': 'css', 'value': r'tbody tbody tr td.smalltextnolink.text-opensans', 'custom': validate_func},
        {'loc': 'name', 'value': 'answer', 'action': 'send-keys'},
        {'loc': 'name', 'value': 'custrecord_appfcust_display', 'action': 'send-keys', 'keys': 'Customer'},
        {'loc': 'name', 'value': 'inpt_custrecord_appfproposalstatus', 'action': 'send-keys', 'keys': 'Status'},
        {'loc': 'name', 'value': 'custrecord_proposalmemo', 'action': 'send-keys', 'keys': 'Memo'},
        {'loc': 'name', 'value': 'inpt_custrecord_proposalsales', 'action': 'send-keys', 'keys': 'Proposal Sales Rep'},
        {'loc': 'name', 'value': 'inpt_custrecord_proposaldepartment', 'action': 'send-keys click',
         'keys': 'Department'},
        {'loc': 'name', 'value': 'inpt_custrecord_proposalclass', 'action': 'send-keys click', 'keys': 'Class'},
        {'loc': 'id', 'value': 'recmachcustrecord_proposallink_custrecord_proposalitem_display',
         'action': 'send-keys', 'keys': 'Item'},
        {'loc': 'css', 'value': '.uir-popup-select-content tbody td .smalltextnolink', 'action': 'click',
         'custom': popup_handler},
        {'loc': 'css', 'value': 'td[data-ns-tooltip="MILESTONE NAME"]', 'action': 'click'},
        {'loc': 'name', 'value': 'custrecord_proposalmilestone', 'action': 'send-keys', 'keys': 'Milestone'},
        {'loc': 'css', 'value': 'td[data-ns-tooltip="QUANTITY"]', 'action': 'click'},
        {'loc': 'name', 'value': 'custrecord_proposalquantity_formattedValue', 'action': 'send-keys',
         'keys': 'Quantity'},
        {'loc': 'id', 'value': 'custrecord_appfproj_display', 'action': 'hover'},
        {'loc': 'id', 'value': 'custrecord_appfproj_popup_new', 'action': 'click'},
        {'loc': 'name', 'value': 'parent_display', 'action': 'send-keys', 'keys': 'Customer', 'window': 1},
        {'loc': 'css', 'value': '.uir-popup-select-content tbody td .smalltextnolink', 'action': 'click',
         'custom': popup_handler, 'window': 1},
        {'loc': 'name', 'value': 'inpt_custentityprime_choose_template', 'action': 'send-keys click',
         'keys': 'Choose', 'window': 1},
        {'loc': 'name', 'value': 'inpt_projecttemplate', 'action': 'send-keys click',
         'keys': 'Project Template', 'window': 1},
        {'loc': 'name', 'value': 'custentityprime_project_scope', 'action': 'send-keys',
         'keys': 'Project Scope', 'window': 1},
        {'loc': 'id', 'value': 'custentity1_display', 'action': 'send-keys',
         'keys': 'Project Type', 'window': 1},
        {'loc': 'css', 'value': '.uir-popup-select-content tbody td .smalltextnolink', 'action': 'click',
         'custom': popup_handler, 'window': 1},
        {'loc': 'name', 'value': 'custentityprime_project_site_address_display', 'action': 'send-keys',
         'keys': 'Site Address', 'window': 1},
        {'loc': 'css', 'value': '.uir-popup-select-content tbody td .smalltextnolink', 'action': 'click',
         'custom': popup_handler, 'window': 1},
        {'loc': 'name', 'value': 'custentityprime_project_site_subfacility', 'retrieve': 'attr[value]', 'window': 1},
        {'loc': 'name', 'value': 'inpt_jobbillingtype', 'action': 'send-keys', 'keys': 'Billing Type', 'window': 1},
        {'loc': 'id', 'value': 'btn_secondarymultibutton_submitter', 'action': 'click', 'window': 1},
        {'loc': 'id', 'value': 'btn_secondarymultibutton_submitter', 'action': 'click'},
        {'loc': 'css', 'value': '#custrecord_appfproj_fs_lbl_uir_label + span', 'retrieve': 'text'},
        {'custom': fetch_current_url, 'retrieve': 'url'}
    ]
