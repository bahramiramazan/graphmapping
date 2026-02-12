from tkinter.ttk import Separator
from sources.set_config.tkinter_elements import *
from sources.set_config.utils import *
from sources.set_config.alerts import *


def page_3(info):

    def feedback_on_off():
        elements = [correct_answer_text, correct_answer, correct_color_text, correct_answer_button_color,
                    incorrect_answer_text, incorrect_answer, incorrect_color_text, incorrect_answer_button_color,
                    no_answer_text, no_answer, no_answer_color_text, no_answer_button_color,
                    press_space_message_text, press_space_message,
                    press_space_button_color_text, press_space_button_color,
                    feedback_text_size_text, feedback_text_size,
                    feedback_position_x_text, feedback_position_x, feedback_position_y_text, feedback_position_y,
                    feedback_position_text]
        show_on_off(elements, feedback_var, ["disabled", "normal"])

    def choose_correct_answer():
        return choose_button_color(correct_answer_button_color, title="Choose correct answer feedback text color")

    def choose_incorrect_answer():
        return choose_button_color(incorrect_answer_button_color, title="Choose incorrect answer feedback text color")

    def choose_no_answer():
        return choose_button_color(no_answer_button_color, title="Choose no answer feedback text color")

    def choose_press_space():
        return choose_button_color(press_space_button_color, title="Choose press space text color")

    def go_back():
        global information
        window.destroy()
        information = "go_back"

    def add_info_from_config():
        try:
            feedback_var.set(info["feedback"])
            if info["feedback"]:
                correct_answer.insert(0, info["correct_answer"])
                incorrect_answer.insert(0, info["incorrect_answer"])
                no_answer.insert(0, info["no_answer"])
                press_space_message.insert(0, info["press_space_message"])

                change_button_color(correct_answer_button_color, info["correct_answer_color"])
                change_button_color(incorrect_answer_button_color, info["incorrect_answer_color"])
                change_button_color(no_answer_button_color, info["no_answer_color"])
                change_button_color(press_space_button_color, info["press_space_button_color"])

                feedback_text_size.insert(0, info["feedback_text_size"])
                feedback_position_x.insert(0, info["feedback_position"][0])
                feedback_position_y.insert(0, info["feedback_position"][1])

        except:
            messagebox.showerror(message="Can't load file with config")
            feedback.focus_force()

    def alerts():
        global information
        if feedback_var.get():
            if not try_button_color(correct_answer_button_color, orig_button_background, "correct answer text"):
                return None
            if not try_button_color(incorrect_answer_button_color, orig_button_background, "incorrect answer text"):
                return None
            if not try_button_color(no_answer_button_color, orig_button_background, "no answer text"):
                return None
            if not try_button_color(press_space_button_color, orig_button_background, "press space text"):
                return None

            txt_size = try_convert_to_int(feedback_text_size.get(), "Feedback text size")
            if not try_in_range(txt_size, "Feedback text size", v_min=0):
                return None

            f_position_x = try_convert_to_int(feedback_position_x.get(), "Feedback x position")
            if f_position_x is None:
                return None
            f_position_y = try_convert_to_int(feedback_position_y.get(), "Feedback y position")
            if f_position_y is None:
                return None
        else:
            txt_size = None
            f_position_x = None
            f_position_y = None

        information = {
            "feedback": feedback_var.get(),
            "correct_answer": correct_answer.get(),
            "correct_answer_color": correct_answer_button_color["background"],
            "incorrect_answer": incorrect_answer.get(),
            "incorrect_answer_color": incorrect_answer_button_color["background"],
            "no_answer": no_answer.get(),
            "no_answer_color": no_answer_button_color["background"],
            "press_space_message": press_space_message.get(),
            "press_space_button_color": press_space_button_color["background"],
            "feedback_text_size": txt_size,
            "feedback_position": [f_position_x, f_position_y]}

        window.destroy()

    global information
    information = None

    window = create_window("Set config", 550, 680)

    feedback, feedback_var = insert_checkbutton(text="Show feedback in training trials", column=0, row=1, sticky="W",
                                                win=window, command=feedback_on_off, size=16, columnspan=6)

    # TEXTS

    # Correct answer
    correct_answer_text = insert_text(text="Correct answer text:", column=0, row=2,
                                      columnspan=1, win=window, sticky="W")
    correct_answer = insert_entry(column=0, row=2, width=50, sticky="E", win=window, columnspan=6)

    # InCorrect answer
    incorrect_answer_text = insert_text(text="Incorrect answer text:", column=0, row=3,
                                        columnspan=1, win=window, sticky="W")
    incorrect_answer = insert_entry(column=0, row=3, width=50, sticky="E", win=window, columnspan=6)

    # No answer
    no_answer_text = insert_text(text="No answer text:", column=0, row=4, columnspan=1, win=window, sticky="W")
    no_answer = insert_entry(column=0, row=4, width=50, sticky="E", win=window, columnspan=6)

    # Press space
    press_space_message_text = insert_text(text="Press space text:", column=0, row=5, columnspan=1, win=window,
                                           sticky="W")
    press_space_message = insert_entry(column=0, row=5, width=50, sticky="E", win=window, columnspan=6)

    # COLORS
    correct_color_text = insert_text(text="Correct answer color:", column=0, row=7, columnspan=1, win=window,
                                     sticky="W")
    correct_answer_button_color = insert_button(text="Choose color", column=1, row=7, win=window, columnspan=1,
                                                command=choose_correct_answer, size=9, sticky="W")

    incorrect_color_text = insert_text(text="Incorrect answer color:", column=0, row=8, columnspan=1, win=window,
                                       sticky="W")
    incorrect_answer_button_color = insert_button(text="Choose color", column=1, row=8, win=window,
                                                  command=choose_incorrect_answer, size=9, sticky="W", columnspan=1)

    no_answer_color_text = insert_text(text="No answer color:", column=0, row=9, columnspan=1, win=window, sticky="W")
    no_answer_button_color = insert_button(text="Choose color", column=1, row=9, command=choose_no_answer,
                                                size=9, win=window, sticky="W", columnspan=1)

    press_space_button_color_text = insert_text(text="Press space color:", column=0, row=10, columnspan=1, win=window,
                                                sticky="W")
    press_space_button_color = insert_button(text="Choose color", column=1, row=10, command=choose_press_space,
                                             size=9, win=window, sticky="W", columnspan=1)

    # GENERAL

    feedback_text_size_text = insert_text(text="Feedback text size (px):", column=0, row=14, columnspan=1, win=window,
                                          sticky="W")
    feedback_text_size = insert_entry(column=1, row=14, width=5, sticky="E", win=window, columnspan=1)

    feedback_position_text = insert_text(text="Feedback text position:", column=0, row=15, columnspan=1, win=window,
                                         sticky="W")

    feedback_position_x_text = insert_text(text="x:", column=1, row=15, win=window, sticky="W", columnspan=1)
    feedback_position_x = insert_entry(column=1, row=15, width=5, sticky="E", win=window, columnspan=1)

    feedback_position_y_text = insert_text(text="y:", column=3, row=15, win=window, sticky="W", columnspan=1)
    feedback_position_y = insert_entry(column=3, row=15, width=5, sticky="E", win=window, columnspan=1)

    # ------------------ Other ------------------- #

    insert_button(text="    Back    ", column=0, row=32, command=go_back, size=12, win=window, columnspan=1, sticky="")
    next_button = insert_button(text="    Next     ", column=3, row=32, command=alerts, size=12, win=window,
                                columnspan=1)
    orig_button_background = next_button['background']
    add_info_from_config()
    feedback_on_off()

    window.mainloop()
    return information
