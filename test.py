from random import randrange
import tkinter
from tkinter import *
from random import randrange
from tkinter import messagebox

board = Tk()
obw = 0
board.geometry("400x500")
board.title("Game01")
canvas = Canvas(board,width=400,height=500,background="#dee817")
logic = randrange(0,2)
canvas.pack()
print(logic)
ob_height = randrange(175,200)
obs = []
interval = 4000
def obcreate():
    global obc
    x1 = randrange(100,200)
    x2 = randrange(150,275)
    y1 = ob_height
    y2 = randrange(175,200)
    if logic == 0:
        obc = canvas.create_rectangle(100,50.0,x2,75.0,fill="red")
    else:
        obc = canvas.create_rectangle(x1,50.0,200,75.0,fill="red")
    #obc = canvas.create_rectangle(x1, 50.0, x2, 75.0,fill="red")
    print(canvas.coords(obc))
    obs.append(obc)
    board.after(interval,obcreate)

board.mainloop()