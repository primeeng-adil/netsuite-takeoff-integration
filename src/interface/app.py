import sys
import ctypes
import itertools
import webbrowser
import PIL.Image
from PIL import ImageTk
from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from threading import Thread, Event
from interface import utils
from utility import csv_handler
from pywebgo.controller import WebController
from middleware.middleware import run_middleware
from consts import DROPDOWN_PATHS, CHROME_USER_PROFILE, NETSUITE_URL

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class App(Tk):
    """
    Main application class for the NetSuite Takeoff Integration.

        Attributes:
        event (Event): An Event object to control the execution of the application.
        pause (bool): A boolean indicating whether the execution of the application is paused or not.
        pb_status (StringVar): A StringVar object to store the status of the progress bar.
        pb (Progressbar): A Progressbar widget to display the progress of the application.
        pb_window (Tk): A Tk window to display the progress bar and status.
        tabs (list): A list to store the frames for each tab in the application.
        tab_grid (list): A list to store the grid configurations for each tab.
        data_vars (dict): A dictionary to store the tkinter variables for various data fields.
        settings (dict): A dictionary to store the application settings.
        elements (list): A list to store the tkinter elements added to the application.
        pad_x (int): The padding value for the x-axis.
        default_csv_path (Path): The default path for CSV files.
    """

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
        self.settings = {}
        self.elements = []
        self.pad_x = 40
        self.default_csv_path = None
        self.settings_window = None

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            self.data_path = Path(sys._MEIPASS, 'data')
        else:
            self.data_path = Path(__package__).resolve().parent / 'data'

        utils.adjust_window(self, "NetSuite Takeoff Integration - v1.0.1", 850, 725)

        self.__add_icon()
        self.__add_menu()
        logo = self.__add_logo()

        tab_titles = [
            '   Login   ',
            '   Proposal   ',
            '   Project   ',
        ]

        self.settings.update({
            'delay': DoubleVar(),
            'csv-path': StringVar(),
            'config': BooleanVar(),
            'log': BooleanVar(),
            'status': StringVar(),
            'memo': StringVar()
        })

        self.__create_tabs(3, titles=tab_titles)
        self.__load_settings()
        self.__design_tabs()
        self.__add_cmd_buttons()
        self.__customize()

        self.mainloop()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Clean up and exit the application.
        """
        self.destroy()

    def __add_icon(self):
        """
        Add the application icon.
        """
        self.iconbitmap(Path(self.data_path, 'icon.ico'))

    def __add_logo(self) -> PhotoImage:
        """
        Add the logo image to the application.
        :return: logo image
        """
        maxsize = (200, 200)
        logo = PIL.Image.open(Path(self.data_path, 'logo.png'))
        logo.thumbnail(maxsize)
        img = ImageTk.PhotoImage(logo)
        logo_panel = Label(self, image=img)
        logo_panel.pack(pady=(20, 0), anchor='center', padx=(0, 35))
        return img

    def __add_menu(self):
        """
        Add the menu to the application.
        """
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
            ['Exit', self.destroy]
        ]
        edit_cmd_funcs = [
            ['Open Browser', self.open_chromedriver],
            ['Clear Inputs', self.clear_inputs]
        ]
        help_cmd_funcs = [
            ['User Guide', self.empty],
            ['GitHub Repo', self.open_github],
            ['Check for Updates...', self.check_updates],
            ['About', self.empty]
        ]

        menu_bar = Menu(self)
        file = Menu(menu_bar, tearoff=0)
        edit = Menu(menu_bar, tearoff=0)
        help_ = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file)
        menu_bar.add_cascade(label='Edit', menu=edit)
        menu_bar.add_cascade(label='Help', menu=help_)

        utils.fill_menu_cascade(file, file_cmd_funcs, [3, 7, 8])
        utils.fill_menu_cascade(edit, edit_cmd_funcs, [])
        utils.fill_menu_cascade(help_, help_cmd_funcs, [1])
        self.config(menu=menu_bar)

    def __load_settings(self):
        """
        Load the application settings from a CSV file.
        """
        utils.load(self.settings, Path(self.data_path, 'settings.csv'))
        self.default_csv_path = Path(self.settings['csv-path'].get())
        if not self.default_csv_path.is_dir() or self.default_csv_path:
            self.default_csv_path = Path.home() / 'Documents' / 'Netsuite Inputs'
            self.settings['csv-path'].set(str(self.default_csv_path))

    def __create_tabs(self, count: int, titles: list):
        """
        Create the tabs for the application.

        :param count: number of tabs
        :param titles: titles of the tabs
        """
        tab_controller = Notebook(self)
        for i in range(count):
            self.tabs.append(Frame(tab_controller))
            tab_controller.add(self.tabs[i], text=titles[i])
        tab_controller.pack(expand=1, fill='both', padx=20, pady=(10, 0))

    def __design_tabs(self):
        """
        Design and add the content of each tab.
        """
        self.tab_grid.append([12, 2])
        self.tab_grid.append([12, 2])
        self.tab_grid.append([12, 2])

        utils.create_grid(self.tabs[0], *self.tab_grid[0])
        utils.create_grid(self.tabs[1], *self.tab_grid[1])
        utils.create_grid(self.tabs[2], *self.tab_grid[2])

        self.__add_elements_login()
        self.__add_elements_proposal()
        self.__add_elements_project()

    def __add_elements_login(self):
        """
        Add the elements for the login tab.
        """
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
        """
        Add the elements for the proposal tab.
        """
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
        """
        Add the elements for the project tab.
        """
        templates = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['templates']), header=True)
        types = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['types']), header=True)
        addresses = csv_handler.read_csv_column(Path(DROPDOWN_PATHS['addresses']), header=True)
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
        """
        Add the command buttons for running and exiting the application.
        """
        run_btn = Button(self, text="Run", command=self.run_controller)
        run_btn.pack(side=LEFT, padx=(self.pad_x + 20, 0), pady=40, ipadx=30)
        exit_btn = Button(self, text="Exit", command=self.destroy)
        exit_btn.pack(side=RIGHT, padx=(0, self.pad_x + 20), pady=40, ipadx=30)

    def __customize(self):
        """
        Customize the appearance and behavior of certain elements.
        """
        self.elements[1].config(show="*")
        for i in range(5, 8):
            self.elements[i].config(show="*")

        self.data_vars['Status'].set(self.settings['status'].get())
        self.data_vars['Memo'].set(self.settings['memo'].get())
        self.add_browse_button(self.tabs[2], 7, 0, self.pad_x, utils.browse_directory, self.data_vars['Project Path'])

        tooltip = Label(self.tabs[2], text='(Not required)')
        tooltip.grid(row=3, column=0, sticky=E, padx=self.pad_x)
        tooltip = Label(self.tabs[0], text='(Not required)')
        tooltip.grid(row=5, column=0, sticky=E, padx=self.pad_x)

        bool_var = BooleanVar()
        bool_var.set(self.settings['config'].get())
        cb = Checkbutton(self.tabs[2], text='Configurator', variable=bool_var, onvalue=True, offvalue=False)
        cb.grid(row=7, column=1, sticky=W, padx=self.pad_x)
        self.data_vars.update({'Configurator': bool_var})

        bool_var = BooleanVar()
        bool_var.set(self.settings['log'].get())
        cb = Checkbutton(self.tabs[2], text='Quote Log', variable=bool_var, onvalue=True, offvalue=False)
        cb.grid(row=8, column=1, sticky=NW, padx=self.pad_x)
        self.data_vars.update({'Quote Log': bool_var})

    def __error_handler(self) -> bool:
        """
        Handle and display errors for missing required input fields.
        :return: flag indicating error
        """
        req_vars = dict(itertools.islice(self.data_vars.items(), 2))
        req_vars.update(dict(itertools.islice(self.data_vars.items(), 8, len(self.data_vars) - 2)))
        req_vars.pop('Project Scope')
        for key in req_vars:
            req_var = req_vars[key]
            if isinstance(req_var, StringVar) and not req_var.get() or req_var.get() == 'Select...':
                utils.messagebox.showerror('Input Error', f"Enter value for '{key}'.")
                return True
        return False

    def start_progress(self):
        """
        Start the progress bar and status window.
        """
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
        pb_button.grid(row=5, column=0, columnspan=3, sticky=W, padx=20, ipadx=5)
        pb_button = Button(self.pb_window, text="Pause", command=self.pause_execution)
        pb_button.grid(row=5, column=0, columnspan=3, sticky=W, padx=(135, 0), ipadx=5)
        pb_button = Button(self.pb_window, text="Resume", command=self.resume_execution)
        pb_button.grid(row=5, column=0, columnspan=3, sticky=W, padx=(250, 0), ipadx=5)

    def stop_progress(self):
        """
        Stop the progress bar and closes the status window.
        """
        self.pb.grid_forget()
        self.pb.destroy()
        self.pb_window.destroy()

    def update_progress(self, status: str, inc: float):
        """
        Update the progress bar and status.

        :param status: status message to display
        :param inc: amount by which to increment the progress
        """
        self.pb_status.set(status + '...')
        self.pb['value'] += inc

    def save_login(self):
        """
        Save the login information to the default CSV file.
        """
        utils.save(self.data_vars, self.default_csv_path / 'login_info.csv', end=8)

    def save_login_as(self):
        """
        Save the login information to a new CSV file.
        """
        utils.save_as(self.data_vars, 'login_data.csv', end=8)

    def load_login(self):
        """
        Load the login information from the default CSV file.
        """
        try:
            utils.load(self.data_vars, self.default_csv_path / 'login_info.csv')
        except FileNotFoundError:
            utils.messagebox.showerror('File Not Found', 'No saved login information '
                                                         'found from the previous run.')

    def load_login_as(self):
        """
        Load the login information from a different CSV file.
        """
        utils.load_as(self.data_vars)

    def save_inputs(self):
        """
        Save the input data to the default CSV file.
        """
        utils.save(self.data_vars, self.default_csv_path / 'last_inputs.csv', start=8, end=len(self.data_vars))

    def save_inputs_as(self):
        """
        Save the input data to a new CSV file.
        """
        utils.save_as(self.data_vars, 'input_data.csv', start=8, end=len(self.data_vars))

    def load_inputs(self):
        """
        Load the input data from the default CSV file.
        """
        utils.load(self.data_vars, self.default_csv_path / 'last_inputs.csv')

    def load_inputs_as(self):
        """
        Load the input data from a different CSV file.
        """
        utils.load_as(self.data_vars)

    def clear_inputs(self):
        """
        Clear all the input fields.
        """
        for key in self.data_vars:
            var = self.data_vars[key]
            if isinstance(var, StringVar):
                var.set('')
            elif isinstance(var, BooleanVar):
                var.set(False)

    def get_data(self) -> dict:
        """
        Retrieve the input data from the fields.

        :return: a collection of data variables
        """
        data_dict = {}
        for key in self.data_vars:
            data_dict.update({key: self.data_vars[key].get()})
        return data_dict

    @staticmethod
    def show_success_msg():
        """
        Display a success message.
        """
        utils.show_info_msg('Success', "Process completed successfully!")

    @staticmethod
    def show_failure_msg():
        """
        Display a failure message.
        """
        utils.show_error_msg("Error", "Unexpected error occurred. Please check the browser for more info.")

    @staticmethod
    def add_browse_button(frame, row: int, col: int, pad_x: int, command, arg):
        """
        Add a browse button to select a directory.

        :param frame: frame object to put the button in
        :param row: grid row to place the button in
        :param col: grid column to place the button in
        :param pad_x: horizontal padding
        :param command: function to run on button click
        :param arg: argument for the function
        """
        button = Button(frame, text="Browse", command=lambda: command(arg))
        button.grid(row=row, column=col, sticky=W, padx=pad_x, pady=15)

    def run_controller(self):
        """
        Execute the main logic of the application in a separate thread.
        """
        if self.__error_handler():
            return
        execution_thread = Thread(target=run_middleware, args=(self,))
        execution_thread.daemon = True
        execution_thread.start()

    def view_settings(self):
        """
        Display the application settings window.
        """
        if self.settings_window and Toplevel.winfo_exists(self.settings_window):
            settings_window = self.settings_window
            settings_window.focus()
        else:
            settings_window = utils.open_new_window(self, 'Settings', 500, 545, 14, 2)

        heading = Label(settings_window, text='Settings', font=("Tahoma", 12))
        heading.grid(row=0, column=0, columnspan=2, sticky=W, pady=20, padx=self.pad_x)

        lb = Label(settings_window, text='Execution Delay (s): ')
        lb.grid(row=1, column=0, sticky=NW, padx=self.pad_x)
        en = Entry(settings_window, textvariable=self.settings['delay'])
        en.grid(row=1, column=1, sticky='ew', padx=(0, self.pad_x))

        lb = Label(settings_window, text='Default CSV path: ')
        lb.grid(row=3, column=0, sticky=NW, padx=self.pad_x)
        en = Entry(settings_window, textvariable=self.settings['csv-path'])
        en.grid(row=3, column=1, sticky='ew', padx=(0, self.pad_x))

        self.add_browse_button(settings_window, 4, 1, 0, utils.browse_directory, self.settings['csv-path'])

        lb = Label(settings_window, text='Default Checkboxes:')
        lb.grid(row=6, column=0, sticky=NW, padx=self.pad_x)
        cb = Checkbutton(settings_window, text='Configurator', variable=self.settings['config'], onvalue=True, offvalue=False)
        cb.grid(row=6, column=1, sticky=W)
        cb = Checkbutton(settings_window, text='Quote Log', variable=self.settings['log'], onvalue=True, offvalue=False)
        cb.grid(row=7, column=1, sticky=W)

        lb = Label(settings_window, text='Default Entries:')
        lb.grid(row=9, column=0, sticky=NW, padx=self.pad_x)

        lb = Label(settings_window, text='Status:')
        lb.grid(row=9, column=1, sticky=NW)
        en = Entry(settings_window, textvariable=self.settings['status'])
        en.grid(row=10, column=1, sticky='ew', padx=(0, self.pad_x))

        lb = Label(settings_window, text='Memo:')
        lb.grid(row=11, column=1, sticky=NW)
        en = Entry(settings_window, textvariable=self.settings['memo'])
        en.grid(row=12, column=1, sticky='ew', padx=(0, self.pad_x))

        save_btn = Button(settings_window, text="Save", command=lambda: self.save_settings(settings_window))
        save_btn.grid(row=14, columnspan=2, sticky='ew', padx=self.pad_x * 4)

        self.settings_window = settings_window

    def save_settings(self, settings_window):
        """
        Save the settings in the settings window.

        :param settings_window: window displaying settings
        """
        utils.save(self.settings, Path(self.data_path, 'settings.csv'))
        settings_window.destroy()

    @staticmethod
    def open_chromedriver():
        options = [f'user-data-dir={CHROME_USER_PROFILE}', 'start-maximized']
        controller = WebController([NETSUITE_URL], options=options, detach=True)

    @staticmethod
    def open_github():
        webbrowser.open(r"https://github.com/primeeng-adil/netsuite-takeoff-integration")

    @staticmethod
    def check_updates():
        webbrowser.open(r"https://github.com/primeeng-adil/netsuite-takeoff-integration/releases")

    def empty(self):
        pass

    def pause_execution(self):
        self.pause = True

    def resume_execution(self):
        self.pause = False
