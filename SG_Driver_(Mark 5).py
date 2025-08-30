import tkinter
from tkinter import *
from random import randrange, randint
from tkinter import messagebox
from PIL import Image, ImageTk
from collections import deque

board = Tk()
obstacle_image_instances = deque(maxlen=10)

board.geometry("400x500")
board.title("SG_Driver_(Mark 4)")
canvas = Canvas(board, width=400, height=500, background="#dee817")  

# Load static images
roadimg = ImageTk.PhotoImage(Image.open("road.png").resize((250, 500)))
carimg = ImageTk.PhotoImage(Image.open("car.png"))
paveimg = ImageTk.PhotoImage(Image.open("pavement.png"))
paveimgR = ImageTk.PhotoImage(Image.open("pavementR.png"))

canvas.create_image(75, 0, anchor=NW, image=roadimg)

for y in range(0, 500, 100):
    canvas.create_image(0, y, anchor=NW, image=paveimg)
    canvas.create_image(325, y, anchor=NW, image=paveimgR)

car = canvas.create_image(200, 300, anchor=NW, image=carimg)
canvas.pack(expand=1, fill=BOTH)

obc = ""
paused = False
ob_height = randrange(175, 200)
car_speed = 40000
interval = 3750
score = 0
lives = 3

score_text = canvas.create_text(10, 10, anchor="nw", fill="darkblue", text="Score: " + str(score))
lives_text = canvas.create_text(390, 10, anchor="ne", fill="darkblue", text="Lives: " + str(lives))

obs = []
mup = 3
md = 3

def obcreate():
    global obs, obc, paused
    if paused:
        return
    logic = randint(0, 1)
    x1 = randrange(50, 126)
    x2 = randrange(50, 156)
    logic0 = 100 + x2
    logic1 = 300 - x1

    height = 15

    if logic == 0:
        width = max(logic0 - 75, 10)
        obsimg = ImageTk.PhotoImage(Image.open("obs.png").resize((width, height)))
        obstacle_image_instances.append(obsimg)
        obc = canvas.create_image(75, 60, anchor=NW, image=obsimg)
        obs.append(obc)
    else:
        width = max(325 - logic1, 10)
        obsimg = ImageTk.PhotoImage(Image.open("obs.png").resize((width, height)))
        obstacle_image_instances.append(obsimg)
        obc = canvas.create_image(logic1, 60, anchor=NW, image=obsimg)
        obs.append(obc)

    board.after(interval, obcreate)

def moving():
    for ob in obs:
        coords = canvas.coords(ob)
        if len(coords) == 2:
            canvas.move(ob, 0, 10)
            if coords[1] > 500:
                pass
    board.after(car_speed, moving)
    catching()

def catching():
    global obc, score, lives, paused
    car_box = canvas.bbox(car)
    if not car_box:
        return
    x1, y1, x2, y2 = car_box
    fact = canvas.find_overlapping(x1 + 10, y1 + 10, x2 - 10, y2 - 10)
    fact = list(fact)
    if car in fact:
        fact.remove(car)
    if len(fact) >= 2:
        print("Current Life:", lives)
        if lives == 0:
            if obc in obs:
                obs.remove(obc)
            canvas.delete(obc)
            board.destroy()
            messagebox.showinfo("GAME OVER!...", f"You have scored: {score}")
        else:
            lives -= 1
            canvas.itemconfigure(lives_text, text="Lives: " + str(lives))
            paused = True
            choice = messagebox.askyesno(detail=f"Do You Want to Use One of Your {lives + 1} Lives?", title="You Crashed On an Obstacle!")
            if choice:
                paused = False
                obcreate()
            else:
                board.destroy()
                messagebox.showinfo("GAME OVER!...", f"You have scored: {score}")
            print("Choice:", choice)
    score += 1
    canvas.itemconfigure(score_text, text="Score: " + str(score // 10))
    board.after(100, catching)

# function to increase speed depends on score
def speed():
    global car_speed
    multi  = (score//100) * 10
    car_speed -= multi

def left(event):
    x1, y1 = canvas.coords(car)
    if x1 > 120:
        canvas.move(car, -20, 0)

def right(event):
    x1, y1 = canvas.coords(car)
    if x1 < 250:
        canvas.move(car, 20, 0)

def acc(event):
    global mup, md
    if mup > 0:
        canvas.move(car, 0, -20)
        mup -= 1
        if md < 3:
            md += 1

def brake(event):
    global md, mup
    if md > 0:
        canvas.move(car, 0, 20)
        md -= 1
        if mup < 3:
            mup += 1

canvas.bind("<Left>", left)
canvas.bind("<Right>", right)
canvas.bind("<Up>", acc)
canvas.bind("<Down>", brake)
canvas.focus_set()

board.after(1000, obcreate)
# board.after(1000, catching)
board.after(1000, moving)
board.after(1000, speed)
board.mainloop()