import sys
import tkinter as tk
from tkinter import messagebox
from typing import List


class Racket:
    def __init__(self, x):
        self.x = x

    def update(self, key_press_r, key_press_l):
        if key_press_r and self.x <= 350:
            self.x += 5
        if key_press_l and self.x >= -10:
            self.x -= 5

    @property
    def shape_parameters(self):
        return self.x, 580, self.x + 60, 595


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
        if self.y >= 560 and racket.x - 10 <= self.x <= racket.x + 50:
            self.vy *= -1
        self.x += self.vx
        self.y += self.vy

    @property
    def shape_parameters(self):
        return self.x, self.y, self.x + 20, self.y + 20


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_broken = False

    def update(self, ball: Ball):
        if ball.y <= self.y + 30 and self.x - 10 <= ball.x <= self.x + 60 and not self.is_broken:
            ball.vy *= -1
            self.is_broken = True

    @property
    def shape_parameters(self):
        return self.x, self.y, self.x + 70, self.y + 30


class Blocks:
    def __init__(self, blocks: List[Block]):
        assert hasattr(blocks, '__iter__')
        for i in blocks:
            assert isinstance(i, Block)
        self._blocks = blocks

    def __iter__(self):
        for i in self._blocks:
            yield i

    def update(self, ball: Ball):
        for block in self._blocks:
            block.update(ball)

    def all_broken(self):
        broken_flag = [i.is_broken for i in self._blocks]
        return all(broken_flag)


class GameBoard:
    def __init__(self, racket: Racket, ball: Ball, blocks: Blocks):
        self.racket = racket
        self.ball = ball
        self.blocks = blocks

    def is_clear(self):
        return self.blocks.all_broken()

    def is_game_over(self):
        return self.ball.y >= 603

    def update(self, key_press_r, key_press_l):
        self.ball.update(self.racket)
        self.racket.update(key_press_r, key_press_l)
        self.blocks.update(self.ball)

    @staticmethod
    def game_over():
        messagebox.showinfo('Information', 'Game over!')
        exit()

    @staticmethod
    def game_clear():
        messagebox.showinfo('Information', 'Game Clear!')
        sys.exit()


class Application:
    def __init__(self):
        win = tk.Tk()
        win.title('breakout')
        win.geometry('425x625')
        win.resizable(False, False)

        win.bind('<KeyPress-Right>', self.right_key_press)
        win.bind('<KeyRelease-Right>', self.right_key_release)
        win.bind('<KeyPress-Left>', self.left_key_press)
        win.bind('<KeyRelease-Left>', self.left_key_release)

        can = tk.Canvas(bg='black', width=400, height=600)
        can.place(x=10, y=10)

        self.win = win
        self.can = can

        self.key_press_r = False
        self.key_press_l = False

        self.board = GameBoard(
            Racket(170),
            Ball(x=50, y=500, vx=5, vy=-5),
            Blocks([Block(80 * xx + 5, 40 * yy + 10) for xx in range(5) for yy in range(4)])
        )

    def right_key_press(self, _):
        self.key_press_r = True

    def right_key_release(self, _):
        self.key_press_r = False

    def left_key_press(self, _):
        self.key_press_l = True

    def left_key_release(self, _):
        self.key_press_l = False

    def loop(self):
        self.can.delete('all')
        self.board.update(self.key_press_r, self.key_press_l)
        self.draw_racket()
        self.draw_ball()
        self.draw_blocks()

        if self.board.is_game_over():
            self.board.game_over()
        if self.board.is_clear():
            self.board.game_clear()
        self.win.after(15, self.loop)

    def run(self):
        self.loop()
        self.win.mainloop()

    def draw_racket(self):
        parameters = self.board.racket.shape_parameters
        self.can.create_rectangle(*parameters, fill='white')

    def draw_ball(self):
        parameters = self.board.ball.shape_parameters
        self.can.create_oval(*parameters, fill='white')

    def draw_blocks(self):
        for block in self.board.blocks:
            if not block.is_broken:
                parameter = block.shape_parameters
                self.can.create_rectangle(*parameter, fill='white')


def main():
    application = Application()
    application.run()


if __name__ == '__main__':
    main()
