from tkinter import *
from tkinter import messagebox
from customtkinter import CTkEntry, CTkLabel, CTkButton, CTkCheckBox, CTkSlider
import pyglet, os, sys, random, pyperclip, json

# ---------------------------- CONSTANTS ------------------------------- #
MAIN_FONT = "IBM Plex Sans"
TITLE_FONT = "Press Start 2P"

DARK = "#161A30"
MID = "#31304D"
BACKGROUND = "#B6BBC4"
LIGHT = "#F0ECE5"

WARNING = "#CF3333"

FRAME_DELAY = 250

LOWER_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
CAPITAL_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- RESOURCE PATH ------------------------------- #
# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ---------------------------- FONT ------------------------------- #
pyglet.options["win32_gdi_font"] = True
font_path_1 = resource_path("assets/fonts/IBMPlexSans-Medium.ttf")
font_path_2 = resource_path("assets/fonts/PressStart2P-Regular.ttf")
pyglet.font.add_file(font_path_1)
pyglet.font.add_file(font_path_2)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_slider(value):
    global password_length
    slider_label.configure(text=f"Length: {int(value)}")
    password_length = int(value)

def update_characters():
    global characters
    characters = []

    lowercase_value = include_letters.get()
    capital_value = include_capital_letters.get()
    number_value = include_numbers.get()
    symbols_value = include_symbols.get()

    # Creates list
    if lowercase_value:
        characters.append(LOWER_LETTERS)
    if capital_value:
        characters.append(CAPITAL_LETTERS)
    if number_value:
        characters.append(NUMBERS)
    if symbols_value:
        characters.append(SYMBOLS)

    # Enables/disables
    if lowercase_value + capital_value + number_value + symbols_value == 1:
        if lowercase_value:
            lower_letters_toggle.configure(state="disabled")
        elif capital_value:
            upper_letters_toggle.configure(state="disabled")
        elif number_value:
            numbers_toggle.configure(state="disabled")
        else:
            symbols_toggle.configure(state="disabled")
    else:
        lower_letters_toggle.configure(state="normal")
        upper_letters_toggle.configure(state="normal")
        numbers_toggle.configure(state="normal")
        symbols_toggle.configure(state="normal")

def generate_password():
    pwd_entry.delete(0, END)
    password = ""

    for _ in range(password_length):
        random_list = random.choice(characters)
        random_character = random.choice(random_list)
        password += random_character

    pyperclip.copy(password)
    pwd_entry.insert(0, "".join(password))

