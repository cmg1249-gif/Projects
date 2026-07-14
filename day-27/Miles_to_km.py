"""
A simple program to convert miles to kilometers. Created w/ python and Tkinter library.
"""

from tkinter import *

def calculate():
    try:
        miles = int(input.get())
        km = miles * 1.60934
        label_answer.config(text=str(km))
        return km
    except:
        return 0
# Setting up the window
window = Tk()
window.title("Mile to Km Converter")
window.minsize(50, 50)
window.config(padx=50, pady=30)

# SETTING UP WIDGETS

# Entry

input = Entry(width=10)
input.insert(END, "0")
input.grid(row=0, column=1)

#Labels
label_1 = Label(text="Miles")
label_1.grid(row=0, column=2)

label_2 = Label(text="is equal to")
label_2.grid(row=1, column=0)

label_answer = Label(text="0")
label_answer.grid(row=1, column=1)

label_3 = Label(text="Km")
label_3.grid(row=1, column=2)


#Button
button = Button(text="Calculate" ,command=calculate)
button.grid(row=3, column=1)

window.mainloop()
