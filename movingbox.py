from tkinter import *
import time

tk = Tk()
tk.title("Snake game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost",1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

class Snake:
    def __init__(self, canvas, color,key_press_left, key_press_right):
        self.canvas = canvas
        self.id = canvas.create_rectangle(10, 10, 20, 20, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.x_speed = 1
        self.y_speed = 0
        self.hit_wall = False
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all(key_press_left, self.turn_left)
        self.canvas.bind_all(key_press_right, self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x_speed, self.y_speed)
        pos = self.canvas.coords(self.id)                                                                                                                         
        if pos[1] <= 0:
            self.hit_wall = True
        if pos[3] >= self.canvas_height:
            self.hit_wall = True
        if pos[0] <= 0:
            self.hit_wall = True
        if pos[2] >= self.canvas_width:
            self.hit_wall = True

    def turn_left(self, event):
        if self.x_speed == 1:
            self.x_speed = 0
            self.y_speed = -1
        elif self.x_speed == -1:
            self.x_speed = 0
            self.y_speed = 1
        elif self.y_speed == 1:
            self.x_speed = 1
            self.y_speed = 0
        elif self.y_speed == -1:
            self.x_speed = -1
            self.y_speed = 0

    def turn_right(self,event):
        if self.x_speed == 1:
            self.x_speed = 0
            self.y_speed = 1
        elif self.x_speed == -1:
            self.x_speed = 0
            self.y_speed = -1
        elif self.y_speed == 1:
            self.x_speed = -1
            self.y_speed = 0
        elif self.y_speed == -1:
            self.x_speed = -1
            self.y_speed = 0

snake = Snake(canvas, "blue","<KeyPress-Left>","<KeyPress-Right>")

while True:
    if not snake.hit_wall:
        snake.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
  
