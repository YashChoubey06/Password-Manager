from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def random_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list = (
        [random.choice(letters) for _ in range(nr_letters)] +
        [random.choice(symbols) for _ in range(nr_symbols)] +
        [random.choice(numbers) for _ in range(nr_numbers)]
    )


    random.shuffle(password_list)

    password = ""
    for char in password_list:
      password += char

    pass_entry.insert(END, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    passw = pass_entry.get()
    user = user_entry.get()
    web = website_entry.get()

    new_data = {
        web : {
            "email" : user,
            "password" : passw
        }
    }

    if len(passw) == 0 or len(user) == 0 or len(web) == 0:
        messagebox.showinfo(title="Oops", message="Please dont leave any fields empty")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data,file, indent = 4)

        else:
            data.update(new_data)

            with open("data.json", "w") as file:
                json.dump(data, file, indent = 4)

        finally:
            pass_entry.delete(0, END)
            website_entry.delete(0, END)

# ---------------------------- Search ------------------------------- #

def find_pass():
    web_search = website_entry.get()
    
    if web_search == "":
        messagebox.showinfo(title="Oops", message="The website entry cannot be blank!")
    else:
        try:
            with open("data.json", "r") as file:
                data_file = json.load(file)

        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="The Password database is empty D:")

        else:
            try:
                req_pass = data_file[web_search]['password']
                req_mail = data_file[web_search]['email']

            except KeyError:
                messagebox.showinfo(title="Oops", message="There's no password saved for that domain D:")

            else:
                messagebox.showinfo(title=web_search, message=f"Email: {req_mail}\nPassword: {req_pass}")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

icon = PhotoImage(file = "logo.png")
canvas = Canvas(height= 200, width = 200)
canvas.create_image(100,100,image = icon)
canvas.grid(column = 1, row = 0)

website_label = Label(text="Website:")
website_label.grid(column = 0, row = 1)

user_label = Label(text="Email/Username:")
user_label.grid(column = 0, row = 2)

pass_label = Label(text="Password:")
pass_label.grid(column = 0, row = 3)

website_entry = Entry(width= 21)
website_entry.grid(column = 1, row = 1)
website_entry.focus()

user_entry = Entry(width= 35)
user_entry.grid(column = 1, row = 2,  columnspan = 2)
user_entry.insert(END, "dummy@gmail.com")

pass_entry = Entry(width= 21)
pass_entry.grid(column = 1, row = 3)

gen_pass = Button(text= "Generate One", width = 11, command=random_password)
gen_pass.grid(column = 2, row = 3)

search_button = Button(text="Search", width = 11, command = find_pass)
search_button.grid(column = 2, row = 1)

add_button = Button(text="Add", width=30, command= save)
add_button.grid(column = 1, row = 4, columnspan = 2)


window.mainloop()

