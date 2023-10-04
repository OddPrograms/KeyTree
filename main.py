from tkinter import *
from tkinter import messagebox
# import tkinter.scrolledtext as st
import string
import secrets
import pyclip
import json
import os


# CONSTANTS
bgcolor = "#e5decf"
buttoncolor = "#2a6417"
buttontextcolor = "#ffffff"
alphabet = string.ascii_letters + string.digits + string.punctuation


# NEEDED FOR PYINSTALLER COMPILING IMAGES
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

key_tree = resource_path(r"keytree.png")
key_tree_icon = resource_path(r"keytreeicon.png")


# PASSWORD GENERATOR
def generate_password():
    if password_length.get() == "":
        passlength = 12
        password = ''.join(secrets.choice(alphabet) for i in range(passlength))
        password_input.delete(0, END)
        password_input.insert(0, password)
        pyclip.copy(password)
    elif password_length.get().isalpha():
        messagebox.showinfo(title="Invalid Type", message="The Password Length Entry Must Be An Integer, Defaulting To 12.")
    else:
        passlength = int(password_length.get())
        password = ''.join(secrets.choice(alphabet) for i in range(passlength))
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
            with open('data.json', 'w') as data_file, open("backup/data.backup.json", "w") as data_backup:
                json.dump(data, data_file, indent=4)
                json.dump(data, data_backup, indent=4)
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


# GET DEFAULT EMAIL IF SET
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


# PASSWORD TO CLIPBOARD UI
def password_to_clipboard():
    pass_window = Toplevel(window)
    pass_window.title("KeyTree Clipboard")
    pass_window.config(bg=bgcolor)
    pass_window_icon = PhotoImage(file = key_tree_icon)
    pass_window.iconphoto(False, pass_window_icon)
    # Gets the requested values of the height and width.
    passWindowWidth = pass_window.winfo_reqwidth()
    passWindowHeight = pass_window.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    passPositionRight = int(pass_window.winfo_screenwidth() / 2.95 - windowWidth / 1)
    passPositionDown = int(pass_window.winfo_screenheight() / 2 - windowHeight / 1)
    # Positions the window in the center of the page.
    pass_window.geometry("+{}+{}".format(passPositionRight, passPositionDown))


    button_area_canvas = Canvas(pass_window, bg=bgcolor, bd=0, highlightthickness=0, width=400, height=300)
    button_scroll_bar = Scrollbar(master=pass_window, orient='vertical', command=button_area_canvas.yview)

    button_area_frame = Frame(button_area_canvas, bg=bgcolor)
    button_area_frame.bind('<Configure>', lambda e: button_area_canvas.configure(scrollregion=button_area_canvas.bbox('all')))
    button_area_canvas.create_window((0, 0), window=button_area_frame, anchor='nw')

    button_scroll_bar.pack(side='right', fill='y')
    button_area_canvas.pack(side='left', fill='both')


    with open('data.json', 'r') as data_file:
        data = json.load(data_file)
        keyArray = []
        valueArray = []
        for key, value in data.items():
            keyArray.append(key)
            if value['email'] == 'email':
                pass
            else:
                valueArray.append(value)
        button = []
        for i in range(len(data.items())):
            def copy_from(x = i):
                pyclip.copy(str(valueArray[x]["password"]))
            # new_button = button.append(Button(pass_window, text=keyArray[i],  font=("sans-serif", 8), fg=buttontextcolor, bg=buttoncolor, width=14, bd=0, command=copy_from))
            new_button = button.append(Button(button_area_frame, text=keyArray[i],  font=("sans-serif", 8), fg=buttontextcolor, bg=buttoncolor, width=14, bd=0, command=copy_from))
            # button[i].grid(column=0, row=i+1, sticky=W, pady=10, padx=100)
            button[i].pack(pady=10, padx=150)

# Directory Setup For Backup
path = "backup"
# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(path)


# UI SETUP
window_width = 200
window_height = 200
window = Tk()
window.title("KeyTree")
window.config(width=window_width, height=window_height, padx=20, pady=20, bg=bgcolor)
window_icon = PhotoImage(file=key_tree_icon)
window.iconphoto(False, window_icon)
# window.overrideredirect(1)

# Gets the requested values of the height and width.
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth() / 2 - windowWidth / 1)
positionDown = int(window.winfo_screenheight() / 2 - windowHeight / 1)
# Positions the window in the center of the page.
window.geometry("+{}+{}".format(positionRight, positionDown))

canvas = Canvas(width=window_width, height=window_height, bg=bgcolor, highlightthickness=0)
logo = PhotoImage(file=key_tree)
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
website_input.grid(column=1, row=1, pady=1, padx=1)
website_input.focus()

email_user_input = Entry(width=50)
email_user_input.grid(column=1, row=2, columnspan=2, padx=1)
default_email = str(get_default_email())
email_user_input.insert(0, default_email)

password_input = Entry(width=33)
password_input.grid(column=1, row=3, padx=1)

password_length = Entry(width=3)
password_length.grid(column=0, row=4, padx=1)


# Buttons
search_button = Button(text="Search", font=("sans-serif", 8), fg=buttontextcolor, bg=buttoncolor, width=14, command=find_password, bd=0)
search_button.grid(column=2, row=1, sticky="N, S, W, E", pady=5)

generate_button = Button(text="Generate Password", font=("sans-serif", 8), fg=buttontextcolor, bg=buttoncolor, command=generate_password, bd=0)
generate_button.grid(column=2, row=3, sticky="N, S, W, E", pady=5)

add_button = Button(text="Add", font=("sans-serif", 8), fg=buttontextcolor, bg=buttoncolor, width=50, command=save, bd=0)
add_button.grid(column=1, row=4, columnspan=2)

clip_button = Button(text="Password To Clipboard", font=("sans-serif", 8), fg=buttontextcolor, bg=buttoncolor, width=20, command=password_to_clipboard, bd=0)
clip_button.grid(column=1, row=5, columnspan=2, pady=5)

window.bind("<Escape>", close)
window.mainloop()
