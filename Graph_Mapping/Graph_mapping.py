import atexit
from psychopy import visual, event, core # , logging
from os.path import join
import csv
import random

from sources.experiment_info import experiment_info
from sources.load_data import load_config, load_trials, replace_polish
from sources.screen import get_screen_res
from sources.show_info import show_info, show_image
from sources.trial import trial
from sources.randomized_experiment import prepare_randomized_experiment
from sources.edit_image import convert_mouse_colors

part_id, part_sex, part_age, date = experiment_info()
NAME = "{}_{}_{}".format(part_id, part_sex[:1], part_age)
RAND = str(random.randint(100, 999))

RESULTS = list()
RESULTS.append(["ID", "GENDER", "AGE", "DATE",
                "ORDER", "NR", 'EXPERIMENT',
                "Nodes_A", "Edges_A", "Nodes_B", "Edges_B", "Left_button_targets", "Right_button_targets",
                "Number_of_nodes", "Number_of_edges", "Type", "Crossed_edges",
                "LEFT_ANS", "RIGHT_ANS",
                'LEFT_CORRECT', "RIGHT_CORRECT", "CORRECT",
                "LEFT_RT", "RIGHT_RT", 'RT'
                ])


SUMMARY_RESULTS = list()
SUMMARY_RESULTS.append(["ID", "GENDER", "AGE", "DATE",
                        "N_of_exp_trials_applied", "N_of_trials_with_answer",
                        "N_of_correct_trials", "Percent_correct", "Mean_RT"])

n_of_exp_trials_applied = 0
n_of_trials_with_answer = 0
n_of_correct_exp_trials = 0


@atexit.register
def save_results():
    with open(join('results', 'raw_results', '{}_{}.csv'.format(NAME, RAND)), 'w', newline='') as f:
        beh_writer = csv.writer(f, delimiter=";")
        beh_writer.writerows(RESULTS)

    percent_correct = 0
    mean_rt = 0
    if n_of_exp_trials_applied > 0:
        percent_correct = round(n_of_correct_exp_trials/n_of_exp_trials_applied, 3)
    if n_of_trials_with_answer > 0:
        mean_rt = round(RT_sum/n_of_trials_with_answer, 3)
    SUMMARY_RESULTS.append([part_id, part_sex, part_age, date,
                            n_of_exp_trials_applied, n_of_trials_with_answer, n_of_correct_exp_trials, percent_correct,
                            mean_rt])
    with open(join('results', 'summary_results', '{}_{}.csv'.format(NAME, RAND)), 'w', newline='') as s:
        beh_sum_writer = csv.writer(s, delimiter=";")
        beh_sum_writer.writerows(SUMMARY_RESULTS)


def prepare_result(i, info, answers, rt, acc, exp):
    return [part_id, part_sex, part_age, date,
            i, info["NR"], exp,
            # "VA", "EA", "VB", "EB",
            info["Nodes_A"], info["Edges_A"], info["Nodes_B"], info["Edges_B"],
            # "Left_button_targets", "Right_button_targets"
            info["Left_button_targets"], info["Right_button_targets"],
            # "NV", "NE", "Type", Crossed_edges
            info["Number_of_nodes"], info["Number_of_edges"], info["Type"], info["Crossed_edges"],
            # "LEFT_ANS", "RIGHT_ANS",
            answers["left"], answers["right"],
            # 'LEFT_ACC', "RIGHT_ACC", "ACC",
            acc["left"], acc["right"], acc["left"] and acc["right"],
            # "LEFT_RT", "RIGHT_RT",
            rt["left"], rt["right"],
            # 'RT'
            round(max(rt["left"], rt["right"]), 3) if rt["left"] and rt["right"] else None]


config = load_config("config.yaml", concatenate=True)

SCREEN_RES = get_screen_res()
window = visual.Window(SCREEN_RES, fullscr=True, units='pix', color=config["background_color"])
mouse = event.Mouse(visible=True)

if config["show_clock_icon"]:
    clock_image = visual.ImageStim(win=window, image=join('images', 'clock.png'), size=config['clock_size'],
                                   interpolate=True, pos=[config['clock_position_x'], config['clock_position_y']])
else:
    clock_image = None

if config["show_mouse_buttons"]:
    convert_mouse_colors(config["left_button_color"], config["right_button_color"])
    mouse_info = visual.ImageStim(win=window, image=join('images', 'mouse_info_2.PNG'), interpolate=True,
                                  size=config["mouse_buttons_size"],
                                  pos=[config["mouse_buttons_position_x"], config["mouse_buttons_position_y"]])
else:
    mouse_info = None

if config["one_target"]:
    answers_colors = [config["left_button_color"]]
else:
    answers_colors = [config["left_button_color"], config["right_button_color"]]

