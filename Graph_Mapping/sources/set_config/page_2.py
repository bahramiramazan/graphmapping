from tkinter.ttk import Separator
from sources.set_config.tkinter_elements import *
from sources.set_config.utils import *
from sources.set_config.alerts import *


def page_2(info):
    def choose_left_color():
        return choose_button_color(left_button_color, title="Choose left button color")

    def choose_right_color():
        return choose_button_color(right_button_color, title="Choose right button color")

    def show_one_target():
        elements = [right_button_color_text, right_button_color, click_show_time]
        show_on_off(elements, one_target_var, ["normal", "disable"])

    def show_number():
        elements = [trial_number_position_x_text, trial_number_position_x, trial_number_position_y_text,
                    trial_number_position_y, trial_number_position_text, trial_number_size_text, trial_number_size]
        show_on_off(elements, show_trial_number_var, ["disable", "normal"])

    def show_buttons():
        elements = [mouse_buttons_position_x_text, mouse_buttons_position_x, mouse_buttons_position_y_text,
                    mouse_buttons_position_y, mouse_buttons_position_text, mouse_buttons_size_text, mouse_buttons_size]
        show_on_off(elements, show_mouse_buttons_var, ["disable", "normal"])

    def show_clock():
        elements = [clock_time_text, clock_time, clock_position_text, clock_position_x, clock_position_x_text,
                    clock_position_y, clock_position_y_text, clock_size_text, clock_size]
        show_on_off(elements, show_clock_icon_var, ["disable", "normal"])

    def add_info_from_config():
        try:
            # Target
            one_target_var.set(info["one_target"])
            change_button_color(left_button_color, info["left_button_color"])
            change_button_color(right_button_color, info["right_button_color"])
            click_show_time_var.set(info["click_show_time"])
            # Trial time
            trial_time.insert(0, info["trial_time"])
            break_time.insert(0, info["break_time"])
            # Trial info
            #    trial number
            show_trial_number_var.set(info["show_trial_number"])
            if info["show_trial_number"]:
                trial_number_position_x.insert(0, info["trial_number_position_x"])
                trial_number_position_y.insert(0, info["trial_number_position_y"])
                trial_number_size.insert(0, info["trial_number_size"])
            #   mouse buttons
            show_mouse_buttons_var.set(info["show_mouse_buttons"])
            if info["show_mouse_buttons"]:
                mouse_buttons_position_x.insert(0, info["mouse_buttons_position_x"])
                mouse_buttons_position_y.insert(0, info["mouse_buttons_position_y"])
                mouse_buttons_size.insert(0, info["mouse_buttons_size"])
            #   clock
            show_clock_icon_var.set(info["show_clock_icon"])
            if info["show_clock_icon"]:
                clock_position_x.insert(0, info["clock_position_x"])
                clock_position_y.insert(0, info["clock_position_y"])
                clock_size.insert(0, info["clock_size"])
                clock_time.insert(0, info["clock_time"])
        except:
            messagebox.showerror(message="Can't load file with config")
            trial_time.focus_force()

    def alerts():
        global information
        # ------------------ Target ------------------ #
        if not try_button_color(left_button_color, orig_button_background, "left button"):
            return None
        if not one_target_var.get() and \
           not try_button_color(right_button_color, orig_button_background, "right button"):
            return None
        # ---------------- Trial time ---------------- #
        tr_time = try_convert_to_float(trial_time.get(), "Trial time")
        if not try_in_range(tr_time, "Trial time", v_min=0):
            return None
        br_time = try_convert_to_float(break_time.get(), "Break time")
        if not try_in_range(br_time, "Break time", v_min=0):
            return None
        # cl_show_time = try_convert_to_float(click_show_time.get(), "Show chose option")
        # if not try_in_range(cl_show_time, "Show chose option", v_min=0):
        #     return None
        # ---------------- Trial info ---------------- #
        # Trial number
        if show_trial_number_var.get():
            tr_number_position_x = try_convert_to_int(trial_number_position_x.get(), "Trial number x position")
            if tr_number_position_x is None:
                return None
            tr_number_position_y = try_convert_to_int(trial_number_position_y.get(), "Trial number y position")
            if tr_number_position_y is None:
                return None
            tr_number_size = try_convert_to_int(trial_number_size.get(), "Number size")
            if not try_in_range(tr_number_size, "Number size", v_min=0):
                return None
        else:
            tr_number_position_x = None
            tr_number_position_y = None
            tr_number_size = None

        # Show mouse buttons
        if show_mouse_buttons_var.get():
            mouse_position_x = try_convert_to_int(mouse_buttons_position_x.get(), "Mouse buttons x position")
            if mouse_position_x is None:
                return None
            mouse_position_y = try_convert_to_int(mouse_buttons_position_y.get(), "Mouse buttons y position")
            if mouse_position_y is None:
                return None
            mouse_size = try_convert_to_int(mouse_buttons_size.get(), "Mouse buttons size")
            if not try_in_range(mouse_size, "Mouse buttons size", v_min=0):
                return None
        else:
            mouse_position_x = None
            mouse_position_y = None
            mouse_size = None

        # Clock
        if show_clock_icon_var.get():
            cl_time = try_convert_to_float(clock_time.get(), "Clock time")
            if not try_in_range(cl_time, "Clock time", v_min=0):
                return None
            cl_position_x = try_convert_to_int(clock_position_x.get(), "Clock time x position")
            if cl_position_x is None:
                return None
            cl_position_y = try_convert_to_int(clock_position_y.get(), "Clock time y position")
            if cl_position_y is None:
                return None
            cl_size = try_convert_to_int(clock_size.get(), "Clock size")
            if not try_in_range(cl_size, "Clock size", v_min=0):
                return None
        else:
            cl_time = None
            cl_position_x = None
            cl_position_y = None
            cl_size = None

        information = {
            # Target
            "one_target": one_target_var.get(),
            "left_button_color": left_button_color['background'],
            "right_button_color": right_button_color['background'],
            "click_show_time": click_show_time_var.get(),
            # Trial time
            "trial_time": tr_time,
            "break_time": br_time,
            # Trial info
            #    trial number
            "show_trial_number": show_trial_number_var.get(),
            "trial_number_position_x": tr_number_position_x,
            "trial_number_position_y": tr_number_position_y,
            "trial_number_size": tr_number_size,
            #   mouse buttons
            "show_mouse_buttons": show_mouse_buttons_var.get(),
            "mouse_buttons_position_x": mouse_position_x,
            "mouse_buttons_position_y": mouse_position_y,
            "mouse_buttons_size": mouse_size,
            #   clock
            "show_clock_icon": show_clock_icon_var.get(),
            "clock_position_x": cl_position_x,
            "clock_position_y": cl_position_y,
            "clock_size": cl_size,
            "clock_time": cl_time
        }
        window.destroy()

    def go_back():
        global information
        window.destroy()
        information = "go_back"

    global information
    information = None

    window = create_window("Set config", 550, 680)

    # ------------------ Target ------------------ #
    insert_text(text="", column=5, row=0, size=1, win=window)
    insert_text(text="Targets", column=0, row=0, size=14, sticky="W", win=window)
    Separator(window, orient='horizontal').place(x=0, y=32, relwidth=1, height=2)

    _, one_target_var = insert_checkbutton(text="Use only one target", column=0, row=1, win=window,
                                           command=show_one_target, sticky="W", columnspan=6)
    insert_text(text="Left button target color:", column=0, row=2, win=window, sticky="W", columnspan=6)
    left_button_color = insert_button(text="Choose color", column=0, row=2, command=choose_left_color, size=9,
                                      win=window, columnspan=6)
    right_button_color_text = insert_text(text="Right button target color:", column=0, row=3, win=window,
                                          sticky="W", columnspan=6)
    right_button_color = insert_button(text="Choose color", column=0, row=3, command=choose_right_color, size=9,
                                       win=window, columnspan=6)
    click_show_time, click_show_time_var = insert_checkbutton(text="Mark first selected node till end of a trial",
                                                              column=0, row=4, sticky="W", win=window, columnspan=4)

    # ---------------- Trial time ---------------- #
    insert_text(text="Trial time", column=0, row=7, size=14, sticky="W", win=window)
    Separator(window, orient='horizontal').place(x=0, y=165, relwidth=1, height=2)

    insert_text(text="Trial time limit (sec):", column=0, row=9, win=window, sticky="W", columnspan=3)
    trial_time = insert_entry(column=2, row=9, width=5, sticky="E", win=window, columnspan=1)
    insert_text(text="Break between trials (sec):", column=0, row=10, win=window, sticky="W", columnspan=3)
    break_time = insert_entry(column=2, row=10, width=5, sticky="E", win=window, columnspan=1)

    # ---------------- Trial info ---------------- #
    # Separator(window, orient='horizontal').place(x=0, y=245, relwidth=1, height=2)
    insert_text(text="Trial info", column=0, row=12, size=14, sticky="W", win=window)
    Separator(window, orient='horizontal').place(x=0, y=288, relwidth=1, height=2)

    # Trial number
    _, show_trial_number_var = insert_checkbutton(text="Show trial number", column=0, row=13, win=window,
                                                  sticky="W", columnspan=6, command=show_number)
    trial_number_position_x_text = insert_text(text="x:", column=2, row=14, win=window, sticky="EW", columnspan=1)
    trial_number_position_x = insert_entry(column=2, row=14, width=5, sticky="E", win=window, columnspan=1)
    trial_number_position_y_text = insert_text(text="y:", column=3, row=14, win=window, sticky="W", columnspan=1)
    trial_number_position_y = insert_entry(column=3, row=14, width=5, sticky="E", win=window, columnspan=1)
    trial_number_position_text = insert_text(text="\tTrial number position:", column=0, row=14, win=window,
                                             sticky="W", columnspan=3)
    trial_number_size_text = insert_text(text="\tTrial number size (px):", column=0, row=15, win=window, columnspan=6,
                                         sticky="W")
    trial_number_size = insert_entry(column=2, row=15, width=5, sticky="E", win=window, columnspan=1)

    # Show mouse buttons
    _, show_mouse_buttons_var = insert_checkbutton(text="Show mouse buttons reminder", column=0, row=17,
                                                   win=window, sticky="W", columnspan=6, command=show_buttons)
    mouse_buttons_position_x_text = insert_text(text="x:", column=2, row=18, win=window, sticky="EW", columnspan=1)
    mouse_buttons_position_x = insert_entry(column=2, row=18, width=5, sticky="E", win=window, columnspan=1)
    mouse_buttons_position_y_text = insert_text(text="y:", column=3, row=18, win=window, sticky="W", columnspan=1)
    mouse_buttons_position_y = insert_entry(column=3, row=18, width=5, sticky="E", win=window, columnspan=1)
    mouse_buttons_position_text = insert_text(text="\tMouse buttons position:", column=0, row=18, win=window,
                                              sticky="W", columnspan=3)
    mouse_buttons_size_text = insert_text(text="\tMouse buttons size (px):", column=0, row=19, win=window,
                                          columnspan=6, sticky="W")
    mouse_buttons_size = insert_entry(column=2, row=19, width=5, sticky="E", win=window, columnspan=1)

    # Clock
    _, show_clock_icon_var = insert_checkbutton(text="Show clock icon (reminder of short time left)", columnspan=6,
                                                column=0, row=21, win=window, command=show_clock, sticky="W")
    clock_time_text = insert_text(text="\tShow n sec before time limit:", column=0, row=23, win=window,
                                  sticky="W", columnspan=6)
    clock_time = insert_entry(column=2, row=23, width=5, sticky="E", win=window, columnspan=1)
    clock_position_x_text = insert_text(text="x:", column=2, row=25, win=window, sticky="EW", columnspan=1)
    clock_position_x = insert_entry(column=2, row=25, width=5, sticky="E", win=window, columnspan=1)
    clock_position_y_text = insert_text(text="y:", column=3, row=25, win=window, sticky="W", columnspan=1)
    clock_position_y = insert_entry(column=3, row=25, width=5, sticky="E", win=window, columnspan=1)
    clock_position_text = insert_text(text="\tClock position:", column=0, row=25, win=window, sticky="W", columnspan=3)
    clock_size_text = insert_text(text="\tClock size (px):", column=0, row=26, win=window, columnspan=6, sticky="W")
    clock_size = insert_entry(column=2, row=26, width=5, sticky="E", win=window, columnspan=1)

    insert_text(text="", column=0, row=29, size=12, win=window)

    # ------------------ Other ------------------- #

    insert_button(text="    Back    ", column=2, row=30, command=go_back, size=12, win=window, columnspan=1, sticky="W")
    next_button = insert_button(text="    Next     ", column=3, row=30, command=alerts, size=12, sticky="W",
                                win=window, columnspan=1)
    orig_button_background = next_button['background']
    orig_button_foreground = next_button['foreground']

    add_info_from_config()
    show_number()
    show_buttons()
    show_clock()
    show_one_target()

    window.mainloop()
    return information
