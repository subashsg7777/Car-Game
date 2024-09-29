import tkinter
from tkinter import *
from random import randrange
from tkinter import messagebox
from random import randint
from pygame import mixer
board = Tk()
obw = 0
mixer.init()
mixer.music.load("background.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)
board.geometry("400x500")
board.title("SG_Driver_(Mark 2)")
canvas = Canvas(board,width=400,height=500,background="#dee817")
canvas.create_rectangle(100,0,300,500,fill="green",width=0)
car = canvas.create_rectangle(200,300,225,350,fill="red")
canvas.pack()
obc = ""
#obstacles properties are
ob_width = randrange(300,400)
ob_height = randrange(175,200)
car_speed = 425
interval = 3750
difficulty = 2
score = 0
score_text = canvas.create_text(10, 10, anchor="nw", fill="darkblue", text="Score: "+ str(score))
lives = 3
lives_text = canvas.create_text(400-10, 10, anchor="ne", fill="darkblue", text="Lives: "+ str(lives))

obs = []
#creating a common up an down movement control value
mup = 3
md = 3
logic = randint(0,1)
#new object creation engine
def obcreate():
    global obs,obc
    logic = randint(0,1)
    x1 = randrange(50,126)
    x2 = randrange(50,156)
    y1 = ob_height
    y2 = randrange(175,200)
    logic0 = 100+x2
    logic1=300-x1
    if logic == 0:
        obc = canvas.create_rectangle(100,60,logic0,75.0,fill="red")
        obs.append(obc)
    elif logic ==1 :
        try:
            obc = canvas.create_rectangle(logic1,60,300,75.0,fill="red")
            obs.append(obc)
        except:
            messagebox.showerror("can't create rught side obstacles!..")
    #obc = canvas.create_rectangle(x1, 50.0, x2, 75.0,fill="red")
    board.after(interval,obcreate)
# for moving the ob's 
def moving():
    for ob in obs:
        (carx, cary, carx2, cary2) = canvas.coords(ob)
        canvas.move(ob, 0, 10)
        if cary2 > 500:
            #acc(ob)
            pass
    board.after(car_speed, moving)

def catching():
    global obc,score,lives,car_speed
    (carx, cary, carx2, cary2) = canvas.coords(car)
    '''for ob in obs:
        (obx1, oby1, obx2, oby2) = canvas.coords(obc)
        if carx < obx1 and obx2 < carx2 and cary2 - oby2 < 20:
            print("touched")
            obs.remove(ob)
            canvas.delete(ob)
            messagebox.showinfo("GAME OVER!...",f"you have scored : {score}")
            board.destroy()'''
    points = canvas.coords(car)
    fact = canvas.find_overlapping(points[0],points[1],points[2],points[3])
    fact = list(fact)
    fact.remove(car)
    if len(fact) >=2 :
        obs.remove(obc)
        canvas.delete(obc)
        messagebox.showinfo("GAME OVER!...",f"you have scored : {score}")
        board.destroy()
    score +=1
    
    canvas.itemconfigure(score_text,text="Score :"+str(score))
    board.after(100, catching)

#for moving the ctcher
def left(event):
    (x1,y1,x2,y2) = canvas.coords(car)
    if x1 >1:
        if x1 <100:
            pass
        else:
            canvas.move(car,-20,0)
    

def right(event):
    (x1,y1,x2,y2) = canvas.coords(car)
    if x2 < 400:
        if x2 >300:
            pass
        else:
            canvas.move(car,20,0)

#to move the car in forward 
def acc(event):
    global mup,md
    if mup != 0:
        canvas.move(car,0,-20)
        mup -=1
        if md >= 3:
            pass
        else:
            md +=1
    else:
        pass

#to apply brake to car or take reverse direction
def brake(event):
    global md,mup
    if md != 0:
        canvas.move(car,0,20)
        md -=1
        if mup >= 3:
            pass
        else:
            mup += 1
canvas.bind("<Left>",left)
canvas.bind("<Right>",right)
canvas.bind("<Up>",acc)
canvas.bind("<Down>",brake)
canvas.focus_set()
board.after(1000,obcreate)
board.after(1000,catching)
board.after(1000,moving)
board.mainloop()


#100-299