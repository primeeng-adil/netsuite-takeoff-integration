import sys
import consts
from pathlib import Path
from interface.app import App


if __name__ == '__main__':
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        app_path = Path(sys._MEIPASS)
    else:
        app_path = Path(__file__).parent
    consts.get_consts_from_csv()
    try:
        app = App(app_path)
    except FileNotFoundError as error:
        App.show_startup_error_msg(str(error))
    except Exception as error:
        App.show_startup_error_msg("Unexpected error occurred.")
