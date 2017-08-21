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

snake1 = None
snake2 = None
snake_array = None


def random_color():
    r = random.randint(0,255)
    b = random.randint(0,255)
    g = random.randint(0,255)
    color = "#%02x%02x%02x" % (r,b,g)
    return color

class Snake:
    def __init__(self, id, canvas, color,key_press_left, key_press_right, key_press_up, key_press_down, food_array):
        self.id = id
        self.length = 5
        self.canvas = canvas
        self.color = color
        first_piece = canvas.create_rectangle(0, 0, 10, 10, fill=color)
        start_x = random.randint(2,95) * 10
        start_y = random.randint(2,45) * 10
        self.canvas.move(first_piece, start_x, start_y)
        self.body_pieces = [first_piece]
        pos = self.canvas.coords(first_piece)
        self.head = canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill=color)
        self.x_speed = 10
        self.y_speed = 0
        self.died = False
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.food_array = food_array
        self.canvas.bind_all(key_press_left, self.turn_left)
        self.canvas.bind_all(key_press_right, self.turn_right)
        self.canvas.bind_all(key_press_up, self.turn_up)
        self.canvas.bind_all(key_press_down, self.turn_down)
        self.score = 0
        self.score_text = canvas.create_text(id * 200, 0, text="Score: %s" % self.score, font=("Arial", 15), fill=color, anchor="nw")
        
        

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
        new_piece = canvas.create_rectangle(old_pos[0], old_pos[1], old_pos[2], old_pos[3], fill=self.color)
        self.body_pieces.append(new_piece)
        if len(self.body_pieces) > self.length:
            last_piece = self.body_pieces.pop(0)
            canvas.delete(last_piece)
        
        self.canvas.move(self.head, self.x_speed, self.y_speed)
        pos = self.canvas.coords(self.head)
        if pos[1] <= 0:
            self.died = True
        if pos[3] >= self.canvas_height:
            self.died = True
        if pos[0] <= 0:
            self.died = True
        if pos[2] >= self.canvas_width:
            self.died = True
        if self.has_crashed(pos):
            self.died = True
        if self.hit_food(pos):
            self.length = self.length + 4
            self.score = self.score + 1
        self.update_score()

    def has_crashed(self, current_pos):
        global snake_array
        for snake in snake_array:
            for body_part in snake.body_pieces:
                part_pos = self.canvas.coords(body_part)
                if current_pos == part_pos:
                    return True
        return False

    def hit_food(self, current_pos):
        head_pos = self.canvas.coords(self.head)
        for food in self.food_array:
            if food.pos_x == head_pos[0] and food.pos_y == head_pos[1]:
                self.food_array.remove(food)
                canvas.delete(food.shape)
                if len(self.food_array) == 0:
                    self.food_array.append(Food.create_random_location(canvas, self.canvas_width,self.canvas_height))
                return True
        return False

    def convert_to_food(self):
        for body_part in self.body_pieces:
            pos = self.canvas.coords(body_part)
            canvas.delete(body_part)
            self.food_array.append(Food.create_at_location(canvas, self.canvas_width,self.canvas_height,pos[0],pos[1]))
        canvas.delete(self.head)
        canvas.delete(self.score_text)

    def remove(self):
        for food in self.food_array:
            canvas.delete(food.shape)
        for body_part in self.body_pieces:
            canvas.delete(body_part)
        canvas.delete(self.head)
        canvas.delete(self.score_text)

class Food:
    def __init__(self, canvas, width, height, pos_x, pos_y):
        self.canvas = canvas
        self.height = height
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.shape = canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x + 10, self.pos_y + 10, fill="Yellow")

    @classmethod
    def create_at_location(cls, canvas, width, height, pos_x, pos_y):
        return cls(canvas, width, height, pos_x, pos_y)

    @classmethod
    def create_random_location(cls, canvas, width, height):
        (pos_x, pos_y) = Food.get_random_position(canvas, width,height)
        return cls(canvas, width, height, pos_x, pos_y)

    @classmethod 
    def get_random_position(cls,canvas, width, height):
        pos_x = 0
        pos_y = 0
        while True:
            pos_x = round(random.randint(10,width-20),-1)
            pos_y = round(random.randint(10,height-20),-1)
            if not Food.overlaps_snake(canvas, pos_x, pos_y):
                break
        return (pos_x, pos_y)

    @classmethod
    def overlaps_snake(cls, canvas, pos_x, pos_y):
        global snake_array
        if snake_array == None:
            return False
        for snake in snake_array:
            for piece in snake.body_pieces:
                part_pos = canvas.coords(piece)
                if part_pos[0] == pos_x and part_pos[1] == pos_y:
                    return True
        return False

my_text = canvas.create_text(width/2, height/2, text="Press any Enter to start game", font=("Arial", 30), fill="blue")

def begin_new_game(event):
    global canvas, tk, my_text, snake1,snake2,snake_array
    if not my_text == None:
        canvas.delete(my_text)
    if not snake1 == None:
        snake1.remove()
        snake1 = None
    if not snake2 == None:
        snake2.remove()
        snake2 = None
    food_array = [Food.create_random_location(canvas, width,height)]
    snake1 = Snake(0, canvas, "blue","<KeyPress-Left>","<KeyPress-Right>","<KeyPress-Up>","<KeyPress-Down>", food_array)
    snake2 = Snake(1, canvas, "red","<KeyPress-a>","<KeyPress-d>","<KeyPress-w>","<KeyPress-s>", food_array)
    snake_array = [snake1, snake2]
    while not ((snake1.died and snake2.died) or (snake1.score >= 100 or snake2.score >= 100)):
        if snake1.died:
            previous_score = snake1.score
            snake1.convert_to_food()
            snake_array.remove(snake1)
            snake1 = Snake(0, canvas, "blue","<KeyPress-Left>","<KeyPress-Right>","<KeyPress-Up>","<KeyPress-Down>", food_array)
            #snake1.score = previous_score
            new_array = [snake1]
            snake_array = new_array + snake_array
        if snake2.died:
            previous_score = snake2.score
            snake2.convert_to_food()
            snake_array.remove(snake2)
            snake2 = Snake(1, canvas, "red","<KeyPress-a>","<KeyPress-d>","<KeyPress-w>","<KeyPress-s>", food_array)
            #snake2.score = previous_score
            new_array = [snake2]
            snake_array = new_array + snake_array
        for snake in snake_array:
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


  
