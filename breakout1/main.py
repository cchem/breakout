import sys
import tkinter as tk
from tkinter import messagebox

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


blocks = [Block(80 * xx + 5, 40 * yy + 10) for xx in range(5) for yy in range(4)]


def draw_block(ball):
    block_count = 0
    for block in blocks:
        if ball.y <= block.y + 30 and block.x - 10 <= ball.x <= block.x + 60 and not block.is_broken:
            ball.vy *= -1
            block.is_broken = True
        if not block.is_broken:
            can.create_rectangle(block.x, block.y, block.x + 70, block.y + 30, fill='white')
            block_count += 1
    if block_count == 0:
        game_clear()


class GameBoard:
    def __init__(self, racket, ball):
        self.racket = racket
        self.ball = ball

    def loop(self):
        can.delete('all')
        self.ball.update(self.racket)
        self.racket.update()

        self.ball.draw()
        self.racket.draw()
        draw_block(self.ball)
        win.after(15, self.loop)


game_board = GameBoard(Racket(170), Ball(x=50, y=500, vx=5, vy=-5))
game_board.loop()

win.mainloop()
