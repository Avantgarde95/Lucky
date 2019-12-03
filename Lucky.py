# -*- coding: utf-8 -*-

import sys
import math
import time
import random

PY_VERSION = sys.version_info[0]

if PY_VERSION == 2:
    import Tkinter as tk
    import tkMessageBox as msgbox
elif PY_VERSION == 3:
    import tkinter as tk
    import tkinter.messagebox as msgbox
else:
    print('Unsupported python version: %d!' % PY_VERSION)
    sys.exit(1)

RADIUS_BOARD = 150
MARGIN_BOARD = 30
NUM_CHOICES = 6 # |lucky| = |unlucky| = NUM_CHOICES / 2

STRING_MAP = {
    'title': u'오늘의 운세!',
    'run': u'ㄱㄱ',
    'lucky': u'당첨!',
    'unlucky': u'꽝!',
    'result': u'결과',
    'lucky_message': u'당첨입니다! 오늘의 운세가 좋으시군요!',
    'unlucky_message': u'꽝입니다 ㅠㅠ 오늘의 운세가 개판이시군요...'
}

class App(tk.Frame, object):
    def __init__(self, root=None):
        self.root = root
        super(App, self).__init__(self.root)

        # canvas_board
        size_canvas = RADIUS_BOARD * 2 + MARGIN_BOARD * 2

        self.canvas_board = tk.Canvas(
                self,
                width=size_canvas,
                height=size_canvas,
                bg='white',
                highlightthickness=0
        )

        self.canvas_board.pack()

        # button_run
        self.button_run = tk.Button(
                self,
                text=STRING_MAP['run'],
                width=8,
                command=self.cb_run
        )

        self.button_run.pack(pady=5)

        # canvas_board - circle_board
        circle_start = MARGIN_BOARD
        circle_end = RADIUS_BOARD * 2 + MARGIN_BOARD
        color_circle = 'orange'

        self.circle_board = self.canvas_board.create_oval(
                circle_start, circle_start, circle_end, circle_end,
                fill=color_circle,
                outline=color_circle
        )

        # canvas_board - lines_board, texts_board
        angle = math.pi * 2 / float(NUM_CHOICES)
        line_start = RADIUS_BOARD + MARGIN_BOARD
        line_radius = RADIUS_BOARD
        text_radius = RADIUS_BOARD * 0.6
        self.lines_board = []
        self.texts_board = []

        for i in range(NUM_CHOICES):
            # lines_board
            line_cos = math.cos(angle * i)
            line_sin = math.sin(angle * i)
            line_end_x = line_start + line_radius * line_cos
            line_end_y = line_start + line_radius * line_sin

            line = self.canvas_board.create_line(
                    line_start, line_start,
                    line_end_x, line_end_y,
                    width=3,
                    fill='blue'
            )

            self.lines_board.append(line)

            # texts_board
            text_cos = math.cos(angle * (i + 0.5))
            text_sin = math.sin(angle * (i + 0.5))
            text_x = line_start + text_radius * text_cos
            text_y = line_start + text_radius * text_sin
            text_label = STRING_MAP['lucky'] if i % 2 == 0 else STRING_MAP['unlucky']
            text_color = 'brown' if i % 2 == 0 else 'dark green'

            text = self.canvas_board.create_text(
                    text_x, text_y,
                    text=text_label,
                    fill=text_color,
                    font=('', 14, 'bold')
            )

            self.texts_board.append(text)

        # canvas_board - needle_board
        self.angle_curr = -math.pi / 2
        self.needle_board = None
        self.update_needle()

        # animation flag
        self.dur_run = 0
        self.flag_run = False
        self.time_run = 0

    def update_needle(self):
        # erase
        self.canvas_board.delete(self.needle_board)

        # draw
        needle_radius = RADIUS_BOARD * 0.8
        needle_start = RADIUS_BOARD + MARGIN_BOARD
        needle_cos = math.cos(self.angle_curr)
        needle_sin = math.sin(self.angle_curr)
        needle_end_x = needle_start + needle_radius * needle_cos
        needle_end_y = needle_start + needle_radius * needle_sin

        self.needle_board = self.canvas_board.create_line(
                needle_start, needle_start,
                needle_end_x, needle_end_y,
                width=6,
                fill='red'
        )

    def incr_angle(self):
        self.angle_curr += 1

        if self.angle_curr > math.pi * 2:
            self.angle_curr -= math.pi * 2

        if self.angle_curr < 0:
            self.angle_curr += math.pi * 2

    def show_msg(self):
        check = int(self.angle_curr / (math.pi * 2 / NUM_CHOICES))

        if check % 2 == 0:
            msgbox.showinfo(
                    STRING_MAP['result'],
                    STRING_MAP['lucky_message']
            )
        else:
            msgbox.showwarning(
                    STRING_MAP['result'],
                    STRING_MAP['unlucky_message']
            )

    def cb_rotate(self):
        if time.time() - self.time_run <= self.dur_run:
            self.incr_angle()
            self.update_needle()
            self.root.after(30, self.cb_rotate)
        else:
            self.show_msg()
            self.flag_run = False

    def cb_run(self):
        if not self.flag_run:
            self.flag_run = True
            self.angle_curr = -math.pi / 2
            self.dur_run = random.uniform(2, 4)
            self.time_run = time.time()
            self.cb_rotate()

if __name__ == '__main__':
    root = tk.Tk()
    root.title(STRING_MAP['title'])
    app = App(root)
    app.pack()
    root.mainloop()

