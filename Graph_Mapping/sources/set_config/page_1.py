from tkinter import IntVar, END, StringVar, messagebox
from tkinter.ttk import Separator
from sources.set_config.tkinter_elements import *
from sources.set_config.utils import *
from sources.set_config.alerts import *
import os


def page_1(info):
    global information, session_type
    information = None
    window = create_window("Set config", 550, 720)
    session_type = IntVar()
    session_type.set(-1)

    def training():
        elements = [predefined_training_text, training_accuracy_text, training_accuracy,
                    training_attempts_text, training_attempts]
        show_on_off(elements, training_session_var, ["disabled", "normal"])
        show_on_off([predefined_training], training_session_var, ["disabled", "readonly"])

    def session():
        elements_left = [randomize_trials_order, randomize_graphs]
        elements_right = [choose_factor_levels, no_of_edges, edges_3, edges_4, edges_5, crossed_edges,
                          graphs_with_crossed, graphs_without_crossed_edges, types_of_target_vertices, direct,
                          indirect, trials_per_cell_text, trials_per_cell, n_of_trials_text]

        show_on_off(elements_left, session_type, ["normal", "disabled"])
        show_on_off([predefined_test_list], session_type, ["readonly", "disabled"])
        show_on_off(elements_right, session_type, ["disabled", "normal"])

    def change_n_of_trials(new):
        n_of_trials.configure(state="normal")
        n_of_trials.delete(0, END)
        n_of_trials.insert(0, new)
        n_of_trials.configure(state="disabled")

    def calculate_n_of_trials():
        if any([edges_3_var.get(), edges_4_var.get(), edges_5_var.get()]) and \
           any([graphs_with_crossed_var.get(), graphs_without_crossed_edges_var.get()]) and \
           any([direct_var.get(), indirect_var.get()]):
            try:
                n = sum([edges_3_var.get(), edges_4_var.get(), edges_5_var.get()]) * \
                    sum([graphs_with_crossed_var.get(), graphs_without_crossed_edges_var.get()]) * \
                    sum([direct_var.get(), indirect_var.get()]) * \
                    int(trials_per_cell.get())
                change_n_of_trials(n)
            except ValueError:
                change_n_of_trials("?")
        else:
            change_n_of_trials("?")

    def add_info_from_config():
        try:
            # Training
            training_session_var.set(info["training_session"])
            predefined_training.set(info["predefined_training"])
            if info["training_accuracy"] is not None:
                training_accuracy.insert(0, info["training_accuracy"])
            if info["training_attempts"] is not None:
                training_attempts.insert(0, info["training_attempts"])
            # Session type
            session_type.set(0 if info["session_type"] == "Predefined test" else 1)
            # Predefined test
            predefined_test_list.set(info["predefined_test"])
            randomize_trials_order_var.set(info["randomize_trials_order"])
            randomize_graphs_var.set(info["randomize_graphs"])
            # Randomized experiment
            edges_3_var.set(info["no_of_edges"]["3"])
            edges_4_var.set(info["no_of_edges"]["4"])
            edges_5_var.set(info["no_of_edges"]["5"])
            graphs_with_crossed_var.set(info["crossed_edges"]["graphs_with_crossed"])
            graphs_without_crossed_edges_var.set(info["crossed_edges"]["graphs_without_crossed_edges"])
            direct_var.set(info["types_of_target_vertices"]["direct"])
            indirect_var.set(info["types_of_target_vertices"]["indirect"])
            if info["trials_per_cell"] is not None:
                trials_per_cell.insert(0, info["trials_per_cell"])
            if info["n_of_trials"] is not None:
                n_of_trials.insert(0, info["n_of_trials"])
            if info["break_after_n_trials"] is not None:
                break_after_n_trials.insert(0, info["break_after_n_trials"])
        except:
            messagebox.showerror(message="Can't load file with config")
            break_after_n_trials.focus_force()

    def alerts():
        global information, session_type
        # ----------------- Training ----------------- #
        if training_session_var.get() == 1:
            if not try_combobox(predefined_training, "predefined training"):
                return None
            tr_acc = try_convert_to_float(training_accuracy.get(), "Required training accuracy")
            if not try_in_range(tr_acc, "Required training accuracy", v_min=0, v_max=1):
                return None
            tr_attempts = try_convert_to_int(training_attempts.get(), "Training attempts")
            if not try_in_range(tr_attempts, "Training attempts", v_min=0):
                return None
        else:
            tr_acc = None
            tr_attempts = None
        # ---------------- Experiment ---------------- #
        if session_type.get() == 0:
            if not try_combobox(predefined_test_list, "predefined test"):
                return None
        if session_type.get() == 1:
            if not try_any([edges_3_var.get(), edges_4_var.get(), edges_5_var.get()], "No. of edges"):
                return None
            if not try_any([graphs_with_crossed_var.get(), graphs_without_crossed_edges_var.get()], "Crossed edges"):
                return None
            if not try_any([direct_var.get(), indirect_var.get()], "Types of target vertices"):
                return None
            t_per_cell = try_convert_to_int(trials_per_cell.get(), "'No. of trials per cell attempts")
            if not try_in_range(t_per_cell, "Training 'No. of trials per cell", v_min=1):
                return None
            n_trials = try_convert_to_int(n_of_trials.get(), "'No. of trials")

        else:
            t_per_cell = None
            n_trials = None

        if session_type.get() not in [0, 1]:
            messagebox.showerror(message="You have to choose \"Predefined test\" or \"Randomized experiment\".")
            return None

        sess_type = "Predefined test" if session_type.get() == 0 else "Randomized experiment"

        # ------------------ Break ------------------- #
        if break_after_n_trials.get() != "":
            b_n_trails = try_convert_to_int(break_after_n_trials.get(), "Provide break after n trials")
            if not try_in_range(b_n_trails, "Provide break after n trials", v_min=0):
                return None
        else:
            b_n_trails = 0

        information = {
            # Training
            "training_session": training_session_var.get(),
            "predefined_training": predefined_training.get(),
            "training_accuracy": tr_acc,
            "training_attempts": tr_attempts,
            # Session type
            "session_type": sess_type,
            # Predefined test
            "predefined_test": predefined_test_list.get(),
            "randomize_trials_order": randomize_trials_order_var.get(),
            "randomize_graphs": randomize_graphs_var.get(),
            # Randomized experiment
            "no_of_edges": {"3": edges_3_var.get(),
                            "4": edges_4_var.get(),
                            "5": edges_5_var.get()},
            "crossed_edges": {"graphs_with_crossed": graphs_with_crossed_var.get(),
                              "graphs_without_crossed_edges": graphs_without_crossed_edges_var.get()},
            "types_of_target_vertices": {"direct": direct_var.get(),
                                         "indirect": indirect_var.get()},
            "trials_per_cell": t_per_cell,
            "n_of_trials": n_trials,
            # Break
            "break_after_n_trials": b_n_trails
        }

        window.destroy()

    def close():
        global information
        window.destroy()
        information = "close"

    insert_text(text="", column=0, row=0, size=1, win=window)
    training_session, training_session_var = insert_checkbutton(text="Training session", column=0, row=1,
                                                                size=14, columnspan=6, win=window, command=training)
    insert_text(text="", column=0, row=2, size=1, win=window)
    Separator(window, orient='horizontal').place(x=0, y=50, relwidth=1, height=2)

    training_files = os.listdir(os.path.join("trials", "training"))
    predefined_training_text = insert_text(text="Select predefined training:", column=0, row=3, sticky="W", win=window)
    predefined_training = insert_combobox(column=2, row=3, values=training_files, sticky="W", win=window)

    training_accuracy_text = insert_text(text="Min. required training accuracy:", column=0, row=4, sticky="W", win=window)
    training_accuracy = insert_entry(column=2, row=4, width=5, sticky="W", win=window)

    training_attempts_text = insert_text(text="Max. training attempts:", column=0, row=5, sticky="W", win=window)
    training_attempts = insert_entry(column=2, row=5, width=5, sticky="W", win=window)

    # -------------- Experimental session -------------- #

    Separator(window, orient='horizontal').place(x=0, y=155, relwidth=1, height=2)
    insert_text(text="Experimental session", column=0, row=7, size=14, columnspan=6, win=window)
    insert_text(text="", column=0, row=8, size=1, win=window)
    # insert_text(text="", column=0, row=9, size=1, win=window)

    Separator(window, orient='horizontal').place(x=0, y=195, relwidth=1, height=2)
    Separator(window, orient='vertical').place(relx=0.5, y=195, width=1, height=405)

    # ---------------- Predefined test ----------------- #
    insert_radiobutton(text="Predefined test", column=0, row=9, selector=session_type, value=0, size=12,
                       columnspan=3, command=session, win=window)
    insert_text(text="", column=0, row=19, size=1, win=window)
    tests_files = os.listdir(os.path.join("trials", "tests"))
    predefined_test_list = insert_combobox(column=0, row=11, values=tests_files, columnspan=2, win=window)
    insert_text(text="", column=0, row=12, size=1, win=window)
    randomize_trials_order, randomize_trials_order_var = insert_checkbutton(text="Randomize trials order", columnspan=3,
                                                                            row=13, column=0, sticky="W", win=window)
    randomize_graphs, randomize_graphs_var = insert_checkbutton(text="Randomize graphs", column=0, row=14, columnspan=3,
                                                                sticky="W", win=window)

    # -------------- Randomized experiment ------------- #
    insert_radiobutton(text="Randomized experiment", column=3, row=9, selector=session_type, value=1, size=12,
                       columnspan=3, command=session, win=window)
    choose_factor_levels = insert_text(text="Choose factor levels (max 3x2x2):", column=3, row=11, columnspan=3,
                                       sticky="W", size=11, win=window)

    # insert_text(text="", column=0, row=11, size=1, win=window)

    no_of_edges = insert_text(text="No. of edges:", column=3, row=12, columnspan=3, sticky="W", win=window)
    edges_3, edges_3_var = insert_checkbutton(text="3", column=3, row=13, columnspan=1, sticky="W",
                                              win=window, command=calculate_n_of_trials)
    edges_4, edges_4_var = insert_checkbutton(text="4", column=3, row=13, columnspan=2, sticky="",
                                              win=window, command=calculate_n_of_trials)
    edges_5, edges_5_var = insert_checkbutton(text="5", column=3, row=13, columnspan=3, sticky="",
                                              win=window, command=calculate_n_of_trials)

    crossed_edges = insert_text(text="Crossed edges:", column=3, row=14, columnspan=3, sticky="W", win=window)
    graphs_with_crossed, graphs_with_crossed_var = insert_checkbutton(text="Graphs with crossed edges", column=3,
                                                                      row=15, columnspan=3, sticky="W", win=window,
                                                                      command=calculate_n_of_trials)
    graphs_without_crossed_edges, graphs_without_crossed_edges_var = \
        insert_checkbutton(text="Graphs without crossed edges", column=3, row=16, columnspan=3,
                           sticky="W", win=window, command=calculate_n_of_trials)

    insert_text(text="", column=0, row=17, size=1, win=window)

    types_of_target_vertices = insert_text(text="Types of target vertices:", column=3, row=18,
                                           columnspan=3, sticky="W", win=window)
    direct, direct_var = insert_checkbutton(text="Direct", column=3, row=19, columnspan=3, sticky="W",
                                            win=window, command=calculate_n_of_trials)
    indirect, indirect_var = insert_checkbutton(text="Indirect", column=3, row=19, columnspan=3, sticky="",
                                                win=window, command=calculate_n_of_trials)

    insert_text(text="", column=0, row=20, size=1, win=window)
    insert_text(text="", column=0, row=21, size=1, win=window)

    trials_per_cell_text = insert_text(text="No. of trials per cell:", column=3, row=22,
                                       columnspan=2, sticky="W", win=window)
    s_var = StringVar()
    s_var.trace("w", lambda name, index, mode, sv=s_var: calculate_n_of_trials())
    trials_per_cell = insert_entry(column=5, row=22, width=5, columnspan=1, sticky="W", win=window, textvariable=s_var)

    n_of_trials_text = insert_text(text="Total n of trials:", column=3, row=23, columnspan=2, sticky="W", win=window)
    n_of_trials = insert_entry(column=5, row=23, width=5, columnspan=1, sticky="W", win=window)
    change_n_of_trials("?")

    # --------- Break ---------- #
    Separator(window, orient='horizontal').place(x=0, y=600, relwidth=1, height=2)

    insert_text(text="Provide break after n trials:", column=0, row=27, win=window, size=14, columnspan=5)
    break_after_n_trials = insert_entry(column=2, row=27, width=5, sticky="E", win=window)

    Separator(window, orient='horizontal').place(x=0, y=650, relwidth=1, height=2)

    # --------- Experimental session disabled ---------- #
    add_info_from_config()
    training()
    session()

    # ------------------ Other ------------------- #

    insert_button(text="  Cancel  ", column=1, row=32, command=close, size=12, win=window, columnspan=1, sticky="E")
    insert_button(text="    Next     ", column=3, row=32, command=alerts, size=12, win=window, columnspan=1)

    window.mainloop()

    return information
