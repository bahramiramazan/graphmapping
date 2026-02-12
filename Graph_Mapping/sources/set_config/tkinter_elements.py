from tkinter import Tk, Label, Checkbutton, BooleanVar, Entry, Radiobutton, Button
from tkinter.ttk import Combobox


def create_window(title, width, height):
    win = Tk()
    win.title(title)

    x_left = int(win.winfo_screenwidth() / 2 - width / 2)
    y_top = int(win.winfo_screenheight() / 2 - height / 2)
    win.geometry("{}x{}+{}+{}".format(width, height, x_left, y_top))
    win.resizable(0, 0)

    win.grid_rowconfigure(list(range(int(height / 20))), weight=1)
    win.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
    return win


def insert_text(text, column, row, win, size=10, columnspan=2, sticky=""):
    lbl = Label(win, text=text, font=("Arial Bold", size), justify="center")
    lbl.grid(column=column, row=row, columnspan=columnspan, sticky=sticky, padx=30)
    return lbl


def insert_checkbutton(text, column, row, win, size=10, columnspan=2, sticky="", command=None):
    chb_state = BooleanVar()
    chb_state.set(False)  # set check state
    chb = Checkbutton(win, text=text, var=chb_state, font=("Arial Bold", size), command=command)
    chb.grid(column=column, row=row, columnspan=columnspan, sticky=sticky, padx=30)
    return chb, chb_state


def insert_entry(column, row, width, win, columnspan=2, sticky="", textvariable=None):
    txt = Entry(win, width=width, justify="center", textvariable=textvariable)
    txt.grid(column=column, row=row, columnspan=columnspan, sticky=sticky, padx=30)
    return txt


def insert_combobox(column, row, values, win, size=10, columnspan=2, sticky=""):
    combo = Combobox(win, justify="center", font=("Arial Bold", size), state="readonly")
    combo['values'] = values
    # combo.current(0)  # set the selected item
    combo.grid(column=column, row=row, columnspan=columnspan, sticky=sticky, padx=30)
    return combo


def insert_radiobutton(text, column, row, selector, value, command, win, size=10, columnspan=2, sticky=""):
    rad = Radiobutton(win, text=text, value=value, variable=selector, font=("Arial Bold", size), command=command)
    rad.grid(column=column, row=row, columnspan=columnspan, sticky=sticky, padx=30)
    return rad


def insert_button(text, column, row, command, win, size=10, columnspan=2, sticky=""):
    button = Button(win, text=text, command=command, font=("Arial Bold", size))
    button.grid(column=column, row=row, columnspan=columnspan, sticky=sticky)
    return button
