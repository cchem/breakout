import sys
import tkinter as tk
from tkinter import messagebox
from typing import List

win = tk.Tk()
win.title('breakout')
win.geometry('425x625')
win.resizable(False, False)

can = tk.Canvas(bg='black', width=400, height=600)
can.place(x=10, y=10)


def game_over():
    messagebox.showinfo('Information', 'Game over!')
    exit()


def game_clear():
    messagebox.showinfo('Information', 'Game Clear!')
    sys.exit()


key_press_r = False
key_press_l = False


def right_key_press(_):
    global key_press_r
    key_press_r = True


def right_key_release(_):
    global key_press_r
    key_press_r = False


def left_key_press(_):
    global key_press_l
    key_press_l = True


def left_key_release(_):
    global key_press_l
    key_press_l = False


win.bind('<KeyPress-Right>', right_key_press)
win.bind('<KeyRelease-Right>', right_key_release)
win.bind('<KeyPress-Left>', left_key_press)
win.bind('<KeyRelease-Left>', left_key_release)


class Racket:
    def __init__(self, x):
        self.x = x

    def update(self):
        if key_press_r and self.x <= 350:
            self.x += 5
        if key_press_l and self.x >= -10:
            self.x -= 5

    def draw(self):
        can.create_rectangle(self.x, 580, self.x + 60, 595, fill='white')


class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self, racket: Racket):
        if self.x <= 0 or 385 <= self.x:
            self.vx *= -1
        if self.y <= 0:
            self.vy *= -1
        if self.y >= 603:
            game_over()
        if self.y >= 560 and racket.x - 10 <= self.x <= racket.x + 50:
            self.vy *= -1
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        can.create_oval(self.x, self.y, self.x + 20, self.y + 20, fill='white')


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_broken = False

    def update(self, ball: Ball):
        if ball.y <= self.y + 30 and self.x - 10 <= ball.x <= self.x + 60 and not self.is_broken:
            ball.vy *= -1
            self.is_broken = True

    def draw(self):
        if not self.is_broken:
            can.create_rectangle(self.x, self.y, self.x + 70, self.y + 30, fill='white')


class Blocks:
    def __init__(self, blocks: List[Block]):
        assert hasattr(blocks, '__iter__')
        for i in blocks:
            assert isinstance(i, Block)
        self.blocks = blocks

    def update(self, ball: Ball):
        for block in self.blocks:
            block.update(ball)

    def draw(self):
        for block in self.blocks:
            block.draw()

    def all_broken(self):
        broken_flag = [i.is_broken for i in self.blocks]
        return all(broken_flag)


class GameBoard:
    def __init__(self, racket: Racket, ball: Ball, blocks: Blocks):
        self.racket = racket
        self.ball = ball
        self.blocks = blocks

    def is_clear(self):
        return self.blocks.all_broken()

    def loop(self):
        can.delete('all')
        self.ball.update(self.racket)
        self.racket.update()

        self.ball.draw()
        self.racket.draw()

        self.blocks.update(self.ball)
        self.blocks.draw()
        if self.is_clear():
            game_clear()
        win.after(15, self.loop)


game_board = GameBoard(
    Racket(170),
    Ball(x=50, y=500, vx=5, vy=-5),
    Blocks([Block(80 * xx + 5, 40 * yy + 10) for xx in range(5) for yy in range(4)])
)
game_board.loop()

win.mainloop()
