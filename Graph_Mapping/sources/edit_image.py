from os.path import join
from PIL import Image


def change_color(im, convert_colors):
    width, height = im.size
    pix = im.load()
    for [old_color, new_color] in convert_colors:
        print(old_color, new_color)
        for x in range(0, width):
            for y in range(0, height):
                if pix[x, y] == old_color:
                    im.putpixel((x, y), new_color)


def convert_mouse_colors(left_color, right_color, file_path='images', file_name='mouse_info.png', file_new_name='mouse_info_2.png'):
    if left_color[0] == "#":
        left_color = tuple([int(left_color[i:i+2], 16) for i in (1, 3, 5)] + [255])
    if right_color[0] == "#":
        right_color = tuple([int(right_color[i:i+2], 16) for i in (1, 3, 5)] + [255])

    im = Image.open(join(file_path, file_name))
    im = im.convert("RGBA")
    change_color(im, convert_colors=[[(1, 255, 0, 255), left_color], [(0, 0, 255, 255), right_color]])
    im.save(join(file_path, file_new_name))

