from tkinter import *
import time

tk = Tk()
tk.title("Chad's game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost",1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

class Ball:
    def __init__(self, canvas, bottom_paddle, top_paddle, color):
        self.canvas = canvas
        self.bottom_paddle = bottom_paddle
        self.top_paddle = top_paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.speed = 1
        self.x = self.speed
        self.y = -self.speed
        self.hit_bottom = False
        self.hit_top = False
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)                                                                                                                         
        if pos[1] <= 0:
            self.hit_top = True
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if pos[0] <= 0:
            self.x = self.speed
        if pos[2] >= self.canvas_width:
            self.x = -self.speed
        if self.hit_paddle(pos,self.bottom_paddle) == True:
            self.y = -self.speed
        if self.hit_paddle(pos,self.top_paddle) == True:
            self.y = self.speed
			
    def hit_paddle(self, pos, paddle):
        paddle_pos = self.canvas.coords(paddle.id)
        # if the ball is between the edges of the paddle...
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            # if the bottom of the ball is between top and bottom of the paddle...
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.speed = self.speed + .25
                return True
        return False


class Paddle:
    def __init__(self, position, canvas, color, key_press_left, key_press_right):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, position)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all(key_press_left, self.turn_left)
        self.canvas.bind_all(key_press_right, self.turn_right)

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

bottom_paddle = Paddle(375,canvas, 'green','<KeyPress-Left>','<KeyPress-Right>')
top_paddle = Paddle(30,canvas, 'blue','<KeyPress-1>','<KeyPress-2>')

ball = Ball(canvas, bottom_paddle, top_paddle, 'red')

while True:
    if not (ball.hit_bottom or ball.hit_top):
        ball.draw()
        top_paddle.draw()
        bottom_paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
