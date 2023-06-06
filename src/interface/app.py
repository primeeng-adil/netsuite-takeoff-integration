import ctypes
import itertools
import PIL.Image
from PIL import ImageTk
from tkinter import *
from tkinter.ttk import *
import src.interface.utils as utils
from pathlib import Path
from threading import Thread, Event
from src.utility import csv_handler
from src.consts import DROPDOWN_PATHS
from src.middleware.middleware import run_middleware

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class App(Tk):

    def __init__(self):
        super().__init__()
        self.event = Event()
        self.pause = False

        self.pb_status = None
        self.pb = None
        self.pb_window = None
        self.tabs = []
        self.tab_grid = []
        self.data_vars = {}
        self.elements = []
        self.pad_x = 40
        self.default_csv_path = Path.home() / 'Documents' / 'Netsuite Inputs'

        utils.adjust_window(self, "NetSuite Takeoff Integration - v1.0.1", 850, 725)

        self.__add_icon()
        self.__add_menu()
        logo = self.__add_logo()

        tab_titles = [
            '   Login   ',
            '   Proposal   ',
            '   Project   ',
        ]

        self.__create_tabs(3, titles=tab_titles)
        self.__design_tabs()
        self.__add_cmd_buttons()
        self.__customize()

        self.mainloop()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    def __add_icon(self):
        self.iconbitmap(Path('./data/icon.ico'))

    def __add_logo(self):
        maxsize = (200, 200)
        logo = PIL.Image.open(Path('./data/logo.png'))
        logo.thumbnail(maxsize)
        img = ImageTk.PhotoImage(logo)
        logo_panel = Label(self, image=img)
        logo_panel.pack(pady=(20, 0), anchor='center', padx=(0, 35))
        return img

    def __add_menu(self):

        file_cmd_funcs = [
            ['Load Login', self.load_login],
            ['Load Login As', self.load_login_as],
            ['Save Login', self.save_login],
            ['Save Login As...', self.save_login_as],
            ['Load Details', self.load_inputs],
            ['Load Details As', self.load_inputs_as],
            ['Save Details', self.save_inputs],
            ['Save Details As...', self.save_inputs_as],
            ['Settings', self.view_settings],
            ['Update Dropdowns', self.empty],
            ['Exit', self.destroy]
        ]
        edit_cmd_funcs = [
            ['Clear Inputs', self.clear_inputs],
            ['Autofill Inputs', self.empty]
        ]
        help_cmd_funcs = [
            ['User Guide', self.empty],
            ['Source Code', self.empty],
            ['Check for Updates...', self.empty],
            ['About', self.empty]
        ]

        menu_bar = Menu(self)
        file = Menu(menu_bar, tearoff=0)
        edit = Menu(menu_bar, tearoff=0)
        help_ = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file)
        menu_bar.add_cascade(label='Edit', menu=edit)
        menu_bar.add_cascade(label='Help', menu=help_)

        utils.fill_menu_cascade(file, file_cmd_funcs, [3, 7, 8, 9])
        utils.fill_menu_cascade(edit, edit_cmd_funcs, [])
        utils.fill_menu_cascade(help_, help_cmd_funcs, [1])
        self.config(menu=menu_bar)

    def __create_tabs(self, count, titles):
        tab_controller = Notebook(self)
        for i in range(count):
            self.tabs.append(Frame(tab_controller))
            tab_controller.add(self.tabs[i], text=titles[i])
        tab_controller.pack(expand=1, fill='both', padx=20, pady=(10, 0))

    def __design_tabs(self):
        self.tab_grid.append([12, 2])
        self.tab_grid.append([12, 2])
        self.tab_grid.append([12, 2])

        utils.create_grid(self.tabs[0], *self.tab_grid[0])
        utils.create_grid(self.tabs[1], *self.tab_grid[1])
        utils.create_grid(self.tabs[2], *self.tab_grid[2])

        self.__add_elements_login()
        self.__add_elements_proposal()
        self.__add_elements_project()

    def __add_browse_button(self, tab, row, col, command):
        button = Button(self.tabs[tab], text="Browse", command=lambda: command(self.data_vars['Project Path']))
        button.grid(row=row, column=col, sticky=W, padx=self.pad_x, pady=15)

    def start_progress(self):
        self.pb_status = StringVar()
        self.pb_window = utils.open_new_window(self, "Progress", 400, 300, 6, 3)
        self.pb = Progressbar(self.pb_window, orient=HORIZONTAL, mode='determinate')
        self.pb.grid(row=2, column=0, columnspan=3, sticky=EW, padx=20)

        self.pb_status.set("Initializing...")
        status_label = Label(self.pb_window, textvariable=self.pb_status)
        status_label.grid(row=1, column=0, columnspan=3, sticky=W, padx=20)

        log = Listbox(self.pb_window, height=6, fg='orange')
        log.grid(column=0, columnspan=3, sticky=EW, padx=20)

        pb_button = Button(self.pb_window, text="End", command=self.pb_window.destroy)
        pb_button.grid(row=4, column=0, columnspan=3, sticky=W, padx=20, ipadx=5)
        pb_button = Button(self.pb_window, text="Pause", command=self.pause_execution)
        pb_button.grid(row=4, column=0, columnspan=3, sticky=W, padx=(135, 0), ipadx=5)
        pb_button = Button(self.pb_window, text="Resume", command=self.resume_execution)
        pb_button.grid(row=4, column=0, columnspan=3, sticky=W, padx=(250, 0), ipadx=5)

    def stop_progress(self):
        self.pb.grid_forget()
        self.pb.destroy()
        self.pb_window.destroy()

    def update_progress(self, status, inc):
        self.pb_status.set(status + '...')
        self.pb['value'] += inc

    def __add_elements_login(self):
        utils.add_heading(self, 'Login Info', 0, 0)
        utils.add_fields(self, [
            ['entry', 'Username:'],
            ['entry', 'Password:']
        ], 0, 1, 0)
        utils.add_heading(self, 'Security Questions', 0, 5)
        utils.add_fields(self, [
            ['entry', 'Question 1:'],
            ['entry', 'Question 2:'],
            ['entry', 'Question 3:']
        ], 0, 6, 0)
        utils.add_fields(self, [
            ['entry', 'Answer 1:'],
            ['entry', 'Answer 2:'],
            ['entry', 'Answer 3:']
        ], 0, 6, 1)

    def __add_elements_proposal(self):
        departments = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['departments']), header=True)
        classes = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['classes']), header=True)
        reps = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['reps']), header=True)
        customers = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['customers']), header=True)
        items = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['items']), header=True)

        status = ['Initial Review', 'Submitted', 'Closed Won', 'Closed Lost']
        utils.add_heading(self, 'Proposal Info', 1, 0)
        utils.add_fields(self, [
            ['combo', 'Customer:', customers],
            ['combo', 'Status:', status],
            ['entry', 'Memo:'],
            ['combo', 'Proposal Sales Rep:', reps]
        ], 1, 1, 0)
        utils.add_fields(self, [
            ['combo', 'Department:', departments],
            ['combo', 'Class:', classes],
            ['combo', 'Item:', items]
        ], 1, 1, 1)

    def __add_elements_project(self):
        templates = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['templates']), header=True)
        types = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['types']), header=True)
        addresses = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['addresses']), column=1, header=True)
        billing = ['Charge-Based', 'Fixed Bid, Interval', 'Fixed Bid, Milestone', 'Time and Materials']
        utils.add_heading(self, 'Project Info', 2, 0)
        utils.add_fields(self, [
            ['combo', 'Site Address:', addresses],
            ['entry', 'Project Scope:'],
            ['entry', 'Project Path:']
        ], 2, 1, 0)
        utils.add_fields(self, [
            ['combo', 'Project Template:', templates],
            ['combo', 'Project Type:', types],
            ['combo', 'Billing Type:', billing]
        ], 2, 1, 1)

    def __add_cmd_buttons(self):
        run_btn = Button(self, text="Run", command=self.run_controller)
        run_btn.pack(side=LEFT, padx=(self.pad_x + 20, 0), pady=40, ipadx=30)
        exit_btn = Button(self, text="Exit", command=self.destroy)
        exit_btn.pack(side=RIGHT, padx=(0, self.pad_x + 20), pady=40, ipadx=30)

    def __customize(self):
        self.elements[1].config(show="*")
        for i in range(5, 8):
            self.elements[i].config(show="*")

        self.data_vars['Status'].set('Initial Review')
        self.data_vars['Memo'].set('2.0.0 – base bid')
        self.__add_browse_button(2, 7, 0, utils.browse_directory)

        bool_var = BooleanVar()
        bool_var.set(True)
        cb = Checkbutton(self.tabs[2], text='Configurator', variable=bool_var, onvalue=True, offvalue=False)
        cb.grid(row=7, column=1, sticky=W, padx=self.pad_x)
        self.data_vars.update({'Configurator': bool_var})

        bool_var = BooleanVar()
        bool_var.set(False)
        cb = Checkbutton(self.tabs[2], text='Quote Log', variable=bool_var, onvalue=True, offvalue=False)
        cb.grid(row=8, column=1, sticky=NW, padx=self.pad_x)
        self.data_vars.update({'Quote Log': bool_var})

    def save_login(self):
        utils.save(self.data_vars, self.default_csv_path / 'login_info.csv', end=8)

    def save_login_as(self):
        utils.save_as(self.data_vars, 'login_data.csv', end=8)

    def load_login(self):
        try:
            utils.load(self.data_vars, self.default_csv_path / 'login_info.csv')
        except FileNotFoundError:
            utils.messagebox.showerror('File Not Found', 'No saved login information '
                                                         'found from the previous run.')

    def load_login_as(self):
        utils.load_as(self.data_vars)

    def save_inputs(self):
        utils.save(self.data_vars, self.default_csv_path / 'last_inputs.csv', start=8, end=len(self.data_vars))

    def save_inputs_as(self):
        utils.save_as(self.data_vars, 'input_data.csv', start=8, end=len(self.data_vars))

    def load_inputs(self):
        utils.load(self.data_vars, self.default_csv_path / 'last_inputs.csv')

    def load_inputs_as(self):
        utils.load_as(self.data_vars)

    def __error_handler(self):
        req_vars = dict(itertools.islice(self.data_vars.items(), 2))
        req_vars.update(dict(itertools.islice(self.data_vars.items(), 8, len(self.data_vars) - 2)))
        req_vars.pop('Project Scope')
        for key in req_vars:
            req_var = req_vars[key]
            if isinstance(req_var, StringVar) and not req_var.get() or req_var.get() == 'Select...':
                utils.messagebox.showerror('Input Error', f"Enter value for '{key}'.")
                return True
        return False

    def clear_inputs(self):
        for key in self.data_vars:
            var = self.data_vars[key]
            if isinstance(var, StringVar):
                var.set('')
            elif isinstance(var, BooleanVar):
                var.set(False)

    def get_data(self):
        data_dict = {}
        for key in self.data_vars:
            data_dict.update({key: self.data_vars[key].get()})
        return data_dict

    @staticmethod
    def show_success_msg():
        utils.show_success_msg()

    def run_controller(self):
        if self.__error_handler():
            return
        execution_thread = Thread(target=run_middleware, args=(self,))
        execution_thread.daemon = True
        execution_thread.start()

    def view_settings(self):
        pass

    def empty(self):
        pass

    def pause_execution(self):
        self.pause = True

    def resume_execution(self):
        self.pause = False