if config["feedback"]:
    pos_feedb = visual.TextStim(window, text=replace_polish(config["correct_answer"]), pos=config["feedback_position"],
                                color=config["correct_answer_color"], height=config["feedback_text_size"])
    neg_feedb = visual.TextStim(window, text=replace_polish(config["incorrect_answer"]),
                                height=config["feedback_text_size"], pos=config["feedback_position"],
                                color=config["incorrect_answer_color"])
    no_feedb = visual.TextStim(window, text=replace_polish(config["no_answer"]), pos=config["feedback_position"],
                               color=config["no_answer_color"], height=config["feedback_text_size"])
    feedb = {"pos": pos_feedb, "neg": neg_feedb, "no": no_feedb}
else:
    feedb = None


# TRAINING
if config["training_session"]:
    data_train, _ = load_trials(file_name=join("training", config['predefined_training']),
                                randomize_graphs=config["randomize_graphs"])
    mean_acc = 0
    training_nr = 0
    while mean_acc < config["training_accuracy"] or training_nr < 1:

        show_image(window, 'instruction1.png', SCREEN_RES)
        show_image(window, 'instruction2.png', SCREEN_RES)
        show_image(window, 'instruction3.png', SCREEN_RES)
        show_image(window, 'instruction4.png', SCREEN_RES)
        show_image(window, 'instruction5.png', SCREEN_RES)

        mean_acc = 0
        i = 1
        training_nr += 1
        for info in data_train:
            if config["show_trial_number"]:
                idx_info = visual.TextStim(window, color=config["text_color"], height=config["trial_number_size"], text=i,
                                           pos=[config["trial_number_position_x"], config["trial_number_position_y"]])
            else:
                idx_info = None
            answers, rt, acc, A_to_B_relation = trial(window, config, answers_colors, info, mouse, clock_image,
                                                      feedb, mouse_info, idx_info)

            RESULTS.append(prepare_result(i, info, answers, rt, acc, "train"))
            i += 1
            if not config["one_target"]:
                mean_acc += 1 if acc["left"] and acc["right"] else 0
            else:
                mean_acc += 1 if acc["left"] else 0
        if i > 1:
            mean_acc /= (i - 1)
        else:
            print("AA")
            break
        if mean_acc < config["training_accuracy"] and training_nr == config['training_attempts']:
            show_info(window, join('.', 'texts', "too_many_attempts.txt"), text_size=config['text_size'],
                      screen_width=SCREEN_RES[0], color=config['text_color'])
            exit(1)
        if mean_acc < config["training_accuracy"]:
            show_info(window, join('.', 'texts', "after_unsuccessful_training.txt"), text_size=config['text_size'],
                      screen_width=SCREEN_RES[0], color=config['text_color'])

# EXPERIMENT
if config["session_type"] == "Predefined test":
    _, data_exp = load_trials(join("tests", config['predefined_test']))
    if config["randomize_trials_order"]:
        random.shuffle(data_exp)
else:
    _, data_exp = load_trials(join("experiment", "experiment.csv"))
    data_exp = prepare_randomized_experiment(data_exp, config)
    random.shuffle(data_exp)

if config["training_session"]:
    show_info(window, join('.', 'texts', "after_training.txt"), text_size=config['text_size'],
              screen_width=SCREEN_RES[0], key="q", color=config['text_color'])
else:
    # INSTRUCTIONS
    show_image(window, 'instruction1.png', SCREEN_RES)
    show_image(window, 'instruction2.png', SCREEN_RES)
    show_image(window, 'instruction3.png', SCREEN_RES)
    show_image(window, 'instruction4.png', SCREEN_RES)
    show_image(window, 'instruction5.png', SCREEN_RES)

i = 1
RT_sum = 0
for info in data_exp:
    if config["show_trial_number"]:
        idx_info = visual.TextStim(window, color=config["text_color"], height=config["trial_number_size"], text=i,
                                   pos=[config["trial_number_position_x"], config["trial_number_position_y"]])
    else:
        idx_info = None
    answers, rt, acc, A_to_B_relation = trial(window, config, answers_colors, info,
                                              mouse, clock_image, feedb, mouse_info, idx_info)
    RESULTS.append(prepare_result(i, info, answers, rt, acc, "exp"))

    n_of_exp_trials_applied += 1
    if config["one_target"]:
        n_of_correct_exp_trials += int(acc["left"])
        RT_sum += rt["left"] if rt["left"] else 0
        n_of_trials_with_answer += 1 if rt["left"] else 0
    else:
        n_of_correct_exp_trials += int(acc["left"] and acc["right"])
        RT_sum += max(rt["left"], rt["right"]) if rt["left"] and rt["right"] else 0
        n_of_trials_with_answer += 1 if rt["left"] and rt["right"] else 0

    if config['break_after_n_trials'] > 0 and i % config['break_after_n_trials'] == 0:
        show_info(window, join('.', 'texts', "break.txt"), text_size=config['text_size'] + 25,
                  screen_width=SCREEN_RES[0], key="q", color=config['text_color'])

    i += 1

show_info(window, join('.', 'texts', "end.txt"), text_size=config['text_size'],
          screen_width=SCREEN_RES[0], color=config['text_color'])
