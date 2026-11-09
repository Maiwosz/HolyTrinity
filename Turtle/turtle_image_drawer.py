import turtle as t
from typing import Tuple

def draw_1(bitmap):
    homex, homey = t.pos()
    for row in bitmap:
        t.penup()
        t.setpos((homex, homey))
        for i, pixel in enumerate(row, start=0):
            if pixel == 1:
                pass
            else:
                t.setpos(homex + i, homey)
                t.pendown()
                t.forward(1)
                t.penup()
        homey -= 1


def draw_2(bitmap):
    homex, homey = t.pos()
    for row in bitmap:
        t.penup()
        t.setpos((homex, homey))
        for i, pixel in enumerate(row, start=0):
            pd = False
            if pixel == 1:
                pass
            else:
                t.setpos(homex + i, homey)
                if not pd:
                    t.pendown()
                t.forward(1)
                if row[i + 1] == 1:
                    t.penup()
        homey -= 1


def draw_3(bitmap):
    only_flips = []
    for row in bitmap:
        flip_row = []
        cur_pix = 1
        for i, pixel in enumerate(row):
            if pixel != cur_pix:
                cur_pix = pixel
                flip_row.append(i)
        only_flips.append(flip_row)

    homex, homey = t.pos()
    for row in only_flips:
        t.penup()
        t.setpos((homex, homey))
        for i, flip in enumerate(row):
            if i % 2 == 1:
                continue
            else:
                t.setpos(homex + row[i], homey)
                t.pendown()
                if len(row) > i + 1:
                    t.forward(row[i + 1] - row[i])
                else:
                    t.forward(len(bitmap[0]) - row[i])
                t.penup()
        homey -= 1

import numpy as np
from PIL import Image

def convert_to_mono(path: str, size: Tuple[int, int]):
    # TODO 5: Implement a function that reads an image from a file and converts it to a monochrome bitmap. 
    thres = 92
    rows, cols = size
    image = Image.open(path).convert("L").resize((cols, rows))
    gray = np.asarray(image)
    monochrome_table = (gray >= thres).astype(int)
    return monochrome_table

if __name__ == "__main__":
    t.speed("fastest")
    t.penup()
    t.setpos(-400, 400)
    table = convert_to_mono("avatar.jpg", (292, 293))
    
    function_to_use = 2
    functions = {0: draw_1, 1: draw_2, 2: draw_3}
    functions[function_to_use](table)
    input()
