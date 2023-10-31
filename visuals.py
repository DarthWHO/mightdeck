import tkinter.scrolledtext as tkscrolled
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import os

class PlayArea():
    def __init__(self, parent, row, column, colour, bgcolour):
        self.parent = parent
        self.row = row
        self.column = column
        self.colour = colour
        self.bordercolor = colour
        style.configure(f'Frame{self.colour}.TFrame', bordercolor="black")
        style.configure('TSpinbox', selectbackground='black')
        style.configure(f'Spin{self.colour}.TSpinbox', bordercolor=self.bordercolor)        
        self.header = create_frame(self.parent, column_width, action_header_height, 0, self.column, 3, 2, 'raised', 1)
        self.header.configure(style=f'Frame{self.colour}.TFrame')
        self.card_area = create_frame(self.parent, column_width, action_height, 1, self.column, 3, 2, 'ridge', 1, rowconfig=9, columnconfig=2)
        self.card_area.configure(style=f'Frame{self.colour}.TFrame')
        self.info = create_label(self.header, "initialize", 0, 0, 5, 5, sticky=NW, font=("Consolas", 11))
        self.info.grid(rowspan=3)
        self.spin = Spinbox(self.header, from_=0, to=18, width=2, font=("Terminal", 12))
        self.spin['style'] = f'Spin{self.colour}.TSpinbox'
        self.spin.grid(row=0, column=1)
        self.btn_shuffle = Button(self.header, text="Shuffle")
        self.btn_shuffle.grid(row=1, column=1, padx=5, pady=5)
        self.btn_draw = Button(self.header, text="No Crits")
        self.btn_draw.grid(row=2, column=1, padx=5,pady=5)

class DrawCard():
    def __init__(self, parent, row, column, colour, bgcolour, text):
        self.parent = parent
        self.row = row
        self.column = column
        self.colour = colour
        self.bgcolour = bgcolour
        self.text = text
        self.card = create_frame(self.parent, 115, 40, self.row, self.column, 2, 2, 'solid', 2, sticky='NW')
        style.configure(f'FrameCard{self.colour}.TFrame', bordercolor=self.colour)
        self.card.configure(style=f'FrameCard{self.colour}.TFrame')
        self.info = create_label(self.card, text, 0, 0, 5, 5, font=("Consolas", 14))
      
# Function to create frames use ttk
def create_frame(parent, width, height, row, column, padx=0, pady=0, relief='', borderwidth=0, sticky='', rowconfig=0, columnconfig=0):
    frame = ttk.Frame(parent, width=width, height=height, relief=relief, borderwidth=borderwidth)
    frame.grid(row=row,column=column, padx=padx, pady=pady, stick=sticky)
    frame.grid_propagate(FALSE)
    frame.grid_columnconfigure(columnconfig, weight=1)
    frame.grid_rowconfigure(rowconfig, weight=1)
    return frame

# Function to create labels use ttk
def create_label(parent, text, row, column, padx=0, pady=0, sticky=(), font=("Consolas", 10)):
    label = ttk.Label(parent, text=text, font=font)
    label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    return label

def create_label_place(parent, text, font=("Consolas", 25)):
    label = ttk.Label(parent, text=text, font=font)
    label.place(anchor=CENTER, relx = .5, rely = .5)
    return label

# Function to update the status window for logging and history
def update_status(text):
    status_text.delete(1.0, END)
    status_text.insert(END, text)

def update_deck_status(play_area, text):
    label = play_area.info.config(text = text)

# Setup the main window parameters, themes and overall size guidelines
window_width = 1000
columns = 4
column_width = (window_width / columns) - 5
header_height = 40
info_height = 110
action_header_height = 150
action_height = 400
root = Tk() 
root.title("Oathsworn Digital Might Deck")
root.geometry("1200x700")
# root.tk.call('source', '_internal/awthemes-10.4.0/awthemes.tcl')
dir_path = os.path.dirname(os.path.realpath(__file__))
root.tk.call('source', os.path.join(dir_path, 'awthemes-10.4.0/awthemes.tcl'))
style = ttk.Style()
# print(style.theme_names())
style.theme_use('awdark')
white_colour = "white"
yellow_colour = "yellow"
red_colour = "red"
black_colour = "black"
main_frame = create_frame(root, window_width, 700, 0, 0)

# Generate the status frame on the right side of the screen and prevent accidental typing into it.
status_frame = create_frame(root, 200, 700, 0, 1, 0, 0, 'groove', 1)
status_text = tkscrolled.ScrolledText(status_frame, font=("Consolas", 10))
status_text.bind("<Key>", lambda e: "break")
status_text.grid(row=0, column=0, sticky=NSEW)

# Generate the header 
header_frame = create_frame(main_frame, window_width, header_height, 0, 0)
header_label = create_label_place(header_frame, "Welcome to the Oathsworn Digital Might Deck!")

# Generate the information and main game information area
instructions = """INSTRUCTIONS:
    - Select how many to draw from each deck. Click Draw All.
    - Click on End Draw to clear the drawn cards
    - Click on shuffle to manually shuffle a deck 
    - CRIT: if a crit is drawn, be sure to draw additional cards - misses will not count"""
info_frame = create_frame(main_frame, window_width, info_height, 1, 0, padx=2, pady=2)
info_frame_ins = create_frame(info_frame, 700, info_height, 0, 0)
info_frame_result = create_frame(info_frame, 150, info_height, 0, 1)
info_frame_buttons = create_frame(info_frame, 150, info_height, 0, 2)
info_label = create_label(info_frame_ins, instructions, 0, 0, 5, 5, sticky=NW)

# Generate the result area and the buttons for drawing and ending a draw
result_text = create_label(info_frame_result, "", 0, 0, 5, 5, font=("Consolas", 12))
btn_draw_all = Button(info_frame_buttons, text="Draw All")
btn_draw_all.grid(row=0, column=0,sticky=E, padx=2)
style.configure('TButton', font=(None, 10))
btn_end_draw = Button(info_frame_buttons, text="End Draw")
btn_end_draw.grid(row=0, column=1,sticky=E, padx=2)

# Setup the main action areas for the cards that will be drawn
action_frame = create_frame(main_frame, window_width, 700 - (header_height + info_height), 2, 0, columnconfig=4)
white_area = PlayArea(action_frame, 0, 0, white_colour, white_colour)
yellow_area = PlayArea(action_frame, 0, 1, yellow_colour, yellow_colour)
red_area = PlayArea(action_frame, 0, 2, red_colour, red_colour)
black_area = PlayArea(action_frame, 0, 3, black_colour, black_colour)
