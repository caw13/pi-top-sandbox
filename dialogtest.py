from tkinter import *

dialog = Tk()
name_label = Label(dialog, text="Your name")
name_label.pack()

name_entry = Entry(dialog)
name_entry.pack()

speed_label = Label(dialog, text="Speed")
speed_label.pack()
speed_entry = Entry(dialog)
speed_entry.pack()
speed_entry.insert(0,"1")

def begin():
    name = name_entry.get()
    print("Hello %s" % name)
    speed = int(speed_entry.get())
    print("Speed is %s" % speed)

btn = Button(dialog, text="Begin", command=begin)
btn.pack()
