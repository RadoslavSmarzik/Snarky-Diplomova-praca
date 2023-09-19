from tkinter import *
from tkinter import ttk
from functions import create_button
from page_construction_1 import Page_construction_1
from page_construction_2 import Page_construction_2
from page_dipol_1 import Page_dipol_1
from page_dipol_2 import Page_dipol_2
from page_dot_product import Page_dot_product
from page_find_2factor import Page_find_2factor
from page_image_of_kvocient import Page_image_of_kvocient
from page_star_product import Page_star_product

# trieda pre hlavnu obrazovku
class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        # nastavim font pre vsetky ttk widgety
        s = ttk.Style()
        s.configure('.', font=('TkDefaultFont', 11))

        self.page_dot_product = Page_dot_product(self)
        self.page_star_product = Page_star_product(self)
        self.page_construction_1 = Page_construction_1(self)
        self.page_construction_2 = Page_construction_2(self)
        self.page_dipol_1 = Page_dipol_1(self)
        self.page_dipol_2 = Page_dipol_2(self)
        self.page_image_of_kvocient = Page_image_of_kvocient(self)
        self.page_find_2factor = Page_find_2factor(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False, pady=(0,50))
        container.pack(side="top", fill="both", expand=True)

        self.page_dot_product.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.page_star_product.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.page_construction_1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.page_construction_2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.page_dipol_1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.page_dipol_2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.page_image_of_kvocient.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.page_find_2factor.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.button1 = create_button(buttonframe, "pem 4-súčin", 0, 0, command=self.button1_function)
        self.button2 = create_button(buttonframe, "perm 5-súčin", 0, 1, command=self.button2_function)
        self.button3 = create_button(buttonframe, "konštrukcia 1", 0, 2, command=self.button3_function)
        self.button4 = create_button(buttonframe, "konštrukcia 2", 0, 3, command=self.button4_function)
        self.button5 = create_button(buttonframe, "vkladanie inv dipólu", 0, 4, command=self.button5_function)
        self.button6 = create_button(buttonframe, "vkladanie perm dipólov", 0, 5, command=self.button6_function)
        self.button7 = create_button(buttonframe, "kvocient", 0, 6, command=self.button7_function)
        self.button8 = create_button(buttonframe, "perm 2-faktory", 0, 7, command=self.button8_function)

        self.button1_function()

    def button1_function(self):
        self.reset_button_colors()
        self.button1.config(bootstyle="success")
        self.page_dot_product.show()

    def button2_function(self):
        self.reset_button_colors()
        self.button2.config(bootstyle="success")
        self.page_star_product.show()

    def button3_function(self):
        self.reset_button_colors()
        self.button3.config(bootstyle="success")
        self.page_construction_1.show()

    def button4_function(self):
        self.reset_button_colors()
        self.button4.config(bootstyle="success")
        self.page_construction_2.show()

    def button5_function(self):
        self.reset_button_colors()
        self.button5.config(bootstyle="success")
        self.page_dipol_1.show()

    def button6_function(self):
        self.reset_button_colors()
        self.button6.config(bootstyle="success")
        self.page_dipol_2.show()

    def button7_function(self):
        self.reset_button_colors()
        self.button7.config(bootstyle="success")
        self.page_image_of_kvocient.show()

    def button8_function(self):
        self.reset_button_colors()
        self.button8.config(bootstyle="success")
        self.page_find_2factor.show()

    def reset_button_colors(self):
        self.button1.config(bootstyle="primary")
        self.button2.config(bootstyle="primary")
        self.button3.config(bootstyle="primary")
        self.button4.config(bootstyle="primary")
        self.button5.config(bootstyle="primary")
        self.button6.config(bootstyle="primary")
        self.button7.config(bootstyle="primary")
        self.button8.config(bootstyle="primary")