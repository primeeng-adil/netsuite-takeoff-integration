from selenium.webdriver import Keys
from pywebgo import utils

questions = {}
username = ''
password = ''


def set_user_pass_questions(data_keys):
    """

    :param data_keys:
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

    :param argv:
    """
    controller, element = argv[0], argv[1]
    webelement = controller.get_element(element, timeout=20)
    answer = questions[webelement.text]
    index = controller.elem_handler.elements.index(element)
    controller.elem_handler.elements[index + 1]['keys'] = answer + Keys.ENTER


def popup_handler(controller, element):
    """
    Handle any pop-ups that come along during web navigation.

    :param controller:
    :param element:
    """
    if controller.element_exists(element, 2):
        identifiers = utils.get_element_identifiers(element)
        (strategy, locator) = (identifiers['strategy'], identifiers['locator'])
        web_element = controller.find_element(strategy, locator)
        controller.execute_actions(web_element, element)


def get_elements() -> list:
    """
    Return a list of elements.

    :return: Static element list for WebController
    """
    return [
        {'loc': 'id', 'value': 'email', 'action': 'send-keys', 'keys': username},
        {'loc': 'id', 'value': 'password', 'action': 'send-keys', 'keys': password + Keys.ENTER},
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
        {'loc': 'css', 'value': '#custrecord_appfproj_fs_lbl_uir_label + span', 'retrieve': 'text'}
    ]
