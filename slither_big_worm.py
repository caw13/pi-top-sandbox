from tkinter import *
import time
import random


height = 600
width = 1200
dialog = Tk()
tk = None
canvas = None
players_label = Label(dialog, text="How many players, 2 or 3: ")
players_label.pack()
players_entry = Entry(dialog)
players_entry.pack()
players_entry.insert(0,"2")
num_players = 2


snake1 = None
snake2 = None
snake3 = None
snake_array = None


def random_color():
    r = random.randint(0,255)
    b = random.randint(0,255)
    g = random.randint(0,255)
    color = "#%02x%02x%02x" % (r,b,g)
    return color

class Body_segment:
    def __init__(self, canvas, piece_array):
        self.canvas = canvas
        self.piece_array = piece_array

    def copy(self, color):
        new_piece_array = None
        for piece in self.piece_array:
            pos = self.canvas.coords(piece)
            new_piece = canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill=color)
            if new_piece_array == None:
                new_piece_array = [new_piece]
            else:
                new_piece_array.append(new_piece)
        return Body_segment(self.canvas, new_piece_array)

    def move(self, dist_x, dist_y):
        for piece in self.piece_array:
            self.canvas.move(piece, dist_x, dist_y)

    def size(self):
        return len(self.piece_array)

    def append(self, body_piece):
        self.piece_array.append(body_piece)

    def grow(self,color):
        pos = self.get_coords()
        cur_size = int((pos[2]-pos[0])/10)
        for i in range(1,cur_size+2):
            new_piece = canvas.create_rectangle(pos[2], pos[1]+((i-1)*10), pos[2]+10, pos[1]+(i*10), fill=color)
            new_pos = self.canvas.coords(new_piece)
            self.append(new_piece)
        for j in range(1,cur_size+1):
            new_piece = canvas.create_rectangle(pos[0]+((j-1)*10), pos[3], pos[0]+(j*10), pos[3]+10, fill=color)
            new_pos = self.canvas.coords(new_piece)
            self.append(new_piece)
            
    def get_coords(self):
        min_x0 = self.canvas.winfo_width()+1
        min_y0 = self.canvas.winfo_height()+1
        max_x1 = -1
        max_y1 = -1
        for piece in self.piece_array:
            pos = self.canvas.coords(piece)
            if pos[0] < min_x0:
                min_x0 = pos[0]
            if pos[1] < min_y0:
                min_y0 = pos[1]
            if pos[2] > max_x1:
                max_x1 = pos[2]
            if pos[3] > max_y1:
                max_y1 = pos[3]
        return (min_x0, min_y0, max_x1, max_y1)

    def remove(self):
        for piece in self.piece_array:
            self.canvas.delete(piece)
            
    def touching_food(self, food_array):
        num_food = 0
        for piece in self.piece_array:
            head_pos = self.canvas.coords(piece)
            for food in food_array:
                if food.pos_x == head_pos[0] and food.pos_y == head_pos[1]:
                    food_array.remove(food)
                    canvas.delete(food.shape)
                    num_food = num_food + 1
                    if len(food_array) == 0:
                        food_array.append(Food.create_random_location(canvas, self.canvas.winfo_width(),self.canvas.winfo_height()))
    
        return num_food
                
    def convert_to_food(self, food_array):
        for piece in self.piece_array:
            pos = self.canvas.coords(piece)
            self.canvas.delete(piece)
            food_array.append(Food.create_at_location(canvas, self.canvas.winfo_width(),self.canvas.winfo_height(),pos[0],pos[1]))

class Snake:
    def __init__(self, id, canvas, color,key_press_left, key_press_right, key_press_up, key_press_down, food_array):
        self.tick = 0
        self.id = id
        self.width = 1
        self.length = 10
        self.canvas = canvas
        self.color = color
        first_piece = canvas.create_rectangle(0, 0, 10, 10, fill=color)
        start_x = random.randint(2,95) * 10
        start_y = random.randint(2,45) * 10
        self.canvas.move(first_piece, start_x, start_y)
        self.body_pieces = [Body_segment(self.canvas,[first_piece])]
        pos = self.canvas.coords(first_piece)
        head_piece = canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill=color)
        self.head = Body_segment(self.canvas,[head_piece])
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
        self.tick = self.tick + 1
        speed_govenor = int(self.width *1.5)
        if (self.tick % speed_govenor)==0:
            old_pos = self.head.get_coords()
            new_piece = self.head.copy(self.color)
            self.body_pieces.append(new_piece)
            if len(self.body_pieces) > self.length:
                last_piece = self.body_pieces.pop(0)
                last_piece.remove()
            
            self.head.move(self.x_speed*self.width, self.y_speed*self.width)
            #self.head.move(self.x_speed, self.y_speed)
            pos = self.head.get_coords()
            if pos[1] < 0:
                self.died = True
            if pos[3] > self.canvas_height:
                self.died = True
            if pos[0] < 0:
                self.died = True
            if pos[2] > self.canvas_width:
                self.died = True
            if self.has_crashed():
                self.died = True
            num_food_touching = self.head.touching_food(self.food_array)
            if num_food_touching:
                self.length = self.length + num_food_touching
                self.score = self.score + num_food_touching
                if (self.score % 20) == 0:
                    self.width = self.width + 1
                    self.head.grow(self.color)
            self.update_score()

    def has_crashed(self):
        global snake_array
        head_pos_array = []
        for head_part in self.head.piece_array:
            head_pos_array.append(self.canvas.coords(head_part))
        for snake in snake_array:
            for body_segment in snake.body_pieces:
                for body_part in body_segment.piece_array:
                    body_part_pos = self.canvas.coords(body_part)
                    for head_pos in head_pos_array:
                        if body_part_pos == head_pos:
                            return True
        return False

