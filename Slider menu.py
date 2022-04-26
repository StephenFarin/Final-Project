import tkinter as tk
from tkinter import ttk


# root window
root = tk.Tk()
root.geometry('500x600')
root.resizable(False, False)
root.title('Snake game')


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)


# Snake speed current value
Snake_speed = tk.DoubleVar()


def get_Snake_speed():
    range(5,100,200)
    return '{:.0f}'.format(Snake_speed.get())


def slider_changed(event):
    value_label.configure(text=get_Snake_speed())


# label for the slider
Speed_label = ttk.Label(
    root,
    text='Speed:'
)

Speed_label.grid(
    column=0,
    row=0,
    sticky='w'
)

#  slider
Speed = ttk.Scale(
    root,
    from_=50,
    to=200,
    orient='horizontal',  # vertical
    command=slider_changed,
    variable=Snake_speed
)

Speed.grid(
    column=1,
    row=0,
    sticky='we'
)

# current value label
Snake_speed_label = ttk.Label(
    root,
    text='Snake Speed:'
)

Snake_speed_label.grid(
    row=1,
    columnspan=2,
    sticky='n',
    ipadx=10,
    ipady=10
)

# value label
value_label = ttk.Label(
    root,
    text=get_Snake_speed()
)
value_label.grid(
    row=2,
    columnspan=2,
    sticky='n'
)

root.mainloop()


import tkinter as tk
from tkinter import ttk


# root window
root = tk.Tk()
root.geometry('400x300')
root.resizable(False, False)
root.title('Number of Apples')


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)


# slider current value
Num_apples = tk.DoubleVar()


def get_Num_apples():
    return '{: .0f}'.format(Num_apples.get())


def slider_changed(event):
    value_label.configure(text=get_Num_apples())


# label for the slider
Apples_label = ttk.Label(
    root,
    text='Apples:'
)

Apples_label.grid(
    column=0,
    row=0,
    sticky='w'
)

#  slider horizontal
Apples = ttk.Scale(
    root,
    from_=5,
    to=10,
    orient='horizontal',  
    command=slider_changed,
    variable=Num_apples
)

Apples.grid(
    column=1,
    row=0,
    sticky='we'
)

# current value label
Num_apples_label = ttk.Label(
    root,
    text='Number of Apples:'
)

Num_apples_label.grid(
    row=1,
    columnspan=2,
    sticky='n',
    ipadx=10,
    ipady=10
)

# value label
value_label = ttk.Label(
    root,
    text=get_Num_apples()
)
value_label.grid(
    row=2,
    columnspan=2,
    sticky='n'
)


root.mainloop()

