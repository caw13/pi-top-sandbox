from tkinter import *
import random
import time

tk = Tk()

canvas = Canvas(tk, width=500, height=500)
canvas.pack()

def random_color():
    r = random.randint(0,255)
    b = random.randint(0,255)
    g = random.randint(0,255)
    # Creates a hex representation of those numbers
    color = "#%02x%02x%02x" % (r,b,g)
    return color

def hello():
    print("Hello Chad")
    x1 = random.randint(0,500)
    y1 = random.randint(0,500)
    x2 = random.randint(x1,500)
    y2 = random.randint(y1,500)
    canvas.create_line(20, 20, 40, 500)
    my_shape = canvas.create_rectangle(x1,y1,x2,y2, fill=random_color())
    for x in range(0,60):
        canvas.move(my_shape, 5, 7)
        tk.update()
        time.sleep(0.05)



def fun():
    name = input("What is your name: ")
    color = colorchooser.askcolor()
    my_text = canvas.create_text(50, 50, text=name, font=("Arial",30), fill=color[1])
    for x in range(0,60):
        canvas.move(my_text, 5, 7)
        tk.update()
        time.sleep(0.05)

btn = Button(tk, text="Click me", command=hello)
btn.pack()

btn2 = Button(tk, text="Another one", command=fun)
btn2.pack()

def shapes():
    canvas.create_oval(10,10,25,100)
    canvas.create_polygon(10,10,100,10,100,110)

btn3 = Button(tk, text="Shapes", command=shapes)
btn3.pack()
