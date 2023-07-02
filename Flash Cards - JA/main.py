import tkinter as tk
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


# =========================================================================================================
def new_japanese_card():
    global current_card, flip_after
    window.after_cancel(flip_after)
    current_card = choice(ToLearn)
    canvas.itemconfig(Language, text="Japanese", fill="black")
    canvas.itemconfig(Word, text=current_card['japanese'], fill="black")
    canvas.itemconfig(card_image, image=front_card_photo)
    flip_after = window.after(3000, new_english_card)


def new_english_card():
    canvas.itemconfig(Language, text="English", fill="white")
    canvas.itemconfig(Word, text=current_card['english'].capitalize(), fill="white")
    canvas.itemconfig(card_image, image=back_card_photo)


def is_known():
    ToLearn.remove(current_card)
    data = pd.DataFrame(ToLearn)
    data.to_csv("data/words_to_learn_ja.csv", index=False)
    new_japanese_card()


# ===============================================================================================
try:
    data_df = pd.read_csv("data/words_to_learn_ja.csv")
except FileNotFoundError:
    data_df = pd.read_csv("data/japanese_words.csv")

ToLearn = data_df.to_dict(orient="records")

window = tk.Tk()
window.title("ja-en Flash Cards")
window.config(width=900, height=600, padx=50, pady=30, bg=BACKGROUND_COLOR)

flip_after = window.after(3000, func=new_english_card)

canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card_photo = tk.PhotoImage(file='images/card_front.png')
back_card_photo = tk.PhotoImage(file='images/card_back.png')
card_image = canvas.create_image(400, 263, image=front_card_photo)
Language = canvas.create_text(400, 150, text="", font=("Ariel", 30, "italic"))
Word = canvas.create_text(400, 263, text="",font=("Ariel",40, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right_image = tk.PhotoImage(file="images/right.png")
button = tk.Button(image=right_image, bd=0, bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
                   command=is_known)
button.grid(column=0, row=1)

wrong_image = tk.PhotoImage(file="images/wrong.png")
button = tk.Button(image=wrong_image, bd=0, bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
                   command=new_japanese_card)
button.grid(column=1, row=1)

new_japanese_card()

window.mainloop()
