import itertools
from pathlib import Path
from tkinter import END, W, NW
from tkinter import messagebox, filedialog, StringVar, BooleanVar, Toplevel, Menu, Tk, Event
from tkinter.ttk import Label, Entry, Checkbutton
from utility import csv_handler
from ttkwidgets.autocomplete import AutocompleteCombobox


def adjust_window(app, title: str, width: int, height: int):
    """
    Adjust the root window layout.

    :param app: current app object interacting with the user
    :param title: title to be displayed on the root window
    :param width: width of the window
    :param height: height of the window
    """
    position_right = int((app.winfo_screenwidth() - width) / 2)
    position_down = int((app.winfo_screenheight() - height) / 2 - height / 6)

    app.geometry("{}x{}+{}+{}".format(width, height, position_right, position_down))
    app.resizable(height=True, width=True)
    app.title(title)


def open_new_window(app, title: str, width: int, height: int, rows: int, columns: int) -> Toplevel:
    """
    Create and return a new tkinter window object.

    :param app: current app object interacting with the user
    :param title: title to be displayed on the window
    :param width: width of the window
    :param height: height of the window
    :param rows: number of grid rows to be created in the window
    :param columns: number of grid columns to be created in the window
    :return: created window
    """
    window = Toplevel(app)
    for cols in range(columns):
        window.columnconfigure(cols, weight=1, uniform='fred')
    for rows in range(rows):
        window.rowconfigure(rows, minsize=30)
    window.title(title)
    window.iconbitmap(Path(app.data_path, 'icon.ico'))
    position_right = int((app.winfo_screenwidth() - width) / 2)
    position_down = int((app.winfo_screenheight() - height) / 2 - height / 6)
    window.geometry("{}x{}+{}+{}".format(width, height, position_right, position_down))
    window.focus_set()
    return window


def fill_menu_cascade(menu: Menu, cmd_funcs: list, separators: list):
    """
    Add commands to the given menu object.

    :param menu: an instance of menu object
    :param cmd_funcs: functions to be added to each menu command
    :param separators: indices of menu separators
    """
    for i in range(len(cmd_funcs)):
        menu.add_command(label=cmd_funcs[i][0], command=cmd_funcs[i][1])
        if i in separators:
            menu.add_separator()


def create_grid(master: Tk, rows: int, cols: int):
    """
    Create a grid in the given window object.

    :param master: window to create the grid in
    :param rows: number of rows required in the grid
    :param cols: number of columns required in the grid
    """
    for col in range(cols):
        master.columnconfigure(col, weight=1, uniform='fred')
    for row in range(rows):
        master.rowconfigure(row, minsize=30)


def add_fields(app, labels: list, tab: int, row: int, col: int):
    """
    Add input fields in the given tab.

    :param app: current app object interacting with the user
    :param labels: labels to be added to the corresponding fields
    :param tab: index of the tab required
    :param row: index of the row where the fields are to be added
    :param col: index of the column where the fields are to be added
    """
    for i in range(0, 2 * len(labels), 2):
        field = int(i / 2)
        if labels[field][0] == 'checkbox':
            add_checkbox(app, tab, row + i + 1, col, labels[field][1])
            continue
        label = Label(app.tabs[tab], text=labels[field][1])
        label.grid(row=row + i, column=col, sticky=W, padx=app.pad_x)
        if labels[field][0] == 'combo':
            add_dropdown(app, tab, row + i + 1, col, labels[field][1][:-1], labels[field][2])
        elif labels[field][0] == 'entry':
            add_entry(app, tab, row + i + 1, col, labels[field][1][:-1])


def add_entry(app, tab: int, row: int, col: int, label: str):
    """
    Add a tkinter entry object in the given tab.

    :param label:
    :param app: current app object interacting with the user
    :param tab: index of the tab required
    :param row: index of the row where the entry is to be added
    :param col: index of the column where the entry is to be added
    """
    str_var = StringVar()
    entry = Entry(app.tabs[tab], textvariable=str_var)
    entry.grid(row=row, column=col, sticky='ew', padx=app.pad_x)
    bind_events_to_entry(entry)
    app.data_vars.update({label: str_var})
    app.elements.append(entry)


def add_dropdown(app, tab: int, row: int, col: int, label: str, options: list):
    """
    Add a tkinter dropdown object in the given tab.

    :param label:
    :param app: current app object interacting with the user
    :param tab: index of the tab required
    :param row: index of the row where the dropdown is to be added
    :param col: index of the column where the dropdown is to be added
    :param options: values of the dropdown
    """
    str_var = StringVar()
    str_var.set('Select...')
    dropdown = AutocompleteCombobox(app.tabs[tab], textvariable=str_var, completevalues=options)
    dropdown.grid(row=row, column=col, sticky='ew', padx=app.pad_x)
    dropdown.bind('<FocusIn>', clear_widget)
    dropdown.bind('<FocusOut>', reset_widget)
    app.data_vars.update({label: str_var})
    app.elements.append(dropdown)


