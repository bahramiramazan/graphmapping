from tkinter.ttk import Separator
from sources.set_config.tkinter_elements import *
from sources.set_config.utils import *
from sources.set_config.alerts import *


def page_4(info):
    def choose_text_color():
        return choose_button_color(text_button_color, title="Choose text color")

    def choose_background_color():
        return choose_button_color(background_button_color, title="Choose background color")

    def choose_vertices_color():
        return choose_button_color(vertices_button_color, title="Choose nodes color")

    def choose_edges_color():
        return choose_button_color(edges_button_color, title="Choose edges color")

    def add_info_from_config():
        try:
            # Visual
            text_size.insert(0, info["text_size"])
            change_button_color(text_button_color, info["text_color"])
            change_button_color(background_button_color, info["background_color"])
            change_button_color(vertices_button_color, info["vertices_color"])
            change_button_color(edges_button_color, info["edges_color"])
            left_graph_position_x.insert(0, info["left_graph_position"][0])
            left_graph_position_y.insert(0, info["left_graph_position"][1])
            right_graph_position_x.insert(0, info["right_graph_position"][0])
            right_graph_position_y.insert(0, info["right_graph_position"][1])
            vertices_size.insert(0, info["vertices_size"])
            vertices_distance.insert(0, info["vertices_distance"])
            gap_between_edges_and_vertices.insert(0, info["gap_between_edges_and_vertices"])
            arrowhead_length.insert(0, info["arrowhead_length"])
            arrowhead_width.insert(0, info["arrowhead_width"])
        except:
            messagebox.showerror(message="Can't load file with config")
            text_size.focus_force()

    def alerts():
        global information
        # ------------------ Visual ------------------ #
        if not try_button_color(text_button_color, orig_button_background, "text"):
            return None
        if not try_button_color(background_button_color, orig_button_background, "background"):
            return None
        if not try_button_color(vertices_button_color, orig_button_background, "non-target nodes"):
            return None
        txt_size = try_convert_to_int(text_size.get(), "Text size")
        if not try_in_range(txt_size, "Text size", v_min=0):
            return None
        if not try_button_color(edges_button_color, orig_button_background, "edges"):
            return None

        l_graph_position_x = try_convert_to_int(left_graph_position_x.get(), "Left graph x position")
        if l_graph_position_x is None:
            return None
        l_graph_position_y = try_convert_to_int(left_graph_position_y.get(), "Left graph y position")
        if l_graph_position_y is None:
            return None

        r_graph_position_x = try_convert_to_int(right_graph_position_x.get(), "Right graph x position")
        if r_graph_position_x is None:
            return None
        r_graph_position_y = try_convert_to_int(right_graph_position_y.get(), "Right graph y position")
        if r_graph_position_y is None:
            return None

        v_size = try_convert_to_int(vertices_size.get(), "nodes size")
        if not try_in_range(v_size, "nodes size", v_min=0):
            return None

        v_distance = try_convert_to_int(vertices_distance.get(), "Distance between nodes")
        if not try_in_range(v_distance, "Distance between nodes", v_min=0):
            return None

        e_v_gap = try_convert_to_int(gap_between_edges_and_vertices.get(), "Gap between edges and nodes")
        if not try_in_range(e_v_gap, "Gap between edges and nodes", v_min=0):
            return None

        a_length = try_convert_to_int(arrowhead_length.get(), "Arrowhead length")
        if not try_in_range(a_length, "Arrowhead length", v_min=0):
            return None

        a_width = try_convert_to_int(arrowhead_width.get(), "Arrowhead width")
        if not try_in_range(a_width, "Arrowhead width", v_min=0):
            return None

        information = {
            # Visual
            "text_color": text_button_color["background"],
            "background_color": background_button_color["background"],
            "text_size": txt_size,
            "vertices_color": vertices_button_color["background"],
            "edges_color": edges_button_color["background"],
            "left_graph_position": [l_graph_position_x, l_graph_position_y],
            "right_graph_position": [r_graph_position_x, r_graph_position_y],
            "vertices_size": v_size,
            "vertices_distance": v_distance,
            "gap_between_edges_and_vertices": e_v_gap,
            "arrowhead_length": a_length,
            "arrowhead_width": a_width
        }

        window.destroy()

    def go_back():
        global information
        window.destroy()
        information = "go_back"

    global information
    information = None

    window = create_window("Set config", 550, 680)

    # ------------------ Visual ------------------ #
    insert_text(text="Visual", column=0, row=0, sticky="W", win=window, size=14)
    Separator(window, orient='horizontal').place(x=0, y=40, relwidth=1, height=2)

    insert_text(text="Text size (px):", column=0, row=2, columnspan=2, win=window, sticky="W")
    text_size = insert_entry(column=2, row=2, width=5, sticky="E", win=window, columnspan=1)

    insert_text(text="Text color:", column=0, row=3, columnspan=6, win=window, sticky="W")
    text_button_color = insert_button(text="Choose color", column=0, row=3, command=choose_text_color,
                                      size=9, win=window, columnspan=6)

    insert_text(text="Background color:", column=0, row=4, columnspan=6, win=window, sticky="W")
    background_button_color = insert_button(text="Choose color", column=0, row=4, command=choose_background_color,
                                            size=9, win=window, columnspan=6)

    insert_text(text="Non-target nodes color:", column=0, row=5, columnspan=6, win=window, sticky="W")
    vertices_button_color = insert_button(text="Choose color", column=0, row=5, command=choose_vertices_color,
                                          size=9, win=window, columnspan=6)

    insert_text(text="Edges color:", column=0, row=6, columnspan=6, win=window, sticky="W")
    edges_button_color = insert_button(text="Choose color", column=0, row=6, command=choose_edges_color,
                                       size=9, win=window, columnspan=6)

    insert_text(text="x:", column=2, row=9, win=window, sticky="W", columnspan=1)
    left_graph_position_x = insert_entry(column=2, row=9, width=5, sticky="E", win=window, columnspan=1)
    insert_text(text="y:", column=3, row=9, win=window, sticky="W", columnspan=1)
    left_graph_position_y = insert_entry(column=3, row=9, width=5, sticky="E", win=window, columnspan=1)
    insert_text(text="Graph A position:", column=0, row=9, columnspan=6, win=window, sticky="W")

    insert_text(text="x:", column=2, row=10, win=window, sticky="W", columnspan=1)
    right_graph_position_x = insert_entry(column=2, row=10, width=5, sticky="E", win=window, columnspan=1)
    insert_text(text="y:", column=3, row=10, win=window, sticky="W", columnspan=1)
    right_graph_position_y = insert_entry(column=3, row=10, width=5, sticky="E", win=window, columnspan=1)
    insert_text(text="Graph B position:    ", column=0, row=10, columnspan=6, win=window, sticky="W")

    insert_text(text="Nodes size:", column=0, row=11, columnspan=6, win=window, sticky="W")
    vertices_size = insert_entry(column=2, row=11, width=5, sticky="E", win=window, columnspan=1)

    insert_text(text="Distance between nodes:", column=0, row=12, columnspan=6, win=window, sticky="W")
    vertices_distance = insert_entry(column=2, row=12, width=5, sticky="E", win=window, columnspan=1)

    insert_text(text="Gap between edges and nodes:", column=0, row=13, columnspan=6, win=window, sticky="W")
    gap_between_edges_and_vertices = insert_entry(column=2, row=13, width=5, sticky="E", win=window, columnspan=1)

    insert_text(text="Arrowhead length:", column=0, row=14, columnspan=6, win=window, sticky="W")
    arrowhead_length = insert_entry(column=2, row=14, width=5, sticky="E", win=window, columnspan=1)

    insert_text(text="Arrowhead width:", column=0, row=15, columnspan=6, win=window, sticky="W")
    arrowhead_width = insert_entry(column=2, row=15, width=5, sticky="E", win=window, columnspan=1)

    # ------------------ Other ------------------- #

    insert_button(text="    Back    ", column=1, row=30, command=go_back, size=12, win=window, columnspan=1, sticky="E")
    save_button = insert_button(text="    Save    ", column=3, row=30, command=alerts, size=12, win=window,
                                columnspan=1, sticky="W")
    orig_button_background = save_button['background']

    add_info_from_config()

    window.mainloop()
    return information
