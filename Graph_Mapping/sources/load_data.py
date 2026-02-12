import yaml
from os.path import join
import csv
import ast
import random


def load_config(file_name="config.yaml", concatenate=False):
    try:
        with open(file_name) as yaml_file:
            doc = yaml.safe_load(yaml_file)
        if concatenate:
            doc = {**doc[1], **doc[2], **doc[3], **doc[4]}
        return doc
    except:
        raise Exception("Can't load config file")


def load_trials(file_name, randomize_graphs=False):
    file_path = join("trials", file_name)
    try:
        with open(file_path) as f:
            reader = csv.reader(f, delimiter=';')
            header = None
            data_train = []
            data_exp = []
            for row in reader:
                if not header:
                    header = row
                else:
                    data_row = {k: v for k, v in zip(header, row)}
                    for k in ["NR", "FEED", "TRAIN", "Number_of_nodes", "Number_of_edges"]:
                        data_row[k] = int(data_row[k])
                    for k in ["Nodes_A", "Nodes_B"]:
                        data_row[k] = [int(elem) for elem in data_row[k].split(",")]
                    for k in ["Edges_A", "Edges_B", "Left_button_targets", "Right_button_targets"]:
                        data_row[k] = ast.literal_eval(data_row[k])

                    if randomize_graphs and random.choice([True, False]):
                        data_row["Nodes_A"], data_row["Nodes_B"] = data_row["Nodes_B"], data_row["Nodes_A"]
                        data_row["Edges_A"], data_row["Edges_B"] = data_row["Edges_B"], data_row["Edges_A"]
                        data_row["Left_button_targets"], data_row["Right_button_targets"] = data_row["Right_button_targets"], data_row["Left_button_targets"]

                    if data_row["TRAIN"] == 1:
                        data_train.append(data_row)
                    else:
                        data_exp.append(data_row)
        # block_nr = set([info["Block"] for info in data_exp])
        # data_exp = [[info for info in data_exp if info["Block"] == i] for i in block_nr]
        return data_train, data_exp
    except:
        raise Exception("Can't load file with items: " + file_name)


def replace_polish(text):
    letters = {"Ĺ»": "Ż", "Ã": "Ó", "Ă“": "Ł", "Ä†": "Ć", "Ä": "Ę", "Ĺš": "Ś", "Ä„": "Ą", "Ĺą": "Ź", "Å": "Ń",
               "ĹĽ": "ż", "Ã³": "ó", "Ĺ‚": "ł", "Ä‡": "ć", "Ä™": "ę", "Ĺ›": "ś", "Ä…": "ą", "Ĺş": "ź", "Ĺ„": "ń"}

    for k, v in letters.items():
        text = text.replace(k, v)
    return text
