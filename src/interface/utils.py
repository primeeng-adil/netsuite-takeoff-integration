from pathlib import Path
from tkinter import END, W, NW
from tkinter import messagebox, filedialog, StringVar, Toplevel, Canvas
from tkinter.ttk import Label, Entry
from ttkwidgets.autocomplete import AutocompleteCombobox
from src.utility import csv_handler


def adjust_window(app, title):
    root_width = 850
    root_height = 725
    position_right = int((app.winfo_screenwidth() - root_width) / 2)
    position_down = int((app.winfo_screenheight() - root_height) / 2 - root_height / 6)

    app.geometry("{}x{}+{}+{}".format(root_width, root_height, position_right, position_down))
    app.resizable(height=True, width=True)
    app.title(title)


def open_new_window(app, title, width, height, rows, columns):
    window = Toplevel(app)
    for cols in range(columns):
        window.columnconfigure(cols, weight=1, uniform='fred')
    for rows in range(rows):
        window.rowconfigure(rows, weight=1)
    window.title(title)
    window.iconbitmap(Path('./data/icon.ico'))
    position_right = int((app.winfo_screenwidth() - width) / 2)
    position_down = int((app.winfo_screenheight() - height) / 2 - height / 6)
    window.geometry("{}x{}+{}+{}".format(width, height, position_right, position_down))
    window.focus_set()
    return window


def fill_menu_cascade(cascade, cmd_funcs, separators):
    for i in range(len(cmd_funcs)):
        cascade.add_command(label=cmd_funcs[i][0], command=cmd_funcs[i][1])
        if i in separators:
            cascade.add_separator()


def create_grid(master, rows, cols):
    for col in range(cols):
        master.columnconfigure(col, weight=1, uniform='fred')
    for row in range(rows):
        master.rowconfigure(row, minsize=30)


def add_fields(app, labels, tab, row, col):
    for i in range(0, 2 * len(labels), 2):
        field = int(i / 2)
        label = Label(app.tabs[tab], text=labels[field][1])
        label.grid(row=row + i, column=col, sticky=W, padx=app.pad_x)
        if labels[field][0] == 'combo':
            add_dropdown(app, tab, row + i + 1, col, labels[field][2])
        elif labels[field][0] == 'entry':
            add_entry(app, tab, row + i + 1, col)


def add_entry(app, tab, row, col):
    str_var = StringVar()
    entry = Entry(app.tabs[tab], textvariable=str_var)
    entry.grid(row=row, column=col, sticky='ew', padx=app.pad_x)
    bind_events_to_entry(entry)
    app.data_vars.append(str_var)
    app.elements.append(entry)


def add_dropdown(app, tab, row, col, options):
    str_var = StringVar()
    str_var.set('Select...')
    dropdown = AutocompleteCombobox(app.tabs[tab], textvariable=str_var, completevalues=options)
    dropdown.grid(row=row, column=col, sticky='ew', padx=app.pad_x)
    dropdown.bind('<FocusIn>', clear_box)
    dropdown.bind('<FocusOut>', reset_box)
    app.data_vars.append(str_var)
    app.elements.append(dropdown)


def bind_events_to_entry(entry):
    entry.bind('<FocusIn>', lambda e: entry.select_range(0, END), add='+')
    entry.bind('<FocusIn>', lambda e: entry.xview(END), add='+')
    entry.bind('<FocusIn>', lambda e: entry.icursor(END), add='+')
    entry.bind('<FocusOut>', lambda e: entry.xview(0), add='+')


def add_heading(app, text, tab, row):
    heading = Label(app.tabs[tab], text=text, font=("Tahoma", 12))
    heading.grid(row=row, column=0, columnspan=2, sticky=W, pady=20, padx=app.pad_x)


def create_line(app, tab, row):
    line = Canvas(app.tabs[tab], height=4, width=750)
    line.create_line(0, 2, 750, 2)
    line.grid(row=row, column=0, columnspan=4, sticky=NW, padx=app.pad_x, pady=(5, 0))


def show_success_msg():
    messagebox.showinfo('Success', "Process completed successfully!")


def browse_directory(str_var):
    str_var.set(filedialog.askdirectory())


def clear_box(e):
    e.widget.select_range(0, 'end')
    if e.widget.get() == 'Select...':
        e.widget.set('')


def reset_box(e):
    if not e.widget.get():
        e.widget.set('Select...')


def save(app, path, start=0, end=0):
    path.parent.mkdir(exist_ok=True, parents=True)
    data = [[app.data_vars[i].get()] for i in range(start, end)]
    csv_handler.write_csv(path, data)


def save_as(app, default_name, start=0, end=0):
    file_type = [('CSV UTF-8 (Comma delimited)', '*.csv')]
    path = Path(filedialog.asksaveasfilename(
        filetypes=file_type,
        initialfile=default_name
    ))
    try:
        save(app, path, start, end)
    except FileNotFoundError:
        return


def load(app, path, start=0):
    data = csv_handler.read_csv(path)
    for i in range(len(data)):
        app.data_vars[i + start].set(data[i])


def load_as(app, start=0):
    path = filedialog.askopenfile()
    try:
        load(app, path.name, start=start)
    except (FileNotFoundError, AttributeError):
        return
