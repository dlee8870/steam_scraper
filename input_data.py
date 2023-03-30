from __future__ import annotations
from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("500x500")
root.title("Welcome to Steam Waiter")

input_pf = Entry(root, width=50)
input_pf.pack()

def store_data():
    "Store the data inputed in the textbox into a variable"
    steam_id = input_pf.get()

    # Perhaps call functions to create decision tree

label = Label(root, text="Enter Steam Profile", font=('Arial', 18))
label.pack()

# Enter button to input data
button = Button(root, text='Enter', font=('Arial', 18), command=store_data)
button.pack(pady=10)

# Default text in the input box
input_pf.insert(0, "Enter info here")

# Run the window
root.mainloop()