def add_checkbox(app, tab: int, row: int, col: int, label: str):
    """
    Add a tkinter checkbox object in the given tab.

    :param label:
    :param app: current app object interacting with the user
    :param tab: index of the tab required
    :param row: index of the row where the entry is to be added
    :param col: index of the column where the entry is to be added
    """

    bool_var = BooleanVar()
    checkbox = Checkbutton(app.tabs[tab], text=label, variable=bool_var, onvalue=True, offvalue=False)
    checkbox.grid(row=row, column=col, sticky=NW, padx=app.pad_x)
    app.data_vars.update({label: bool_var})
    app.elements.append(checkbox)


def bind_events_to_entry(entry: Entry):
    """
    Bind tkinter events to the given entry.

    :param entry: tkinter entry object
    """
    entry.bind('<FocusIn>', lambda e: entry.select_range(0, END), add='+')
    entry.bind('<FocusIn>', lambda e: entry.xview(END), add='+')
    entry.bind('<FocusIn>', lambda e: entry.icursor(END), add='+')
    entry.bind('<FocusOut>', lambda e: entry.xview(0), add='+')


def add_heading(app, text: str, tab: int, row: int):
    """
    Add heading text in the given tab.

    :param app: current app object interacting with the user
    :param text: display text of the heading
    :param tab: index of the tab required
    :param row: index of the row where the heading is to be added
    """
    heading = Label(app.tabs[tab], text=text, font=("Tahoma", 12))
    heading.grid(row=row, column=0, columnspan=2, sticky=W, pady=20, padx=app.pad_x)


def save(data_vars: dict, path: Path, start: int = 0, end: int = 0):
    """
    Save the passed data objects to a csv file at the given path.

    :param data_vars: data objects
    :param path: path of the csv file
    :param start: index defining the start position of data objects
    :param end: index defining the end position of the data objects
    """
    if not end:
        end = len(data_vars)
    path.parent.mkdir(exist_ok=True, parents=True)
    filtered_vars = dict(itertools.islice(data_vars.items(), start, end))
    data = [[key, data_vars[key].get()] for key in filtered_vars]
    csv_handler.write_csv(path, data)


def save_as(data_vars: dict, default_name: str, start: int = 0, end: int = 0):
    """
    Save the passed data objects to a csv file at a user specified path.

    :param data_vars: data objects
    :param default_name: default name of the csv file to be created
    :param start: index defining the start position of the data objects
    :param end: index defining the end position of the data objects
    """
    file_type = [('CSV UTF-8 (Comma delimited)', '*.csv')]
    browse_path = filedialog.asksaveasfilename(
        filetypes=file_type,
        initialfile=default_name
    )
    if browse_path:
        save(data_vars, Path(browse_path), start, end)


def load(data_vars: dict, path: Path):
    """
    Load the passed data objects from a csv file at the given path.

    :param data_vars: data objects
    :param path: path of the csv file
    """
    try:
        data = csv_handler.read_csv(path)
        for row in data:
            data_vars[row[0]].set(row[1])
    except (FileNotFoundError, AttributeError):
        pass
    except UnicodeDecodeError:
        messagebox.showerror('Unsupported File Type', f'Error: file type {path.suffix} is not supported.')


def load_as(data_vars: dict):
    """
    Load the passed data objects from a csv file at a user specified browse_path.

    :param data_vars: data objects
    """
    browse_path = filedialog.askopenfile()
    if browse_path:
        load(data_vars, Path(browse_path.name))


def show_info_msg(title: str, msg: str):
    """
    Show a success message box.

    :param title: title of the messagebox
    :param msg: message shown in the messagebox
    """
    messagebox.showinfo(title, msg)


def show_error_msg(title: str, msg: str):
    """
    Show an error message box.

    :param title: title of the messagebox
    :param msg: message shown in the messagebox
    """
    messagebox.showerror(title, msg)


def browse_directory(str_var: StringVar):
    """
    Open the browse directory window.

    :param str_var: variable to store the path of the selected directory
    """
    str_var.set(filedialog.askdirectory())


def clear_widget(e: Event):
    """
    Clear the current widget related to the event object.

    :param e: tkinter event object
    """
    e.widget.select_range(0, 'end')
    if e.widget.get() == 'Select...':
        e.widget.set('')


def reset_widget(e: Event):
    """
    Reset the current widget related to the event object.

    :param e: tkinter event object
    """
    if not e.widget.get():
        e.widget.set('Select...')
