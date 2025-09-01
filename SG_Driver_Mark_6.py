import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randrange, randint
from collections import deque

class game:

    def on_close(self):
        print("Game window is closing...")
        self.game_win.destroy()
        with open("data.txt","a") as file:
            file.write(f"[{self.score},{self.lives}]")


    def main_game(self,master):
        self.game_win = tk.Toplevel(master)
        self.game_win.protocol("WM_DELETE_WINDOW", self.on_close)
        self.game_win.geometry("400x500")
        self.game_win.title("SG_Driver_(Mark 6)")

        canvas = tk.Canvas(self.game_win, width=400, height=500, background="#dee817")
        canvas.pack(expand=1, fill=tk.BOTH)

        # Load images
        roadimg = ImageTk.PhotoImage(Image.open("road.png").resize((250, 500)))
        carimg = ImageTk.PhotoImage(Image.open("car.png"))
        paveimg = ImageTk.PhotoImage(Image.open("pavement.png"))
        paveimgR = ImageTk.PhotoImage(Image.open("pavementR.png"))

        canvas.roadimg = roadimg
        canvas.carimg = carimg
        canvas.paveimg = paveimg
        canvas.paveimgR = paveimgR

        canvas.create_image(75, 0, anchor=tk.NW, image=roadimg)

        # Unified pavement setup
        tile_height = min(paveimg.height(), paveimgR.height()) or 100
        canvas_height = 500
        num_tiles = canvas_height // tile_height + 2

        pavement_Left = []
        pavement_Right = []

        for i in range(num_tiles):
            y = i * tile_height
            lid = canvas.create_image(0, y, anchor=tk.NW, image=paveimg)
            rid = canvas.create_image(325, y, anchor=tk.NW, image=paveimgR)
            pavement_Left.append(lid)
            pavement_Right.append(rid)

        car = canvas.create_image(200, 300, anchor=tk.NW, image=carimg)

        # Game state
        obstacle_image_instances = deque(maxlen=10)
        obs = []
        obc = None
        paused = False
        car_speed = 425
        interval = 3750
        self.score = 0
        self.lives = 3
        mup = 3
        md = 3

        score_text = canvas.create_text(10, 10, anchor="nw", fill="darkblue", text="Score: 0")
        lives_text = canvas.create_text(390, 10, anchor="ne", fill="darkblue", text="Lives: 3")

        def obcreate():
            nonlocal obc, paused
            if paused:
                return
            logic = randint(0, 1)
            x1 = randrange(50, 126)
            x2 = randrange(50, 156)
            logic0 = 100 + x2
            logic1 = 300 - x1
            height = 15

            width = max((logic0 - 75) if logic == 0 else (325 - logic1), 10)
            obsimg = ImageTk.PhotoImage(Image.open("obs.png").resize((width, height)))
            obstacle_image_instances.append(obsimg)

            obc = canvas.create_image(75 if logic == 0 else logic1, 60, anchor=tk.NW, image=obsimg)
            obs.append(obc)
            self.game_win.after(interval, obcreate)

        def move_obstacles():
            for ob in obs:
                coords = canvas.coords(ob)
                if coords:
                    canvas.move(ob, 0, 10)
            self.game_win.after(car_speed, move_obstacles)
            catching()

        def catching():
            nonlocal paused, obc
            car_box = canvas.bbox(car)
            if not car_box or paused:
                return
            x1, y1, x2, y2 = car_box
            fact = canvas.find_overlapping(x1 + 10, y1 + 10, x2 - 10, y2 - 10)
            fact = list(fact)
            if car in fact:
                fact.remove(car)
            if len(fact) >= 2:
                if self.lives == 0:
                    if obc in obs:
                        obs.remove(obc)
                    canvas.delete(obc)
                    self.game_win.destroy()
                    messagebox.showinfo("GAME OVER", f"You scored: {self.score}")
                else:
                    self.lives -= 1
                    canvas.itemconfigure(lives_text, text=f"Lives: {self.lives}")
                    paused = True
                    choice = messagebox.askyesno("Crash!", f"Use one of your {self.lives + 1} lives?")
                    if choice:
                        paused = False
                        obcreate()
                    else:
                        self.game_win.destroy()
                        messagebox.showinfo("GAME OVER", f"You scored: {self.score}")
            self.score += 1
            canvas.itemconfigure(score_text, text=f"Score: {self.score // 10}")
            self.game_win.after(50, catching)

        def speed():
            nonlocal car_speed, interval
            speed_boost = (self.score // 1000) * 10
            car_speed = max(425 - speed_boost, 100)
            interval_drop = (self.score // 1000) * 25
            if car_speed <= 200:
                interval = max(3750 - interval_drop, 1400)
            self.game_win.after(50, speed)

        def move_pavements():
            for pavement in pavement_Left + pavement_Right:
                canvas.move(pavement, 0, 2)
                x, y = canvas.coords(pavement)
                if y > canvas_height:
                    canvas.coords(pavement, x, -tile_height)
            self.game_win.after(50, move_pavements)

        def left(event):
            x1, _ = canvas.coords(car)
            if x1 > 120:
                canvas.move(car, -20, 0)

        def right(event):
            x1, _ = canvas.coords(car)
            if x1 < 250:
                canvas.move(car, 20, 0)

        def acc(event):
            nonlocal mup, md
            if mup > 0:
                canvas.move(car, 0, -20)
                mup -= 1
                md = min(md + 1, 3)

        def brake(event):
            nonlocal md, mup
            if md > 0:
                canvas.move(car, 0, 20)
                md -= 1
                mup = min(mup + 1, 3)

        canvas.bind("<Left>", left)
        canvas.bind("<Right>", right)
        canvas.bind("<Up>", acc)
        canvas.bind("<Down>", brake)
        canvas.focus_set()

        move_pavements()
        self.game_win.after(50, obcreate)
        self.game_win.after(50, move_obstacles)
        self.game_win.after(50, speed)
