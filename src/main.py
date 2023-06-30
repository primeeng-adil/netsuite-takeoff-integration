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
    app = App(app_path)
