#!/usr/bin/env python
from random import randint
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import os
import random
import pyperclip
import json

FONT = "Courier"
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- SEARCH FUNCTIONALITY ------------------------------- #
def find_file(filename, search_path):
    for root, _, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)


def find_password():
    file = find_file("password_manager.json", "/")
    print(f"File found: {file}")
    website = web_input.get().strip()
    print(f"Website input: {website}")
    if not file:
        messagebox.showwarning("No file", "No data file has been loaded or saved yet")
        return
    try:
        with open(file, "r") as data_file:
            print(file)
            data = json.load(data_file)
            print(f"Loaded data: {data}")
    except FileNotFoundError:
        messagebox.showerror("File not found", "Could not find the data file.")
        return

    if website in data:
        password = data[website]["password"]
        messagebox.showinfo(message=f"Website: {website}\nPassword: {password}")
        web_input.delete(0, END)
    else:
        messagebox.showwarning("Website not found", "No data found for the website entered.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    gen_pass = [random.choice(letters) for _ in range(randint(4, 8))] + \
               [random.choice(numbers) for _ in range(randint(2, 4))] + \
               [random.choice(symbols) for _ in range(randint(2,4))]

    random.shuffle(gen_pass)
    pass_word = "".join(gen_pass)
    password_input.insert(0, pass_word)
    pyperclip.copy(pass_word)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = web_input.get()
    password = password_input.get()
    email = email_user_input.get()
    new_data = {
        web: {
            "email": email,
            "password": password
        }
    }
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
                file_path = os.path.join(folder_path, "password_manager.json")
                try:
                    with open(file_path, "r") as file:
                        data = json.load(file)
                except FileNotFoundError:
                        data = new_data
                        messagebox.showinfo("Success", "Data saved successfully!")
                else:
                    data.update(new_data)
                    messagebox.showinfo("Success", "Data updated successfully!")
                finally:
                    with open(file_path, "w") as file:
                        json.dump(data, file, indent=4)
                        web_input.delete(0, END)
                        password_input.delete(0, END)


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

web_input = Entry()
web_input.grid(column=1, row=1, sticky='w')
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

#search button
search = Button(width=14,text="Search", bg="white", command=find_password)
search.grid(column=2, row=1, sticky='w', pady=5)

#add button
add = Button(text="Add", width=36, bg="white", command=save)
add.grid(column=1, row=4,columnspan=2, sticky='w')





window.mainloop()