from tkinter import *
import time
import random

tk = Tk()
tk.title("Snake game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost",1)
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

def random_color():
    r = random.randint(0,255)
    b = random.randint(0,255)
    g = random.randint(0,255)
    color = "#%02x%02x%02x" % (r,b,g)
    return color

class Snake:
    def __init__(self, canvas, color, key_press_left, key_press_right):
        self.canvas = canvas
        start_x = random.randint(2,30) * 10
        start_y = random.randint(2,30) * 10
        first_piece = canvas.create_rectangle(0,0,10,10,fill=random_color())
        self.canvas.move(first_piece, start_x, start_y)
        self.x_speed = 10
        self.y_speed = 0
        pos = self.canvas.coords(first_piece)
        self.head = canvas.create_rectangle(pos[0],pos[1],pos[2],pos[3],fill=color)
        self.canvas.bind_all(key_press_left, self.turn_left)
        self.canvas.bind_all(key_press_right, self.turn_right)

    def turn_left(self, event):
        if self.x_speed == 10:
            self.x_speed = 0
            self.y_speed = -10
        elif self.y_speed == -10:
            self.x_speed = -10
            self.y_speed = 0
        elif self.x_speed == -10:
            self.x_speed = 0
            self.y_speed = 10
        elif self.y_speed == 10:
            self.x_speed = 10
            self.y_speed = 0
            
    def turn_right(self,event):
        if self.x_speed == 10:
            self.x_speed = 0
            self.y_speed = 10
        elif self.x_speed == -10:
            self.x_speed = 0
            self.y_speed = -10
        elif self.y_speed == 10:
            self.x_speed = -10
            self.y_speed = 0
        elif self.y_speed == -10:
            self.x_speed = 10
            self.y_speed = 0

    def draw(self):
        old_pos = self.canvas.coords(self.head)
        new_piece = canvas.create_rectangle(old_pos[0],old_pos[1],old_pos[2],
                                            old_pos[3], fill=random_color())
        self.canvas.move(self.head, self.x_speed, self.y_speed)
        
snake = Snake(canvas, "blue", "<KeyPress-Left>", "<KeyPress-Right>")

while True:
    snake.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.05)
