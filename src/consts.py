NETSUITE_URL = r"https://6516658-sb1.app.netsuite.com/app/common/custom/custrecordentry.nl?rectype=207"
CHROME_USER_PROFILE = r'C:\Users\adil.khan\AppData\Local\Google\Chrome\User Data - Copy'
TAKEOFF_PATH = r"D:\Quotes\XXXX_takeoff_1.11.5.xltm"
CHECKLIST_PATH = r"D:\Quotes\Template_Job Opening Checklist_latest.xltm"
CONFIG_PATH = r'D:\Quotes\CONFIGURATOR_latest.xltm'
DROPDOWN_DIR = r'A:/Templates/Take Off Templates/NetSuite data'
JOB_DIRS = ['Correspondence', 'Info to B drive', 'Purchase Order', 'RFQ', 'Specifications', 'Submittal']

DROPDOWN_PATHS = {
    'customers': f'{DROPDOWN_DIR}/NetSuite_Daily_Customer_List.csv',
    'departments': f'{DROPDOWN_DIR}/NetSuite_Daily_Department_List.csv',
    'classes': f'{DROPDOWN_DIR}/NetSuite_Daily_Class_List.csv',
    'reps': f'{DROPDOWN_DIR}/NetSuite_Daily_SalesRep_List.csv',
    'items': f'{DROPDOWN_DIR}/NetSuite_Daily_Item_List.csv',
    'templates': f'{DROPDOWN_DIR}/NetSuite_Daily_Project_Template_List.csv',
    'types': './data/dropdowns/ProjectTypes.csv',
}
