import tkinter as tk
from tkinter import messagebox

win = tk.Tk()
win.title('breakout')
win.geometry('425x625')
win.resizable(False, False)

can = tk.Canvas(bg='black', width=400, height=600)
can.place(x=10, y=10)

ball_x, ball_y = 50, 500
bx, by = 5, -5


def game_over():
    messagebox.showinfo('Information', 'Game over!')
    exit()


def game_clear():
    messagebox.showinfo('Information', 'Game over!')


def draw_ball():
    global ball_x, ball_y, bx, by
    can.create_oval(ball_x, ball_y, ball_x + 20, ball_y + 20, fill='white')

    if ball_x <= 0 or ball_x >= 385:
        bx *= -1
    if ball_y <= 0:
        by *= -1
    if ball_y >= 603:
        game_over()
    if ball_y >= 560 and ball_x >= rack_x - 10 and ball_x <= rack_x + 50:
        by *= -1
    ball_x += bx
    ball_y += by


rack_x = 170
key_press_r = False
key_press_l = False


def right_key_press(event):
    global key_press_r
    key_press_r = True


def right_key_release(event):
    global key_press_r
    key_press_r = False


def left_key_press(event):
    global key_press_l
    key_press_l = True


def left_key_release(event):
    global key_press_l
    key_press_l = False


win.bind('<KeyPress-Right>', right_key_press)
win.bind('<KeyRelease-Right>', right_key_release)
win.bind('<KeyPress-Left>', left_key_press)
win.bind('<KeyRelease-Left>', left_key_release)


def draw_racket():
    global rack_x
    can.create_rectangle(rack_x, 580, rack_x + 60, 595, fill='white')
    if key_press_r and rack_x <= 350:
        rack_x += 5
    if key_press_l and rack_x >= -10:
        rack_x -= 5


block = []
for x_ in range(5):
    for y_ in range(4):
        block.append({'x': x_ * 80 + 5, 'y': y_ * 40 + 10, 'st': 1})


def draw_block():
    global ball_x, ball_y, by
    block_count = 0
    for i in range(len(block)):
        x = block[i]['x']
        y = block[i]['y']
        st = block[i]['st']
        if ball_y <= y + 30 and x - 10 <= ball_x <= x + 60 and st == 1:
            by *= -1
            block[i]['st'] = 0
        if st == 1:
            can.create_rectangle(x, y, x + 70, y + 30, fill='white')
            block_count += 1
    if block_count == 0:
        game_clear()


def game_loop():
    can.delete('all')
    draw_ball()
    draw_racket()
    draw_block()
    win.after(15, game_loop)


game_loop()

win.mainloop()
