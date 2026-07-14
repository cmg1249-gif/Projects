from tkinter import *

def button_clicked():
	print("I got clicked")
	new_text = input.get()
	my_label.config(text=new_text)

window = Tk()
window.title('My Python tkinter app')
window.minsize(500, 300)
window.config(padx=20, pady=20)

# Label
my_label = Label(text="Dawg, this is a Label", font=("Arial", 25, "bold"))
my_label.config(text="new text")
my_label.grid(column=0, row=0)





# Button


button = Button(text="Click Me", command=button_clicked)
button.grid(column=1, row=1)
button1 = Button(text="Srlsy Click me hard", command=button_clicked)
button1.grid(column=2, row=0)
# Entry

input = Entry(width=10)
print(input.get())
input.grid(column=3, row=2)


window.mainloop()