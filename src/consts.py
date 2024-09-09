import csv

NETSUITE_URL = None
GITHUB_SRC = None
CHROME_USER_PROFILE = None
TAKEOFF_PATH = None
CHECKLIST_PATH = None
CONFIG_PATH = None
QUOTE_LOG_PATH = None
DROPDOWN_DIR = None
JOB_DIRS = None
DROPDOWN_PATHS = None


def get_consts_from_csv(app_path):
    result = {}
    const_file_path = app_path / 'data' / 'consts.csv'
    reader = csv.DictReader(open(const_file_path, encoding='utf-8-sig'))
    for row in reader:
        result[row['VAR']] = row['VAL']

    global NETSUITE_URL
    global GITHUB_SRC
    global CHROME_USER_PROFILE
    global TAKEOFF_PATH
    global CHECKLIST_PATH
    global CONFIG_PATH
    global QUOTE_LOG_PATH
    global DROPDOWN_DIR
    global JOB_DIRS
    global DROPDOWN_PATHS

    NETSUITE_URL = result['NETSUITE_URL']
    GITHUB_SRC = result['GITHUB_SRC']
    CHROME_USER_PROFILE = result['CHROME_USER_PROFILE']
    TAKEOFF_PATH = result['TAKEOFF_PATH']
    CHECKLIST_PATH = result['CHECKLIST_PATH']
    CONFIG_PATH = result['CONFIG_PATH']
    QUOTE_LOG_PATH = result['QUOTE_LOG_PATH']
    DROPDOWN_DIR = result['DROPDOWN_DIR']
    JOB_DIRS = [x.strip() for x in result['JOB_DIRS'].split(',')]
    DROPDOWN_PATHS = {
        'addresses': f'{DROPDOWN_DIR}/NetSuite_Daily_SiteAddress_List.csv',
        'customers': f'{DROPDOWN_DIR}/NetSuite_Daily_Customer_List.csv',
        'departments': f'{DROPDOWN_DIR}/NetSuite_Daily_Department_List.csv',
        'classes': f'{DROPDOWN_DIR}/NetSuite_Daily_Class_List.csv',
        'reps': f'{DROPDOWN_DIR}/NetSuite_Daily_SalesRep_List.csv',
        'items': f'{DROPDOWN_DIR}/NetSuite_Daily_Item_List.csv',
        'templates': f'{DROPDOWN_DIR}/NetSuite_Daily_Project_Template_List.csv',
        'types': f'{DROPDOWN_DIR}/NetSuite_Project_Type_List.csv',
    }
