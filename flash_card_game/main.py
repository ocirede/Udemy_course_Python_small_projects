from tkinter import  *
import pandas as pd
import random

#costants
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("./data/german_word.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def change_card():
    global current_card, flip_timer, to_learn
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    new_word = current_card["German"]
    canvas.itemconfig(g_title, text="German", fill="black")
    canvas.itemconfig(g_word, text=new_word, fill= "black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(g_title, text="English", fill= "white")
    new_e_word = current_card["English"]
    canvas.itemconfig(g_word, text=new_e_word, fill= "white")
    canvas.itemconfig(canvas_image, image=card_back_img)

def is_known_remove():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv")
    change_card()


window = Tk()
window.title("Flashy Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Persistent PhotoImage references
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")

# Canvas setup
canvas = Canvas(width=800, height=526)
canvas_image = canvas.create_image(400, 263, image=card_front_img)
g_title = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
g_word = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
canvas.config( bg=BACKGROUND_COLOR, highlightthickness=0)

canvas.grid(column=1, row=1, columnspan=2)


#Buttons
right_img = PhotoImage(file="./images/right.png")
right_button = Button( image=right_img,  command= is_known_remove)
right_button.grid(column=2, row=2)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img,  command=change_card)
wrong_button.grid(column=1, row=2)


change_card()
window.mainloop()

