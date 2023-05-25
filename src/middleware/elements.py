from selenium.webdriver import Keys
from pywebgo import utils

"""
Variables to store NetSuite username, password and security questions.
"""
questions = {}
username = ''
password = ''


def set_user_pass_questions(data_keys):
    """
    Sets username, password and security questions for NetSuite.

    :param data_keys: input keys from the user in the app
    """
    global username
    global password
    username = data_keys.pop(0)
    password = data_keys.pop(0)
    questions.update({
        data_keys.pop(0): data_keys.pop(2),
        data_keys.pop(0): data_keys.pop(1),
        data_keys.pop(0): data_keys.pop(0)
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
    Handle any pop-ups that come along during web navigation.

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
        {'loc': 'css', 'value': '#custrecord_appfcust_fs_lbl_uir_label + span input', 'action': 'send-keys'},
        {'loc': 'css', 'value': '#custrecord_appfproposalstatus_fs_lbl_uir_label + span input', 'action': 'send-keys'},
        {'loc': 'css', 'value': '#custrecord_proposalmemo_fs_lbl_uir_label + span input', 'action': 'send-keys'},
        {'loc': 'css', 'value': '#custrecord_proposalsales_fs_lbl_uir_label + span input', 'action': 'send-keys'},
        {'loc': 'css', 'value': '#custrecord_proposaldepartment_fs_lbl_uir_label + span img', 'action': 'click'},
        {'loc': 'css', 'value': '#custrecord_proposaldepartment_fs_lbl_uir_label + span input', 'action': 'send-keys'},
        {'loc': 'css', 'value': '#custrecord_proposalclass_fs_lbl_uir_label + span img', 'action': 'click'},
        {'loc': 'css', 'value': '#custrecord_proposalclass_fs_lbl_uir_label + span input', 'action': 'send-keys'},
        {'loc': 'id', 'value': 'recmachcustrecord_proposallink_custrecord_proposalitem_display', 'action': 'send-keys'},
        {'loc': 'css', 'value': '.uir-popup-select-content tbody td .smalltextnolink', 'action': 'click',
         'custom': popup_handler, 'wait': 0.1},
        {'loc': 'active', 'action': 'send-keys'},
        {'loc': 'active', 'action': 'send-keys'},
        {'loc': 'id', 'value': 'custrecord_appfproj_display', 'action': 'hover'},
        {'loc': 'id', 'value': 'custrecord_appfproj_popup_new', 'action': 'click'},
        {'loc': 'id', 'value': 'companyname', 'action': 'send-keys', 'window': 1},
        {'loc': 'id', 'value': 'parent_display', 'action': 'send-keys', 'window': 1},
        {'loc': 'css', 'value': '.uir-popup-select-content tbody td .smalltextnolink', 'action': 'click',
         'custom': popup_handler, 'wait': 0.1, 'window': 1},
        {'loc': 'css', 'value': '#custentityprime_choose_template_fs_lbl_uir_label + span input', 'action': 'send-keys',
         'window': 1},
        {'loc': 'css', 'value': '#projecttemplate_fs_lbl_uir_label + span img', 'action': 'click', 'window': 1},
        {'loc': 'css', 'value': '#projecttemplate_fs_lbl_uir_label + span input', 'action': 'send-keys', 'window': 1},
        {'loc': 'css', 'value': '#custentity1_fs_lbl_uir_label + span input', 'action': 'send-keys', 'window': 1},
        {'loc': 'css', 'value': '.uir-popup-select-content tbody td .smalltextnolink', 'action': 'click',
         'custom': popup_handler, 'wait': 0.1, 'window': 1},
        {'loc': 'css', 'value': '#jobbillingtype_fs_lbl_uir_label + span input', 'action': 'send-keys', 'window': 1},
        {'loc': 'id', 'value': 'btn_secondarymultibutton_submitter', 'action': 'click', 'window': 1},
        {'loc': 'id', 'value': 'btn_secondarymultibutton_submitter', 'action': 'click'},
        {'loc': 'css', 'value': '#custrecord_appfproj_fs_lbl_uir_label + span', 'retrieve': 'text'},
        {'custom': fetch_current_url, 'retrieve': 'url'}
    ]
