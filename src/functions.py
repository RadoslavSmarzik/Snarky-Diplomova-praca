from tkinter import *
from tkinter import filedialog
import ttkbootstrap as ttk
from functions_graph import isomorphism_filter_graphs

def color_connect_two_labels(label1, label2):
    label2.config(background=label1.cget("background"))

def create_radiobutton(master, variable, value, row, column):
    radiobutton = ttk.Radiobutton(master=master, variable=variable, value=value, cursor="hand2")
    radiobutton.grid(row = row, column=column)
    return radiobutton

def create_checbox(master, text, variable):
    checkbox = ttk.Checkbutton(master=master, text=text, variable=variable, bootstyle="round-toggle")
    checkbox.pack()
    return checkbox

def create_label(master, text, row, column):
    label = Label(master=master, text=text, font="TkDefaultFont 11")
    label.grid(row=row,column=column)
    return label

def create_highligted_label(master, text, color, row, column, width=None):
    label = Label(master=master, text=text, font="TkDefaultFont 11")
    label.config(width=width, bg=color)
    label.config(relief="flat", borderwidth=5)
    label.grid(row=row, column=column, padx=2, pady=2)
    if width is not None:
        label.config(width=width)
    return label

def set_cursor_hand_for_labels(labels):
    for i in range(len(labels)):
        for j in range(len(labels[i])):
            labels[i][j].config(cursor="hand2")

def create_selection_label(master, text, color, row, column, width=None):
    label = Label(master=master, text=text, font="TkDefaultFont 11")
    label.config(width=width, cursor="hand2")
    label.config(borderwidth = 5, relief = "flat", background=color, fg="white")
    label.grid(row=row, column=column, padx= 3, pady=3)          # pridal som padding
    if width is not None:
        label.config(width=width)
    return label

def get_int_from_label(label):
    return int(label.cget("text"))

def bind_function_to_label(label, function):
    label.bind("<Button-1>", function)

def save_to_file(graphs):
    graphs = isomorphism_filter_graphs(graphs)  # odfiltrujem izomorfne grafy
    file = filedialog.asksaveasfilename(filetypes=[("txt file", ".txt")], defaultextension=".txt")
    if file is "":
        return
    f = open(file, 'w')
    f.write(str(len(graphs)) + '\n')
    for i in range(len(graphs)):
         f.write(str(i + 1) + '\n')
         f.write(graphs[i].format_string())
    f.close()

def save_to_file_one_graph(graph):
    file = filedialog.asksaveasfilename(filetypes=[("txt file", ".txt")], defaultextension=".txt")
    if file is "":
        return
    f = open(file, 'w')
    f.write(graph.format_string())
    f.close()

def create_button(master, text, row, column, command = None):
    button = ttk.Button(master=master, text=text, command=command)
    button.grid(row=row, column=column, padx=10, pady=5,sticky="w")
    return button

def bind_function_to_button(button, function):
    button.config(command=function)

def create_combo_box(master, row, column, function = None):
    s = ttk.Style()
    s.configure('my.TCombobox', font=('TkDefaultFont', 11))

    n = ttk.StringVar()
    combo_box = ttk.Combobox(master=master, width=5, textvariable=n, style="my.TCombobox")
    combo_box.bind("<<ComboboxSelected>>", function)
    combo_box.grid(row=row, column=column, padx=10, pady=5, sticky="w")
    return combo_box

def bind_function_to_combo_box(combo_box, function):
    combo_box.bind("<<ComboboxSelected>>", function)

def create_frame(master, row, column):
    frame = ttk.Frame(master=master)
    frame.grid(row=row, column=column, sticky=W + N, padx=10)
    return frame

# funkcia na vytvorenie scrollovatelneho framu
def create_scrollbar_frame(master, row, column):
    main_frame = ttk.Frame(master=master, borderwidth=2, relief="solid", width=250)
    main_frame.grid(row=row, column=column, padx=10,pady=5,sticky="w")

    scrollbar = ttk.Scrollbar(main_frame, bootstyle="danger-round")
    scrollbar.grid(row=0, column=1, sticky=N + S + W + E)

    canvas = Canvas(main_frame, yscrollcommand=scrollbar.set, width=250)
    canvas.grid(row=0, column=0, sticky=N + S + E + W)
    scrollbar.config(command=canvas.yview)

    frame_in_canvas = ttk.Frame(canvas)
    frame_in_canvas.rowconfigure(1, weight=1)
    canvas.create_window(0, 0, anchor=NW, window=frame_in_canvas, width=250)

    frame_in_canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    frame_in_canvas.bind('<Enter>', lambda e, c=canvas: _bound_to_mousewheel(c))
    frame_in_canvas.bind('<Leave>', lambda e, c=canvas: _unbound_to_mousewheel(canvas))

    return Scrollbar_wrapper(frame_in_canvas, canvas, scrollbar, main_frame)

# 3 funkcie potrebne k tomu aby sme mohli v scrollovatelnom fame scrollovat aj pomocou kolieska mysky
def _bound_to_mousewheel(canv):
    canv.bind_all("<MouseWheel>", lambda e, c = canv: _on_mousewheel(e,c))

def _unbound_to_mousewheel(canv):
    canv.unbind_all("<MouseWheel>")

def _on_mousewheel(event, canv):
    canv.yview_scroll(int(-1 * (event.delta / 120)), "units")


# Trieda, v ktorej su ulozene veci k scrollovatelnemu framu
# frame in canvas - je frame, ktory je v canvase
# main_frame - je hlavny frame v ktorom je vsetko (pravdepodobne ho nepotrebujeme pouzivat)
# AKO TO FUNGUJE:
# Funguje to tak, ze vytvorime main_frame, do main_framu vytvorime canvas a scrollbar, ktory bude hybat s canvasom
# nakoniec do canvasu vlozime frame (frame_in_canvas) a nim pokryjeme cely canvas
# tym padom veci budeme vzdy vkladat do frame_in_canvas
class Scrollbar_wrapper():

    def __init__(self, frame_in_canvas, canvas, scrollbar, main_frame):
        self.frame_in_canvas = frame_in_canvas
        self.canvas = canvas
        self.scrollbar = scrollbar
        self.main_frame = main_frame





