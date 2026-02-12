from tkinter import colorchooser


def show_on_off(elements, checkbutton_var, states):
    if checkbutton_var.get() == -1:
        state = "disable"
    else:
        state = states[checkbutton_var.get()]
    for elem in elements:
        elem.configure(state=state)


def change_button_color(button, color_code):
    button['background'] = color_code
    if color_code != "SystemButtonFace":
        color_code = tuple(int(color_code[i:i + 2], 16) for i in (1, 3, 5))
        if sum(color_code) < 100:
            button['foreground'] = 'white'
        else:
            button['foreground'] = 'black'


def choose_button_color(button, title):
    color_code = colorchooser.askcolor(title=title)
    change_button_color(button, color_code[1])
    return color_code[1]

