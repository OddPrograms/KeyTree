from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyclip
import json

# CONSTANTS
bgcolor = "#e5decf"

# PASSWORD GENERATOR
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_input.delete(0, END)
    password_input.insert(0, password)
    pyclip.copy(password)

# SAVE PASSWORD
def save():
    website = website_input.get()
    email = email_user_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Missing Info", message="Field Empty!")
    else:
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
                if website in data:
                    do_update = messagebox.askyesno("Warning", f"There is already a password saved for {website}.\nWould you like to overwrite?")
                    if do_update:
                        data[website]["password"] = password
                        data[website]["email"] = email
                    else:
                        return
                else:
                    data.update(new_data)

        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = new_data

        finally:
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
            website_input.delete(0, END)
            password_input.delete(0, END)

# CLOSE WINDOW
def close(event):
   window.destroy()


# FIND PASSWORD
def find_password():
    website = website_input.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No entry for {website}")

def get_default_email():
    try:
        with open("default_email.txt") as default_data:
            lines = 0
            content = default_data.readlines()
            for i in content:
                if i:
                    lines += 1
            if lines == 2:
                default_email = content[1]
                return default_email
            else:
                default_email = ""
                return default_email
    except FileNotFoundError:
        with open("default_email.txt", "w+") as default_data:
            default_data.write("# This will set a default email, erase line 2 if not needed.")
            default_data.write("")
        return ""


# UI SETUP
window_width = 200
window_height = 200
window = Tk()
window.title("KeyTree")
window.config()
window.config(width=window_width, height=window_height, padx=20, pady=20, bg=bgcolor)
window.overrideredirect(1)


# Gets the requested values of the height and width.
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth() / 2 - windowWidth / 1)
positionDown = int(window.winfo_screenheight() / 2 - windowHeight / 1)

# Positions the window in the center of the page.
window.geometry("+{}+{}".format(positionRight, positionDown))


canvas = Canvas(width=window_width, height=window_height, bg=bgcolor, highlightthickness=0)
logo = PhotoImage(file="keytree.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)


# Labels
website_label = Label(text="Website: ", bg=bgcolor)
website_label.grid(column=0, row=1)
email_user_label = Label(text="Email/Username: ", bg=bgcolor)
email_user_label.grid(column=0, row=2)
password_label = Label(text="Password: ", bg=bgcolor)
password_label.grid(column=0, row=3)

# Inputs
website_input = Entry(width=33)
website_input.grid(column=1, row=1, pady=1)
website_input.focus()
email_user_input = Entry(width=52)
email_user_input.grid(column=1, row=2, columnspan=2)

default_email = str(get_default_email())

email_user_input.insert(0, default_email)

password_input = Entry(width=33)
password_input.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", bg=bgcolor, width=14, command=find_password)
search_button.grid(column=2, row=1, sticky="N, S, W, E")
generate_button = Button(text="Generate Password", bg=bgcolor, command=generate_password)
generate_button.grid(column=2, row=3, sticky="N, S, W, E")
add_button = Button(text="Add", bg=bgcolor, width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.bind("<Escape>", close)
window.mainloop()