# ---------------------------- SEARCH WEBSITE ------------------------------- #
def search_website():
    silent_option = silent_toggle.get()
    website = website_entry.get()

    if len(website) == 0:
        if silent_option:
            dialog_label.configure(text="Don't leave the website field empty!")
        else:
            messagebox.showwarning("Oops", "Don't leave the website field empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                credentials = data[website]
        except FileNotFoundError:
            if silent_option:
                dialog_label.configure(text="No data file. Save some credentials first!")
            else:
                messagebox.showerror("No data", "There's no data.json.\nDid you save any credentials?")
        except KeyError:
            if silent_option:
                dialog_label.configure(text="No match. Check spelling/capitalization.")
            else:
                messagebox.showerror("No match", "There was no match.\nDid you use the correct spelling and capitalization?")
        else:
            user_id = credentials["user_id"]
            password = credentials["password"]
            if silent_option:
                dialog_label.configure(text="Match. Credentials filled below.")

                username_entry.delete(0, END)
                pwd_entry.delete(0, END)

                username_entry.insert(0, user_id)
                pwd_entry.insert(0, password)
            else:
                messagebox.showinfo(website, f"User ID: {user_id}\nPassword: {password}")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    user_option = username_toggle.get()
    silent_option = silent_toggle.get()

    website = website_entry.get()
    username = username_entry.get()
    password = pwd_entry.get()

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        if silent_option:
            dialog_label.configure(text="Don't leave any fields empty!")
        else:
            messagebox.showwarning("Oops", "Don't leave any fields empty!")
    else:
        if not silent_option:
            confirm_save = messagebox.askokcancel(title=website,
                                                  message=f"Details entered:\n"
                                                                              f"\nWebsite: {website}"
                                                                              f"\nUser ID: {username}"
                                                                              f"\nPassword: {password}\n"
                                                                              f"\nConfirm save?"
                                              )

        if silent_option or confirm_save:

            new_data = {
                website: {
                    "user_id": username,
                    "password": password
                }
            }

            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                # Deletes fields
                dialog_label.configure(text="")
                website_entry.delete(0, END)
                pwd_entry.delete(0, END)
                if user_option == 0:
                    username_entry.delete(0, END)

# ---------------------------- ANIMATION ------------------------------- #
def animation():
    global frame

    # Reset animation
    if frame < numbers_of_frames-1:
        frame += 1
    else:
        frame = 0

    # Change title text
    if 3 < frame < 8:
        canvas.itemconfig(title_one, text="****", fill=MID)
        canvas.itemconfig(title_two, text="****", fill=MID)
    else:
        canvas.itemconfig(title_one, text="PASS", fill=LIGHT)
        canvas.itemconfig(title_two, text="WORD", fill=LIGHT)

    canvas.itemconfigure("animation", image=frames[frame])
    window.after(FRAME_DELAY, animation)

# ---------------------------- UI SETUP ------------------------------- #
characters = []
password_length = 16

window = Tk()
window.title("Password Manager")
window.config(width=800, height=600, padx=50, pady=25, bg=BACKGROUND)
window.columnconfigure(0, pad=20)
window.columnconfigure(1,pad=5)
window.rowconfigure(0, pad=10)

for i in range(1,13):
    window.rowconfigure(i, pad=5)

window.grid_rowconfigure(11, minsize=20)

icon_photo = PhotoImage(file=resource_path("assets/images/lock.png"))
window.iconphoto(False, icon_photo)

# ANIMATION
frames = [
    PhotoImage(file=resource_path("assets/images/001.png")),
    PhotoImage(file=resource_path("assets/images/002.png")),
    PhotoImage(file=resource_path("assets/images/003.png")),
    PhotoImage(file=resource_path("assets/images/004.png")),
    PhotoImage(file=resource_path("assets/images/005.png")),
    PhotoImage(file=resource_path("assets/images/005_2.png")),
    PhotoImage(file=resource_path("assets/images/005_3.png")),
    PhotoImage(file=resource_path("assets/images/005_4.png")),
    PhotoImage(file=resource_path("assets/images/004.png")),
    PhotoImage(file=resource_path("assets/images/003.png")),
    PhotoImage(file=resource_path("assets/images/002.png"))
]
numbers_of_frames = len(frames)
frame = 0

canvas = Canvas(width=200, height=200, bg=BACKGROUND, highlightthickness=0)
title_two = canvas.create_text(140, 100, text="WORD", font=(TITLE_FONT, 16, "bold"), fill=LIGHT)
canvas.create_image(0, 0, anchor="nw", image=frames[frame], tag="animation")
title_one = canvas.create_text(50, 100, text="PASS", font=(TITLE_FONT, 16, "bold"), fill=LIGHT)
canvas.grid(row=0, column=0, columnspan=3)

# DIALOG TEXT
dialog_label = CTkLabel(master=window, text="", anchor="w", font=(MAIN_FONT, 14, "bold"), text_color=WARNING)
dialog_label.grid(row=1, column=1, columnspan=2, sticky="w")

# WEBSITE
website_label = CTkLabel(master=window, text="Website", anchor="w", font=(MAIN_FONT, 14, "bold"), text_color=DARK)
website_entry = CTkEntry(master=window, width=240, font=(MAIN_FONT, 14), fg_color=LIGHT, text_color=DARK)
website_search = CTkButton(master=window, command=search_website, text="Search", width=75, font=(MAIN_FONT, 14), fg_color=MID, hover_color=DARK, text_color=LIGHT)
website_entry.focus()
website_label.grid(row=2, column=0, sticky="w")
website_entry.grid(row=2, column=1, sticky="w")
website_search.grid(row=2, column=2, sticky="e")

# USER ID
username_label = CTkLabel(master=window, text="User ID", anchor="w", font=(MAIN_FONT, 14, "bold"), text_color=DARK)
username_entry = CTkEntry(master=window, width=320, font=(MAIN_FONT, 14), fg_color=LIGHT, text_color=DARK)
username_label.grid(row=3, column=0, sticky="w")
username_entry.grid(row=3, column=1, columnspan=2)

# PASSWORD
pwd_label = CTkLabel(master=window, text="Password", anchor="w", font=(MAIN_FONT, 14, "bold"), text_color=DARK)
pwd_entry = CTkEntry(master=window, width=240, font=(MAIN_FONT, 14), fg_color=LIGHT, text_color=DARK)
pwd_generate_button = CTkButton(master=window, command=generate_password, text="Generate", width=75, font=(MAIN_FONT, 14), fg_color=MID, hover_color=DARK, text_color=LIGHT)
pwd_save_button = CTkButton(master=window, command=save_password, text="Save", width=320, font=(MAIN_FONT, 14), fg_color=MID, hover_color=DARK, text_color=LIGHT)

pwd_label.grid(row=4, column=0, sticky="w")
pwd_entry.grid(row=4, column=1, sticky="w")
pwd_generate_button.grid(row=4, column=2, sticky="e")
pwd_save_button.grid(row=5, column=1, columnspan=2, sticky="w")

# PASSWORD SETTINGS
length_slider = CTkSlider(master=window, command=password_slider, number_of_steps=98, from_=1, to=99, fg_color=LIGHT, border_color=BACKGROUND, progress_color=DARK, button_color=MID, button_hover_color=MID, width=320)
length_slider.grid(row=6, column=1, columnspan=2, sticky="w")
length_slider.set(16)

slider_label = CTkLabel(master=window, text=f"Length: 16", font=(MAIN_FONT, 14), text_color=DARK)
slider_label.grid(row=6, column=0, sticky="w")

include_letters = IntVar()
include_capital_letters = IntVar()
include_numbers = IntVar()
include_symbols = IntVar()

lower_letters_toggle = CTkCheckBox(master=window, variable=include_letters, command=update_characters, state="disabled", text="Lowercase (abc)", font=(MAIN_FONT, 14), text_color=DARK, border_color=MID, fg_color=MID, hover_color=DARK)
lower_letters_toggle.grid(row=7, column=1, sticky="w")
lower_letters_toggle.select()

upper_letters_toggle = CTkCheckBox(master=window, variable=include_capital_letters, command=update_characters, text="Uppercase (ABC)", font=(MAIN_FONT, 14), text_color=DARK, border_color=MID, fg_color=MID, hover_color=DARK)
upper_letters_toggle.grid(row=8, column=1, sticky="w")

numbers_toggle = CTkCheckBox(master=window, variable=include_numbers, command=update_characters, text="Numbers (123)", font=(MAIN_FONT, 14), text_color=DARK, border_color=MID, fg_color=MID, hover_color=DARK)
numbers_toggle.grid(row=9, column=1, sticky="w")

symbols_toggle = CTkCheckBox(master=window, variable=include_symbols, command=update_characters, text="Symbols (!@#)", font=(MAIN_FONT, 14), text_color=DARK, border_color=MID, fg_color=MID, hover_color=DARK)
symbols_toggle.grid(row=10, column=1, sticky="w")

update_characters()

# OPTIONS
options_label = CTkLabel(master=window, text="Options", anchor="w", font=(MAIN_FONT, 14, "bold"), text_color=DARK)
options_label.grid(row=12, column=0, sticky="w")

username_toggle = CTkCheckBox(master=window, text="Save username", font=(MAIN_FONT, 14, "bold"), text_color=DARK, border_color=MID, fg_color=MID, hover_color=DARK)
username_toggle.grid(row=12, column=1, sticky="w")

silent_toggle = CTkCheckBox(master=window, text="No popups", font=(MAIN_FONT, 14, "bold"), text_color=DARK, border_color=MID, fg_color=MID, hover_color=DARK)
silent_toggle.grid(row=13, column=1, sticky="w")

window.after(FRAME_DELAY, animation)

window.mainloop()