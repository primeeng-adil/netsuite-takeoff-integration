import ctypes
import PIL.Image
from PIL import ImageTk
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
from tkinter import messagebox
from pathlib import Path
from ttkwidgets.autocomplete import AutocompleteCombobox
from utility import csv_handler
from threading import Thread
from middleware.middleware import run_middleware
from .dropdowns import update

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class App(Tk):

    def __init__(self):
        super().__init__()

        self.pb = None
        self.pb_window = None
        self.tabs = []
        self.tab_grid = []
        self.data_vars = []
        self.elements = []
        self.pad_x = 40

        self.__adjust_window()
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

    def __adjust_window(self):
        root_width = 850
        root_height = 725
        position_right = int((self.winfo_screenwidth() - root_width) / 2)
        position_down = int((self.winfo_screenheight() - root_height) / 2 - root_height / 6)

        self.geometry("{}x{}+{}+{}".format(root_width, root_height, position_right, position_down))
        self.resizable(height=True, width=True)
        self.title("NetSuite Proposal Generator - v1.0.1")

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
            ['Update Dropdowns', self.update_dropdowns],
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

        self.fill_menu_cascade(file, file_cmd_funcs, [3, 7, 8, 9])
        self.fill_menu_cascade(edit, edit_cmd_funcs, [])
        self.fill_menu_cascade(help_, help_cmd_funcs, [1])
        self.config(menu=menu_bar)

    @staticmethod
    def fill_menu_cascade(cascade, cmd_funcs, separators):
        for i in range(len(cmd_funcs)):
            cascade.add_command(label=cmd_funcs[i][0], command=cmd_funcs[i][1])
            if i in separators:
                cascade.add_separator()

    def __create_tabs(self, count, titles):
        tab_controller = Notebook(self)
        for i in range(count):
            self.tabs.append(Frame(tab_controller))
            tab_controller.add(self.tabs[i], text=titles[i])
        tab_controller.pack(expand=1, fill='both', padx=20, pady=(10, 0))

    @staticmethod
    def __create_grid(master, rows, cols):
        for col in range(cols):
            master.columnconfigure(col, weight=1, uniform='fred')
        for row in range(rows):
            master.rowconfigure(row, minsize=30)

    def __design_tabs(self):
        self.tab_grid.append([12, 2])
        self.tab_grid.append([12, 2])
        self.tab_grid.append([12, 2])

        self.__create_grid(self.tabs[0], *self.tab_grid[0])
        self.__create_grid(self.tabs[1], *self.tab_grid[1])
        self.__create_grid(self.tabs[2], *self.tab_grid[2])

        self.__add_elements_login()
        self.__add_elements_proposal()
        self.__add_elements_project()

    def __add_heading(self, text, tab, row):
        heading = Label(self.tabs[tab], text=text, font=("Tahoma", 12))
        heading.grid(row=row, column=0, columnspan=2, sticky=W, pady=20, padx=self.pad_x)

    def __add_fields(self, labels, tab, row, col):
        for i in range(0, 2 * len(labels), 2):
            field = int(i / 2)
            label = Label(self.tabs[tab], text=labels[field][1])
            label.grid(row=row + i, column=col, sticky=W, padx=self.pad_x)
            if labels[field][0] == 'combo':
                self.__add_dropdown(tab, row + i + 1, col, labels[field][2])
            else:
                self.__add__entry(tab, row + i + 1, col)

    def __add__entry(self, tab, row, col):
        str_var = StringVar()
        field = Entry(self.tabs[tab], textvariable=str_var)
        field.grid(row=row, column=col, sticky='ew', padx=self.pad_x)
        self.data_vars.append(str_var)
        self.elements.append(field)

    def __add_dropdown(self, tab, row, col, options):
        str_var = StringVar()
        str_var.set('Select...')
        dropdown = AutocompleteCombobox(self.tabs[tab], textvariable=str_var, completevalues=options)
        dropdown.grid(row=row, column=col, sticky='ew', padx=self.pad_x)
        dropdown.bind('<FocusIn>', self.clear_box)
        dropdown.bind('<FocusOut>', self.reset_box)
        self.data_vars.append(str_var)
        self.elements.append(dropdown)

    def open_new_window(self, title, width, height, rows, columns):
        window = Toplevel(self)
        for cols in range(columns):
            window.columnconfigure(cols, weight=1)
        for rows in range(rows):
            window.rowconfigure(rows, weight=1)
        window.title(title)
        window.iconbitmap(Path('./data/icon.ico'))
        position_right = int((self.winfo_screenwidth() - width) / 2)
        position_down = int((self.winfo_screenheight() - height) / 2 - height / 6)
        window.geometry("{}x{}+{}+{}".format(width, height, position_right, position_down))
        window.focus_set()
        return window

    def start_progress(self):
        pb_status = StringVar()
        self.data_vars.append(pb_status)

        self.pb_window = self.open_new_window("Progress", 400, 300, 6, 3)
        self.pb = Progressbar(self.pb_window, orient=HORIZONTAL, mode='determinate')
        self.pb.grid(row=2, column=0, columnspan=3, sticky=EW, padx=20)

        pb_status.set("Initializing...")
        status_label = Label(self.pb_window, textvariable=pb_status)
        status_label.grid(row=1, column=0, columnspan=3, sticky=W, padx=20)

        log = Listbox(self.pb_window, height=6, fg='orange')
        log.grid(column=0, columnspan=3, sticky=EW, padx=20)

        pb_button = Button(self.pb_window, text="End", command=self.pb_window.destroy)
        pb_button.grid(row=4, column=0, columnspan=3, sticky=W, padx=20, ipadx=5)
        pb_button = Button(self.pb_window, text="Pause", command=self.pb_window.destroy)
        pb_button.grid(row=4, column=0, columnspan=3, sticky=W, padx=(135, 0), ipadx=5)

    def stop_progress(self):
        self.pb.grid_forget()
        self.pb.destroy()
        self.pb_window.destroy()

    def update_progress(self, status, inc):
        self.data_vars[-1].set(status + '...')
        self.pb['value'] += inc

    @staticmethod
    def show_success_msg():
        messagebox.showinfo('Success', "Process completed successfully!")

    def __add_elements_login(self):
        self.__add_heading('Login Info', 0, 0)
        self.__add_fields([
            ['entry', 'Username:'],
            ['entry', 'Password:']
        ], 0, 1, 0)
        self.__add_heading('Security Questions', 0, 5)
        self.__add_fields([
            ['entry', 'Question 1:'],
            ['entry', 'Question 2:'],
            ['entry', 'Question 3:']
        ], 0, 6, 0)
        self.__add_fields([
            ['entry', 'Answer 1:'],
            ['entry', 'Answer 2:'],
            ['entry', 'Answer 3:']
        ], 0, 6, 1)

    def __add_elements_proposal(self):
        departments = csv_handler.read_csv(Path('./data/dropdowns/Departments.csv'))
        classes = csv_handler.read_csv(Path('./data/dropdowns/Classes.csv'))
        reps = csv_handler.read_csv(Path('./data/dropdowns/ProposalSalesReps.csv'))
        customers = csv_handler.read_csv(Path('./data/dropdowns/Customers.csv'))
        items = csv_handler.read_csv(Path('./data/dropdowns/Items.csv'))

        status = ['Initial Review', 'Submitted', 'Closed Won', 'Closed Lost']
        self.__add_heading('Proposal Info', 1, 0)
        self.__add_fields([
            ['combo', 'Customer:', customers],
            ['combo', 'Status:', status],
            ['entry', 'Memo:'],
            ['combo', 'Proposal Sales Rep:', reps]
        ], 1, 1, 0)
        self.__add_fields([
            ['combo', 'Department:', departments],
            ['combo', 'Class:', classes],
            ['combo', 'Item:', items]
        ], 1, 1, 1)

    def __add_elements_project(self):
        templates = csv_handler.read_csv(Path('./data/dropdowns/ProjectTemplates.csv'))
        types = csv_handler.read_csv(Path('./data/dropdowns/ProjectTypes.csv'))
        billing = ['Charge-Based', 'Fixed Bid, Interval', 'Fixed Bid, Milestone', 'Time and Materials']
        self.__add_heading('Project Info', 2, 0)
        self.__add_fields([
            ['entry', 'City:'],
            ['entry', 'Address:'],
            ['entry', 'Facility:'],
            ['entry', 'Customer:']
        ], 2, 1, 0)
        self.__add_fields([
            ['combo', 'Project Template:', templates],
            ['combo', 'Project Type:', types],
            ['combo', 'Billing Type:', billing],
            ['entry', 'SharePoint Path:']
        ], 2, 1, 1)

    def __add_cmd_buttons(self):
        run_btn = Button(self, text="Run", command=self.run_controller)
        run_btn.pack(side=LEFT, padx=(self.pad_x + 20, 0), pady=40, ipadx=30)
        exit_btn = Button(self, text="Exit", command=self.destroy)
        exit_btn.pack(side=RIGHT, padx=(0, self.pad_x + 20), pady=40, ipadx=30)

    def create_line(self, tab, row):
        line = Canvas(self.tabs[tab], height=4, width=750)
        line.create_line(0, 2, 750, 2)
        line.grid(row=row, column=0, columnspan=4, sticky=NW, padx=self.pad_x, pady=(5, 0))

    def __customize(self):
        self.elements[1].config(show="*")
        self.data_vars[9].set('Initial Review')
        self.data_vars[10].set('2.0.0 – base bid')
        self.data_vars[18] = self.data_vars[8]
        self.elements[18].config(textvariable=self.data_vars[18])
        self.elements[18].config(state='disabled')
        self.elements[22].insert(0, '/Shared Documents/Quotes/')
        for i in range(5, 8):
            self.elements[i].config(show="*")

    def get_data(self):
        return [var.get() for var in self.data_vars]

    @staticmethod
    def clear_box(e):
        e.widget.select_range(0, 'end')
        if e.widget.get() == 'Select...':
            e.widget.set('')

    @staticmethod
    def reset_box(e):
        if not e.widget.get():
            e.widget.set('Select...')

    def save(self, path, start=0, end=0):
        data = [[self.data_vars[i].get()] for i in range(start, end)]
        data.insert(0, ['Name'])
        csv_handler.write_csv(path, data)

    def save_as(self, default_name, start=0, end=0):
        file_type = [('CSV UTF-8 (Comma delimited)', '*.csv')]
        path = tkinter.filedialog.asksaveasfilename(
            filetypes=file_type,
            initialfile=default_name
        )
        try:
            self.save(path, start, end)
        except FileNotFoundError:
            return

    def load(self, path, start=0):
        data = csv_handler.read_csv(path)
        for i in range(len(data)):
            self.data_vars[i + start].set(data[i])

    def load_as(self, start=0):
        path = tkinter.filedialog.askopenfile()
        try:
            self.load(path.name, start=start)
        except (FileNotFoundError, AttributeError):
            return

    def save_login(self):
        self.save(Path('./data/inputs/LoginInfo.csv'), end=8)

    def save_login_as(self):
        self.save_as('login_data', end=8)

    def load_login(self):
        try:
            self.load(Path('./data/inputs/LoginInfo.csv'))
        except FileNotFoundError:
            messagebox.showerror('File Not Found', 'No saved login information found from the previous run.')

    def load_login_as(self):
        self.load_as()

    def save_inputs(self):
        self.save(Path('./data/inputs/LastInputs.csv'), start=8, end=len(self.data_vars))

    def save_inputs_as(self):
        self.save_as('input_data', start=8, end=len(self.data_vars))

    def load_inputs(self):
        try:
            self.load(Path('./data/inputs/LastInputs.csv'), start=8)
        except FileNotFoundError:
            messagebox.showerror('File Not Found', 'No saved inputs found from the previous run.')

    def load_inputs_as(self):
        self.load_as(start=8)

    def __error_handler(self):
        labels = [
            'Username', 'Password',
            'Question 1', 'Question 2',
            'Question 3', 'Answer 1',
            'Answer 2', 'Answer 3',
            'Customer', 'Status',
            'Memo', 'Proposal Sales Rep',
            'Department', 'Class',
            'Item', 'City',
            'Address', 'Facility',
            'Customer', 'Project Template',
            'Project Type', 'Billing Type',
            'SharePoint Path'
        ]
        for var in self.data_vars:
            if not var.get() or var.get() == 'Select...':
                index = self.data_vars.index(var)
                messagebox.showerror('Input Error', f"Enter value for '{labels[index]}'.")
                return True
        return False

    def clear_inputs(self):
        for var in self.data_vars:
            var.set('')

    def run_controller(self):
        if self.__error_handler():
            return
        execution_thread = Thread(target=run_middleware, args=(self,))
        execution_thread.daemon = True
        execution_thread.start()

    def update_dropdowns(self):
        update_thread = Thread(target=update, args=(self.data_vars[0].get(), self.data_vars[1].get(),))
        update_thread.daemon = True
        update_thread.start()

    def view_settings(self):
        pass

    def empty(self):
        pass
