from tkinter import *

tk = Tk()

canvas = Canvas(tk, width=500, height=500)
canvas.pack()
my_image = PhotoImage(file="field.gif")
canvas.create_image(0,0,anchor=NW, image=my_image)