##    def hit_food(self, current_pos):
##        head_pos = self.canvas.coords(self.head)
##        for head_piece in self.head.
##        for food in self.food_array:
##            if food.pos_x == head_pos[0] and food.pos_y == head_pos[1]:
##                self.food_array.remove(food)
##                canvas.delete(food.shape)
##                if len(self.food_array) == 0:
##                    self.food_array.append(Food.create_random_location(canvas, self.canvas_width,self.canvas_height))
##                return True
##        return False

    def convert_to_food(self):
        for body_part in self.body_pieces:
            body_part.convert_to_food(self.food_array)
        self.head.remove()
        canvas.delete(self.score_text)

    def remove(self):
        for food in self.food_array:
            canvas.delete(food.shape)
        for body_part in self.body_pieces:
            body_part.remove()
        self.head.remove()
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
                part_pos = piece.get_coords()
                if part_pos[0] == pos_x and part_pos[1] == pos_y:
                    return True
        return False

new_game_text = "Press any Enter to start game\nThe arrow keys control one snake\nThe 'a', 's', 'd', and 'w' keys control the 2nd\nThe 'g', 'h', 'j', and 'y' keys control the 3rd"
my_text = None

def begin_new_game(event):
    global canvas, tk, my_text, snake1,snake2,snake3,snake_array,new_game_text
    if not my_text == None:
        canvas.delete(my_text)
    if not snake1 == None:
        snake1.remove()
        snake1 = None
    if not snake2 == None:
        snake2.remove()
        snake2 = None
    if not snake3 == None:
        snake3.remove()
        snake3 = None

    snake_array = None
    food_array = [Food.create_random_location(canvas, width,height)]
    snake1 = Snake(0, canvas, "blue","<KeyPress-Left>","<KeyPress-Right>","<KeyPress-Up>","<KeyPress-Down>", food_array)
    snake2 = Snake(1, canvas, "red","<KeyPress-a>","<KeyPress-d>","<KeyPress-w>","<KeyPress-s>", food_array)
    if num_players == 3:
        snake3 = Snake(3, canvas, "green","<KeyPress-g>","<KeyPress-j>","<KeyPress-y>","<KeyPress-h>", food_array)
        snake_array = [snake1, snake2,snake3]
    else:
        snake_array = [snake1, snake2]
    while not (snake1.score >= 200 or snake2.score >= 200 or ((not snake3 == None) and (snake3.score>=200))):
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
        if (not snake3 == None) and snake3.died:
            previous_score = snake3.score
            snake3.convert_to_food()
            snake_array.remove(snake3)
            snake3 = Snake(3, canvas, "green","<KeyPress-g>","<KeyPress-j>","<KeyPress-y>","<KeyPress-h>", food_array)
            #snake3.score = previous_score
            new_array = [snake3]
            snake_array = new_array + snake_array

        for snake in snake_array:
            snake.draw()
        tk.update_idletasks()
        tk.update()
        time.sleep(0.03)
    my_text = canvas.create_text(width/2, height/2, text=new_game_text, font=("Arial", 30), fill="blue")

def create_canvas():
    global num_players, my_text, players_entry,canvas,tk,dialog
    num_players = int(players_entry.get())
    dialog.destroy()
    tk = Tk()
    tk.title("Snake game")
    #tk.resizable(0, 0)
    canvas = Canvas(tk, width=width, height=height, bd=0, highlightthickness=0, bg="black")
    canvas.pack()
    my_text = canvas.create_text(width/2, height/2, text=new_game_text, font=("Arial", 30), fill="blue")
    canvas.bind_all("<KeyPress-Return>", begin_new_game)
    tk.focus_force()
    
btn = Button(dialog, text="Begin", command=create_canvas)
btn.pack()
dialog.focus()    

while True:
    if tk == None:
        dialog.update_idletasks()
        dialog.update()
        time.sleep(0.05)
    else:
        tk.update_idletasks()
        tk.update()
        time.sleep(0.05)


  
