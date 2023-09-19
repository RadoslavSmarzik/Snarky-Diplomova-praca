from tkinter.font import Font
import ttkbootstrap as ttk
from main_view import MainView

root = ttk.Window(title="SNARKY", themename="sandstone")
root.state('zoomed')  # root.attributes('-zoomed', True) pre linux

bigfont = Font(family="TkDefaultFont",size=11)
root.option_add("*Font", bigfont)

main = MainView(root)
main.pack(side="top", fill="both", expand=True)
root.minsize(1500,800)
root.wm_geometry("1600x900")
root.mainloop()