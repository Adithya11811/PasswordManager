from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
# For json not text file writing----
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pwd():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = ''.join(password_list)

    pwd_text.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_title = website_text.get()
    email_title = email_text.get()
    pwd = pwd_text.get()
    # for JSON
    new_data = {website_title: {
        'email': email_title,
        'Password': pwd
        }
    }

    if len(website_title) == 0 or len(pwd) == 0:
        messagebox.showwarning(title='oops', message="Please don't leave any fields empty")
    else:
        # Writing into a text file
        # with open('data.txt', mode='a') as data_file:
        #     data_file.write(f'{website_title} | {email_title} | {pwd}\n')
        # website_text.delete(0, END)
        # pwd_text.delete(0, END)

        # Writing into a json format
        try:
            with open('data.json', 'r') as data_file:
                # Reading the old data
                data = json.load(data_file)
                # Updating the old Data
                data.update(new_data)

            with open('data.json', 'w') as data_file:
                # saving the updated data
                json.dump(data, data_file, indent=4)

        except json.decoder.JSONDecodeError and FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)

        website_text.delete(0, END)
        pwd_text.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_pwd():
    website = website_text.get()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title='error...', message='No data file found')
    else:
        if website in data:
            email = data[website]['email']
            pwd = data[website]['Password']
            messagebox.showinfo(title=website, message=f"Email: {email}\npassword: {pwd}")
        else:
            messagebox.showinfo(title='Error 404 😒', message=f'No details of {website}')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('PASSWORD MANAGER')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
pwd_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=pwd_img)
canvas.grid(row=0, column=1)

# Website part
website_label = Label(text='Website:')
website_label.grid(row=1, column=0)

website_text = Entry(width=33)
website_text.focus()
website_text.grid(row=1, column=1)

search = Button(text='Search', width=14, command=find_pwd)
search.grid(row=1, column=2)

# Email
email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)

email_text = Entry(width=51)
email_text.insert(0, 'adithya11811@gmail.com')
email_text.grid(row=2, column=1, columnspan=2)

# Password
pwd_label = Label(text='Password:')
pwd_label.grid(row=3, column=0)

pwd_text = Entry(width=33)
pwd_text.grid(row=3, column=1)

# Buttons
gen_pwd = Button(text='GeneratePassword', command=gen_pwd)
gen_pwd.grid(row=3, column=2)

add_button = Button(text='Add', width=43, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
