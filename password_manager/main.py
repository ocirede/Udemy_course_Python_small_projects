#!/usr/bin/env python
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import os
import random

FONT = "Courier"
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    gen_pass = [random.choice(letters) for _ in range(4)] + \
               [random.choice(numbers) for _ in range(4)] + \
               [random.choice(symbols) for _ in range(4)]

    random.shuffle(gen_pass)
    pass_word = "".join(gen_pass)
    password_input.insert(0, pass_word)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = web_input.get()
    password = password_input.get()
    email = email_user_input.get()

    if web == "" or password == "":
        messagebox.showinfo(title="Empty inputs", message="You must fill up the input fields")
    else:
        is_ok = messagebox.askokcancel(
            title=web,
            message=f"These are the details entered: Website:{web}\nEmail: {email}\nPassword: {password}\nIs it okay"
                    f" to save?"
        )
        if is_ok:
            folder_path = askdirectory(title="Select Folder")
            if folder_path:
                file_path = os.path.join(folder_path, "data.txt")
                with open(file_path, "a") as file:
                    file.write(f"{web} | {email} | {password}\n")

                web_input.delete(0, END)
                password_input.delete(0, END)

                messagebox.showinfo("Success", "Data saved successfully!")
            else:
                messagebox.showwarning("No folder selected", "You must select a folder to save the file.")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Passwords manager")
window.config(padx=50, pady=50, bg="white")

#Canvas
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo = PhotoImage(file="/home/chicco/PycharmProjects/Projects/password_manager/logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)


#  website label

web_label = Label()
web_label.config(text="Website:", fg="black", bg="white",font=(FONT, 12, "bold"))
web_label.grid(column=0, row=1, sticky='e', padx=5, pady=5)

# email/username label

email_pass = Label()
email_pass.config(text="Email/Username:", fg="black", bg="white",font=(FONT, 12, "bold"))
email_pass.grid(column=0, row=2, sticky='e',  padx=5, pady=5)


# password label
password_label= Label()
password_label.config(text="Password:", fg="black", bg="white",font=(FONT, 12, "bold"))
password_label.grid(column=0, row=3, sticky='e',  padx=5, pady=5)


#website entry

web_input = Entry(width=35)
web_input.grid(column=1, row=1, columnspan=2, sticky='w')
web_input.focus()

# Email entry
email_user_input = Entry(width=35)
email_user_input.grid(column=1, row=2, columnspan=2, sticky='w')
email_user_input.insert(0, "federico.diaferia@gmail.com")

# password label

password_input = Entry(width=21)
password_input.grid(column=1, row=3, sticky='w')


# generate password button

pass_gen = Button(width=14,text="Generate Password", bg="white", command=password_generator)
pass_gen.grid(column=2, row=3, sticky='w', pady=5)


#add button
add = Button(text="Add", width=36, bg="white", command=save)
add.grid(column=1, row=4,columnspan=2, sticky='w')





window.mainloop()