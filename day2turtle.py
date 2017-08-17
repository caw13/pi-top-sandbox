import turtle
import random
t = turtle.Pen()

def square(x, y, size):
    t.penup()
    t.setpos(x,y)
    t.pendown()
    t.begin_fill()
    for counter in range(0,4):
        t.forward(size)
        t.right(90)
    t.end_fill()

square(25,25,100)
square(0,50,50)
for i in range(0,10000):
    t.color(random.random(),random.random(),random.random())
    x = random.randint(-200,200)
    y = random.randint(-200,200)
    size = random.randint(10,500)
    square(x,y,size)
