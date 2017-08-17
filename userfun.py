from tkinter import *

tk = Tk()

canvas = Canvas(tk, width=500, height=500)
canvas.pack()

my_shape = canvas.create_rectangle(10, 10, 50, 50, fill="blue")

def move_shape(event):
    if event.keysym == 'Up':
        canvas.move(my_shape, 0, -3)
    elif event.keysym == 'Down':
        canvas.move(my_shape, 0, 3)
    elif event.keysym == 'Left':
        canvas.move(my_shape, -3, 0)
    else:
        canvas.move(my_shape, 3, 0)

canvas.bind_all('<KeyPress-Up>', move_shape)
canvas.bind_all('<KeyPress-Down>', move_shape)
canvas.bind_all('<KeyPress-Left>', move_shape)
canvas.bind_all('<KeyPress-Right>', move_shape)
