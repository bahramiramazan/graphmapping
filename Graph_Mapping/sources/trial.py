import time
import random
from psychopy import event, core, visual

from sources.matrix import Matrix
from sources.check_exit import check_exit
from sources.load_data import replace_polish
from sources.matrix_operations import rotate_matrices_in_trial, mirror_matrices_in_trial


def trial(window, config, answers_colors, info, mouse, clock_image, feedb, mouse_info, idx_info):
    response_clock = core.Clock()
    a_to_b_relation = None
    press_space_msg = None
    transformation_a = None
    transformation_b = None
    if config["randomize_graphs"] or config["session_type"] == "Randomized experiment" and info['TRAIN'] == 0:
        while True:
            for matrix in ["A", "B"]:
                if random.choice([True, False]):
                    rotate_matrices_in_trial(info, matrix)
                    if matrix == "A":
                        transformation_a = "ROTATION"
                    else:
                        transformation_b = "ROTATION"
                else:
                    mirror_matrices_in_trial(info, matrix)
                    if matrix == "A":
                        transformation_a = "MIRROR"
                    else:
                        transformation_b = "MIRROR"
            if info["Nodes_A"] != info["Nodes_B"] or info["Edges_A"] != info["Edges_B"]:
                if transformation_a == transformation_b:
                    a_to_b_relation = "ROTATION"
                else:
                    a_to_b_relation = "MIRROR"
                break
    if not config["randomize_graphs"] or not config["session_type"] == "Randomized experiment" \
            or info['TRAIN'] == 1 or random.choice([True, False]):
        a = Matrix(win=window, pos=config["left_graph_position"], config=config, v=info["Nodes_A"], e=info["Edges_A"])
        b = Matrix(win=window, pos=config["right_graph_position"], config=config, v=info["Nodes_B"], e=info["Edges_B"])
    else:
        a = Matrix(win=window, pos=config["left_graph_position"], config=config, v=info["Nodes_B"], e=info["Edges_B"])
        b = Matrix(win=window, pos=config["right_graph_position"], config=config, v=info["Nodes_A"], e=info["Edges_A"])
        info["Left_button_targets"] = info["Left_button_targets"][::-1]
        info["Right_button_targets"] = info["Right_button_targets"][::-1]

    switch_targets = False
    if not config["one_target"] and (config["session_type"] == "Randomized experiment" or config["randomize_graphs"])\
            and info['TRAIN'] == 0 and random.choice([True, False]):
        a.mark_answer(v_nr=info["Left_button_targets"][0], color=answers_colors[1])
        a.mark_answer(v_nr=info["Right_button_targets"][0], color=answers_colors[0])
        switch_targets = True
    elif not config["one_target"]:
        a.mark_answer(v_nr=info["Left_button_targets"][0], color=answers_colors[0])
        a.mark_answer(v_nr=info["Right_button_targets"][0], color=answers_colors[1])
    elif (config["session_type"] == "Randomized experiment" or config["randomize_graphs"]) \
            and info['TRAIN'] == 0 and random.choice([True, False]):
        a.mark_answer(v_nr=info["Right_button_targets"][0], color=answers_colors[0])
        switch_targets = True
    else:
        a.mark_answer(v_nr=info["Left_button_targets"][0], color=answers_colors[0])

    if config["feedback"]:
        press_space_msg = visual.TextStim(window, text=replace_polish(config["press_space_message"]),
                                          color=config["press_space_button_color"], height=config["feedback_text_size"],
                                          pos=[config["feedback_position"][0], config["feedback_position"][1] - 60])
    a.set_auto_draw(True)
    b.set_auto_draw(True)
    window.callOnFlip(response_clock.reset)
    event.clearEvents()
    if config["show_mouse_buttons"]:
        mouse_info.setAutoDraw(True)
    if config["show_trial_number"]:
        idx_info.setAutoDraw(True)
    window.flip()

    click = {"left": False, "right": False}
    answers = {"left": None, "right": None}
    rt = {"left": None, "right": None}
    if not config["one_target"]:
        while response_clock.getTime() < config["trial_time"] and not (click["left"] and click["right"]):
            for idx, point in b.v:
                if not click["left"] and mouse.isPressedIn(point, buttons=[0]):
                    rt["left"] = response_clock.getTime()
                    b.mark_answer(idx, color=answers_colors[0])
                    window.flip()
                    if not config["click_show_time"]:
                        time.sleep(0.2)
                        b.mark_answer(idx, color=config["vertices_color"])
                        window.flip()
                    click["left"] = True
                    answers["left"] = idx
                elif not click["right"] and mouse.isPressedIn(point, buttons=[2]):
                    rt["right"] = response_clock.getTime()
                    b.mark_answer(idx, color=answers_colors[1])
                    window.flip()
                    if not config["click_show_time"]:
                        time.sleep(0.2)
                        b.mark_answer(idx, color=config["vertices_color"])
                        window.flip()
                    click["right"] = True
                    answers["right"] = idx
            if config["show_clock_icon"] and config["trial_time"] - response_clock.getTime() < config['clock_time']:
                clock_image.setAutoDraw(True)
            check_exit()
            window.flip()
        if config["show_clock_icon"]:
            clock_image.setAutoDraw(False)
        if not switch_targets:
            acc = {"left": answers["left"] == info["Left_button_targets"][1],
                   "right": answers["right"] == info["Right_button_targets"][1]}
        else:
            acc = {"left": answers["left"] == info["Right_button_targets"][1],
                   "right": answers["right"] == info["Left_button_targets"][1]}
    else:
        while response_clock.getTime() < config["trial_time"] and not click["left"]:
            for idx, point in b.v:
                if not click["left"] and mouse.isPressedIn(point, buttons=[0]):
                    rt["left"] = response_clock.getTime()
                    b.mark_answer(idx, color=answers_colors[0])
                    window.flip()
                    if not config["click_show_time"]:
                        time.sleep(0.2)
                        b.mark_answer(idx, color=config["vertices_color"])
                        window.flip()
                    click["left"] = True
                    answers["left"] = idx
            if config["show_clock_icon"] and \
               config["trial_time"] - response_clock.getTime() < config['click_show_time']:
                clock_image.setAutoDraw(True)
            check_exit()
            window.flip()
        if config["show_clock_icon"]:
            clock_image.setAutoDraw(False)
        if not switch_targets:
            acc = {"left": answers["left"] == info["Left_button_targets"][1], "right": answers["right"]}
        else:
            acc = {"left": answers["left"] == info["Right_button_targets"][1], "right": answers["right"]}

    b.mark_answer(answers["left"], color=config["vertices_color"])
    b.mark_answer(answers["right"], color=config["vertices_color"])

    if config["feedback"] and info["FEED"] == 1:
        b.mark_answer(info["Left_button_targets"][1], color=answers_colors[0])
        if not config["one_target"]:
            b.mark_answer(info["Right_button_targets"][1], color=answers_colors[1])

        if not config["one_target"]:
            if not click["left"] or not click["right"]:
                feedb["no"].setAutoDraw(True)
            elif acc["left"] and acc["right"]:
                feedb["pos"].setAutoDraw(True)
            else:
                feedb["neg"].setAutoDraw(True)
            window.flip()
        else:
            if not click["left"]:
                feedb["no"].setAutoDraw(True)
            elif acc["left"]:
                feedb["pos"].setAutoDraw(True)
            else:
                feedb["neg"].setAutoDraw(True)
            window.flip()

        press_space_msg.setAutoDraw(True)
        window.flip()
        event.waitKeys(keyList=['f7', 'space'])

    a.set_auto_draw(False)
    b.set_auto_draw(False)
    if config["show_mouse_buttons"]:
        mouse_info.setAutoDraw(False)
    if config["show_trial_number"]:
        idx_info.setAutoDraw(False)
    if config["feedback"]:
        press_space_msg.setAutoDraw(False)
        for k, v in feedb.items():
            v.setAutoDraw(False)

    window.flip()
    time.sleep(config["break_time"])
    return answers, rt, acc, a_to_b_relation
