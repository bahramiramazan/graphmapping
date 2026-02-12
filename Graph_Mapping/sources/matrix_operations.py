import random


def change_info_v(v, operation):
    for i, elem in enumerate(v):
        v[i] = operation[elem]


def change_info_e(e, operation):
    for i, (a, b) in enumerate(e):
        e[i] = (operation[a], operation[b])


def change_info_answers(answer, operation):
    return operation[answer]


def rotate(v, e, left, right, n, rotate_operation):
    if n > 0:
        change_info_v(v, rotate_operation)
        change_info_e(e, rotate_operation)
        left = change_info_answers(left, rotate_operation)
        right = change_info_answers(right, rotate_operation)
        n -= 1
        left, right = rotate(v, e, left, right, n, rotate_operation)
    return left, right


def rotate_matrix(v, e, left, right):
    rotate_operation = {0: 2, 1: 5, 2: 8, 3: 1, 4: 4, 5: 7, 6: 0, 7: 3, 8: 6}
    n = random.randint(0, 3)
    return rotate(v, e, left, right, n, rotate_operation)


def mirror_matrix(v, e, left, right):
    n = random.randint(0, 3)
    if n == 0:  # |
        mirror_operation = {0: 2, 1: 1, 2: 0, 3: 5, 4: 4, 5: 3, 6: 8, 7: 7, 8: 6}
    elif n == 1:  # -
        mirror_operation = {0: 6, 1: 7, 2: 8, 3: 3, 4: 4, 5: 5, 6: 0, 7: 1, 8: 2}
    elif n == 2:  # /
        mirror_operation = {0: 8, 1: 5, 2: 2, 3: 7, 4: 4, 5: 1, 6: 6, 7: 3, 8: 0}
    elif n == 3:  # \
        mirror_operation = {0: 0, 1: 3, 2: 6, 3: 1, 4: 4, 5: 7, 6: 2, 7: 5, 8: 8}
    else:  # nothing - if you want to use it change n = random.randint(0, 3) to n = random.randint(0, 4)
        mirror_operation = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8}

    change_info_v(v, mirror_operation)
    change_info_e(e, mirror_operation)
    left = change_info_answers(left, mirror_operation)
    right = change_info_answers(right, mirror_operation)
    return left, right


def rotate_matrices_in_trial(info, matrix):
    if matrix == "A":
        info["Left_button_targets"][0], info["Right_button_targets"][0] = rotate_matrix(info["Nodes_A"],
        info["Edges_A"], info["Left_button_targets"][0], info["Right_button_targets"][0])
    elif matrix == 'B':
        info["Left_button_targets"][1], info["Right_button_targets"][1] = rotate_matrix(info["Nodes_B"],
        info["Edges_B"], info["Left_button_targets"][1], info["Right_button_targets"][1])


def mirror_matrices_in_trial(info, matrix):
    if matrix == "A":
        info["Left_button_targets"][0], info["Right_button_targets"][0] = mirror_matrix(info["Nodes_A"],
        info["Edges_A"], info["Left_button_targets"][0], info["Right_button_targets"][0])
    elif matrix == "B":
        info["Left_button_targets"][1], info["Right_button_targets"][1] = mirror_matrix(info["Nodes_B"],
        info["Edges_B"], info["Left_button_targets"][1], info["Right_button_targets"][1])
