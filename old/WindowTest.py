from tkinter import *
import time

master = Tk()

def task():
    print("hello")
    master.after(2000, task)

variable = StringVar(master)
variable.set("one") # default value

w = OptionMenu(master, variable, "one", "two", "three")
w.pack()

master.after(2000, task)
mainloop()
