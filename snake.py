from tkinter import *
import time
import random

tk = Tk()
tk.title("Snake game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost",1)
height = 500
width = 1000
canvas = Canvas(tk, width=width, height=height, bd=0, highlightthickness=0, bg="black")
canvas.pack()
tk.update()

def random_color():
    r = random.randint(0,255)
    b = random.randint(0,255)
    g = random.randint(0,255)
    color = "#%02x%02x%02x" % (r,b,g)
    return color

class Snake:
    def __init__(self, canvas, color,key_press_left, key_press_right, key_press_up, key_press_down):
        self.length = 5
        self.canvas = canvas
        first_piece = canvas.create_rectangle(0, 0, 10, 10, fill=random_color())
        start_x = random.randint(2,30) * 10
        start_y = random.randint(2,30) * 10
        self.canvas.move(first_piece, start_x, start_y)
        self.body_pieces = [first_piece]
        pos = self.canvas.coords(first_piece)
        self.head = canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill=color)
        self.x_speed = 10
        self.y_speed = 0
        self.hit_wall = False
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.food_array = [Food(canvas, self, self.canvas_width,self.canvas_height)]
        self.canvas.bind_all(key_press_left, self.turn_left)
        self.canvas.bind_all(key_press_right, self.turn_right)
        self.canvas.bind_all(key_press_up, self.turn_up)
        self.canvas.bind_all(key_press_down, self.turn_down)
        self.score = 0
        self.score_text = canvas.create_text(0, 0, text="Score: %s" % self.score, font=("Arial", 15), fill="blue", anchor="nw")
        
        

    def update_score(self):
        canvas.itemconfigure(self.score_text, text="Score: %s" % self.score)


    def turn_left(self, event):
        if not self.x_speed == 10:
            self.x_speed = -10
            self.y_speed = 0

    def turn_right(self,event):
        if not self.x_speed == -10:
            self.x_speed = 10
            self.y_speed = 0
            
    def turn_up(self, event):
        if not self.y_speed == 10:
            self.x_speed = 0
            self.y_speed = -10

    def turn_down(self, event):
        if not self.y_speed == -10:
            self.x_speed = 0
            self.y_speed = 10

    def draw(self):
        old_pos = self.canvas.coords(self.head)
        new_piece = canvas.create_rectangle(old_pos[0], old_pos[1], old_pos[2], old_pos[3], fill=random_color())
        self.body_pieces.append(new_piece)
        if len(self.body_pieces) > self.length:
            last_piece = self.body_pieces.pop(0)
            canvas.delete(last_piece)
        
        self.canvas.move(self.head, self.x_speed, self.y_speed)
        pos = self.canvas.coords(self.head)
        if pos[1] <= 0:
            self.hit_wall = True
        if pos[3] >= self.canvas_height:
            self.hit_wall = True
        if pos[0] <= 0:
            self.hit_wall = True
        if pos[2] >= self.canvas_width:
            self.hit_wall = True
        if self.has_crashed(pos):
            self.hit_wall = True
            print("Crashed")
        if self.hit_food(pos):
            self.length = self.length + 10
            eaten_food = self.food_array.pop()
            canvas.delete(eaten_food.shape)
            self.food_array.append(Food(canvas, self, self.canvas_width,self.canvas_height))
            self.score = self.score + 1
        self.update_score()

    def has_crashed(self, current_pos):
        for body_part in self.body_pieces:
            part_pos = self.canvas.coords(body_part)
            if current_pos == part_pos:
                return True
        return False

    def hit_food(self, current_pos):
        head_pos = self.canvas.coords(self.head)
        for food in self.food_array:
            if food.pos_x == head_pos[0] and food.pos_y == head_pos[1]:
                return True
        return False

    def remove(self):
        for food in self.food_array:
            canvas.delete(food.shape)
        for body_part in self.body_pieces:
            canvas.delete(body_part)
        canvas.delete(self.head)
        canvas.delete(self.score_text)

class Food:
    def __init__(self, canvas, snake, width, height):
        self.canvas = canvas
        self.height = height
        self.width = width
        (self.pos_x, self.pos_y) = self.get_random_position(snake)
        self.shape = canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x + 10, self.pos_y + 10, fill=random_color())
        

    def get_random_position(self, snake):
        pos_x = 0
        pos_y = 0
        while True:
            pos_x = round(random.randint(10,self.width-20),-1)
            pos_y = round(random.randint(10,self.height-20),-1)
            if not self.overlaps_snake(pos_x, pos_y, snake):
                break
        return (pos_x, pos_y)

    def overlaps_snake(self, pos_x, pos_y, snake):
        for piece in snake.body_pieces:
            part_pos = self.canvas.coords(piece)
            if part_pos[0] == pos_x and part_pos[1] == pos_y:
                return True
        return False

my_text = canvas.create_text(width/2, height/2, text="Press any Enter to start game", font=("Arial", 30), fill="blue")
snake = None
def begin_new_game(event):
    global canvas, tk, my_text, snake
    if not my_text == None:
        canvas.delete(my_text)
    if not snake == None:
        snake.remove()
    snake = Snake(canvas, "blue","<KeyPress-Left>","<KeyPress-Right>","<KeyPress-Up>","<KeyPress-Down>")
    while not snake.hit_wall:
        snake.draw()
        tk.update_idletasks()
        tk.update()
        time.sleep(0.05)
    my_text = canvas.create_text(width/2, height/2, text="Press any Enter to start game", font=("Arial", 30), fill="blue")
    
canvas.bind_all("<KeyPress-Return>", begin_new_game)
while True:
    tk.update_idletasks()
    tk.update()
    time.sleep(0.05)


  
