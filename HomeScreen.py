import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from SG_Driver_Mark_7 import game

username = ""

def handleResume():
    try:
        with open("data.txt", "r") as file:
            lines = file.readlines()
            if not lines:
                print("No saved data found.")
                return
            last_line = lines[-1].strip().split(",")
            if len(last_line) >= 3:
                lives = last_line[2]
                score = last_line[1]
                name = last_line[0]
                print("Resume Data From File:", lives, score)
                gameobj = game(lives, score)
                gameobj.username = name
                gameobj.main_game(board)
                board.withdraw()
    except Exception as e:
        print("Error reading resume data:", e)

def handleSubmit():
    global username
    username = inputbox.get().strip()
    if username:
        print("Your Username:", username)
        with open("data.txt", "a", encoding="utf-8") as file:
            file.write(f"{username},")  # Score and lives will be added on close

def handleNewGame():
    global username
    username = inputbox.get().strip()
    if not username:
        messagebox.showwarning("Missing Name", "Please enter your username before starting a new game.")
        return
    print("Creating New Game for:", username)
    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(f"{username},")
    gameobj = game(3, 0)
    gameobj.username = username
    gameobj.main_game(board)
    board.withdraw()

# Initialize main window
board = tk.Tk()
board.geometry("400x500")
board.title("SG Driver")

# Load and set background image
bg_image = Image.open("home.png").resize((400, 500))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(board, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo  # Prevent garbage collection

# Transparent-style labels (no bg set)
game_label = tk.Label(board, text="SG_Driver", fg="white", font=("Helvetica", 20, "bold"))
label = tk.Label(board, text="Enter Your Username:", fg="white", font=("Helvetica", 12))

# Entry and buttons
inputbox = tk.Entry(board, width=35)
newbutton = tk.Button(board, text="New Game", background="red", width=35, command=handleNewGame)
resbutton = tk.Button(board, text="Resume Game", background="green", width=35, command=handleResume)
exitbutton = tk.Button(board, text="Exit", background="blue", width=35, command=board.destroy)

# Layout
game_label.pack(pady=(30, 10))
label.pack()
inputbox.pack(pady=40)
newbutton.pack(pady=10)
resbutton.pack(pady=10)
exitbutton.pack(pady=10)

inputbox.bind("<Return>", lambda event: handleSubmit())
board.mainloop()
