from functools import partial
from tkinter import messagebox
from functions import *
from functions_graph import get_neighbous_of_vertex_without_vertex2
from graph import Edge
from page import Page

# trieda pre permutacny 4-sucin
class Page_dot_product(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_g1_edges_frame()
        self.create_g2_edge_frame()
        self.create_dot_select_connection()

        self.g1_e1_selected_lbl = None
        self.g1_e2_selected_lbl = None
        self.g2_f_selected_lbl = None

        self.selected_selection_lbl = None



        bind_function_to_button(self.result_button, self.function_btn_dot)
        bind_function_to_button(self.result_all_button, self.function_btn_all_dot)


    # vytvori frame v ktorom sa zobrazuju oznacene hrany e1 a e2 z grafu G1
    def create_g1_edges_frame(self):
        frame = create_frame(self.g1_main_frame, 3, 0)
        #create_label(frame, text="Hrana e1:", row=0, column=0)  #vyriesit padingy
        #create_label(frame, text="Hrana e2:", row=1, column=0)

        self.lbl_g1_e1u = create_label(frame, "", 0, 1)  # vyriesit width a sticky
        self.lbl_g1_e1v = create_label(frame, "", 0,2)
        self.lbl_g1_e2u = create_label(frame, "", 1, 1)
        self.lbl_g1_e2v = create_label(frame, "", 1, 2)

        # nechcem nakoniec zobrazovat
        self.lbl_g1_e1u.grid_forget()
        self.lbl_g1_e1v.grid_forget()
        self.lbl_g1_e2u.grid_forget()
        self.lbl_g1_e2v.grid_forget()

    # vytvori frame v ktorom sa bude zobrazovat hrana f z G2
    def create_g2_edge_frame(self):
        self.frm_g2_edge = create_frame(self.g2_main_frame, 3, 0)
        #create_label(self.frm_g2_edge, "Hrana f:", 0, 0)

        self.lbl_g2_fu = create_label(self.frm_g2_edge, "", 0, 1)
        self.lbl_g2_fv = create_label(self.frm_g2_edge, "", 0, 2)

        self.lbl_g2_fu.grid_forget()
        self.lbl_g2_fv.grid_forget()

    # vytvori frame v ktorom sa bude vyberat presne prepojenie
    def create_dot_select_connection(self):
        frm_select_connection = create_frame(self.g3_main_frame, 2, 0)

        self.lbl_e1_u = create_selection_label(frm_select_connection, "e1_u:", "green", 0, 0, 8) # padding
        self.lbl_e1_v = create_selection_label(frm_select_connection, "e1_v:", "orange", 1, 0, 8)
        self.lbl_e2_u = create_selection_label(frm_select_connection, "e2_u:", "purple", 2, 0, 8)
        self.lbl_e2_v = create_selection_label(frm_select_connection, "e2_v:", "gray", 3, 0, 8)

        self.lbl_f_u_1 = create_selection_label(frm_select_connection, "f_u_1:", "green", 0, 1, 8)
        self.lbl_f_u_2 = create_selection_label(frm_select_connection, "f_u_2:", "orange", 1, 1, 8)
        self.lbl_f_v_1 = create_selection_label(frm_select_connection, "f_v_1:", "purple", 2, 1, 8)
        self.lbl_f_v_2 = create_selection_label(frm_select_connection, "f_v_2:", "gray", 3, 1, 8)

        left_labels = [self.lbl_e1_u, self.lbl_e1_v, self.lbl_e2_u, self.lbl_e2_v]

        bind_function_to_label(self.lbl_e1_u, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.lbl_e1_v, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.lbl_e2_u, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.lbl_e2_v, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))

        bind_function_to_label(self.lbl_f_u_1, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.lbl_f_u_2, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.lbl_f_v_1, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.lbl_f_v_2, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))

    # metoda zvyrazni label a nastavi v aplikacii, ze bola vybrana hrana vertex1 - vertex2 pre G1
    def g1_switch_selected_edge(self, event, vertex1, vertex2, label):
        # hned skonci, ak si chcel kliknut na priecku
        if self.label_is_spoke(label):
            return

        # ak label bol zvyrazneny ako hrana e1, tak ho odznac a vynuluj
        if label is self.g1_e1_selected_lbl:
            label.config(relief="flat")
            self.lbl_g1_e1u.config(text="")
            self.lbl_g1_e1v.config(text="")
            self.g1_e1_selected_lbl = None
            self.lbl_e1_u.config(text="e1_u:")
            self.lbl_e1_v.config(text="e1_v:")
            return

        # ak label bol zvyrazneny ako hrana e2, tak ho odznac a vynuluj
        if label is self.g1_e2_selected_lbl:
            label.config(relief="flat")
            self.lbl_g1_e2u.config(text="")
            self.lbl_g1_e2v.config(text="")
            self.g1_e2_selected_lbl = None
            self.lbl_e2_u.config(text="e2_u:")
            self.lbl_e2_v.config(text="e2_v:")
            self.e2_u = None
            self.e2_v = None
            return

        # ak je hrana e1 prazdna, tak ju nastav na hranu vertex1 - vertex2
        # ak nie je tak prepis hranu e2, nech bola alebo nebola oznacena
        if self.g1_e1_selected_lbl is None:
            # musim povolit, ze ak nahodou e2 je stale zvolena, tak musim dat pozor na farbu
            if self.g1_e2_selected_lbl is not None:
                if self.labels_have_same_color(label, self.g1_e2_selected_lbl):
                    return
            self.lbl_g1_e1u.config(text=str(vertex1))
            self.lbl_g1_e1v.config(text=str(vertex2))
            self.g1_e1_selected_lbl = label
            self.lbl_e1_u.config(text="e1_u: " + str(vertex1))
            self.lbl_e1_v.config(text="e1_v: " + str(vertex2))
        else:
            # tu idem kludne prepisat hranu e2, ale tiez musim dat pozor aby nemala rovnaku farbu ako e1
            if self.labels_have_same_color(label, self.g1_e1_selected_lbl):
                return

            # tu sa ide nastavovat e2
            if self.g1_e2_selected_lbl is not None:
                self.g1_e2_selected_lbl.config(relief="flat")
            self.g1_e2_selected_lbl = label
            self.lbl_g1_e2u.config(text=str(vertex1))
            self.lbl_g1_e2v.config(text=str(vertex2))
            self.lbl_e2_u.config(text="e2_u: " + str(vertex1))
            self.lbl_e2_v.config(text="e2_v: " + str(vertex2))
            self.e2_u = vertex1
            self.e2_v = vertex2

        # zvyrazni label
        label.config(relief="solid")

    # metoda pre preoznacenie hrany f v grafe G2
    def g2_switch_selected_edge(self, event, vertex1, vertex2, label):
        # ak nahodou nie je priecka, tak hned koniec
        if not self.label_is_spoke(label):
            return

        # ak bol nejaky selected label tak ho odznacim
        if self.g2_f_selected_lbl is not None:
            self.g2_f_selected_lbl.config(relief="flat")

        # ak som klikol na taky, co uz predtym bol tak ho odznacim a skoncim
        if self.g2_f_selected_lbl is label:
            self.lbl_g2_fu.config(text="")
            self.lbl_g2_fv.config(text="")
            self.g2_f_selected_lbl = None
            self.lbl_f_u_1.config(text="f_u_1: ")
            self.lbl_f_u_2.config(text="f_u_2: ")
            self.lbl_f_v_1.config(text="f_v_1: ")
            self.lbl_f_v_2.config(text="f_v_2: ")
            return

        # inac zvyraznim ten na ktory som klikol
        self.g2_f_selected_lbl = label
        label.config(relief="solid")
        self.lbl_g2_fu.config(text=str(vertex1))
        self.lbl_g2_fv.config(text=str(vertex2))
        f_u = vertex1
        f_v = vertex2
        f_u_neighbours = self.G2.get_neighbours_of_vertex(f_u)
        f_u_neighbours.remove(f_v)
        f_u_1 = f_u_neighbours[0]
        f_u_2 = f_u_neighbours[1]

        f_v_neighbours = self.G2.get_neighbours_of_vertex(f_v)
        f_v_neighbours.remove(f_u)
        f_v_1 = f_v_neighbours[0]
        f_v_2 = f_v_neighbours[1]
        self.lbl_f_u_1.config(text="f_u_1: " + str(f_u_1))
        self.lbl_f_u_2.config(text="f_u_2: "+ str(f_u_2))
        self.lbl_f_v_1.config(text="f_v_1: "+ str(f_v_1))
        self.lbl_f_v_2.config(text="f_v_2: "+ str(f_v_2))

    # funkcia skontroluje, ci je nacitane vsetko potrebne pre vykonanie productu
    def check_if_you_can_execute(self):
        if self.G1.adjacency_list is None:
            messagebox.showerror('CHYBA', 'Chyba G1')
            return False
        if len(self.G1.twoFactors) == 0:
            messagebox.showerror('CHYBA', 'Chyba G1 2-faktory')
            return False
        if self.G2.adjacency_list is None:
            messagebox.showerror('CHYBA', 'Chyba G2')
            return False
        if len(self.G2.twoFactors) == 0:
            messagebox.showerror('CHYBA', 'Chyba G2 2-faktory')
            return False

        if self.lbl_g1_e1u.cget("text") =="" or self.lbl_g1_e1v.cget("text") =="":
            messagebox.showerror('CHYBA', 'Zvolte hranu e1 v G1')
            return False

        if self.lbl_g1_e2u.cget("text") =="" or self.lbl_g1_e2v.cget("text") =="":
            messagebox.showerror('CHYBA', 'Zvolte hranu e2 v G1')
            return False

        if self.lbl_g2_fu.cget("text") == "" or self.lbl_g2_fv.cget("text") == "":
            messagebox.showerror('CHYBA', 'Zvolte priečku f v G2')
            return False

        return True

    # metoda, ktora vykona 1 dotproduct (podla selekcie) a vysledok zapise na obrazovku
    def function_btn_dot(self):
        if self.check_if_you_can_execute() == False:
            return
        e1_u = int(self.lbl_g1_e1u.cget("text"))
        e1_v = int(self.lbl_g1_e1v.cget("text"))
        e2_u = int(self.lbl_g1_e2u.cget("text"))
        e2_v = int(self.lbl_g1_e2v.cget("text"))

        array_of_labels = [self.lbl_f_u_1, self.lbl_f_u_2, self.lbl_f_v_1, self.lbl_f_v_2]
        f_u_1 = self.get_int_from_labels_by_color(array_of_labels, "green")
        f_u_2 = self.get_int_from_labels_by_color(array_of_labels, "orange")
        f_v_1 = self.get_int_from_labels_by_color(array_of_labels, "purple")
        f_v_2 = self.get_int_from_labels_by_color(array_of_labels, "gray")

        f = Edge(int(self.lbl_g2_fu.cget("text")), int(self.lbl_g2_fv.cget("text")))
        self.G3 = self.G1.do_dot_product(self.G2, e1_u, e1_v, e2_u, e2_v, f, f_u_1, f_u_2, f_v_1, f_v_2)
        self.write_g3_to_frame()
        save_to_file_one_graph(self.G3)

    # funkcia, ktora vykona vsetky mozne 4suciny a zapise ich do suboru
    def function_btn_all_dot(self):
        if self.check_if_you_can_execute() == False:
            return
        e1_u = get_int_from_label(self.lbl_g1_e1u)
        e1_v = get_int_from_label(self.lbl_g1_e1v)
        e2_u = get_int_from_label(self.lbl_g1_e2u)
        e2_v = get_int_from_label(self.lbl_g1_e2v)
        f_u = get_int_from_label(self.lbl_g2_fu)
        f_v = get_int_from_label(self.lbl_g2_fv)

        f = Edge(f_u, f_v)

        f_u_neighbours = get_neighbous_of_vertex_without_vertex2(self.G2, f_u, f_v)
        f_u_1 = f_u_neighbours[0]
        f_u_2 = f_u_neighbours[1]

        f_v_neighbours = get_neighbous_of_vertex_without_vertex2(self.G2, f_v, f_u)
        f_v_1 = f_v_neighbours[0]
        f_v_2 = f_v_neighbours[1]

        ###             e_1 - f_u             ###
        # e1_u - f_u_1,  e1_v - f_u_2, e2_u - f_v_1, e2_v - f_v_2
        dot1 = self.G1.do_dot_product(self.G2, e1_u, e1_v, e2_u, e2_v, f, f_u_1, f_u_2, f_v_1, f_v_2)
        # e1_u - f_u_1,  e1_v - f_u_2, e2_u - f_v_2, e2_v - f_v_1
        dot2 = self.G1.do_dot_product(self.G2, e1_u, e1_v, e2_u, e2_v, f, f_u_1, f_u_2, f_v_2, f_v_1)

        # e1_u - f_u_2,  e1_v - f_u_1, e2_u - f_v_1, e2_v - f_v_2
        dot3 = self.G1.do_dot_product(self.G2, e1_u, e1_v, e2_u, e2_v, f, f_u_2, f_u_1, f_v_1, f_v_2)
        # e1_u - f_u_2,  e1_v - f_u_1, e2_u - f_v_2, e2_v - f_v_1
        dot4 = self.G1.do_dot_product(self.G2, e1_u, e1_v, e2_u, e2_v, f, f_u_2, f_u_1, f_v_2, f_v_1)

        ###             e_2 - f_u             ###
        # e2_u - f_u_1,  e2_v - f_u_2, e1_u - f_v_1, e1_v - f_v_2
        dot5 = self.G1.do_dot_product(self.G2, e2_u, e2_v, e1_u, e1_v, f, f_u_1, f_u_2, f_v_1, f_v_2)
        # e2_u - f_u_1,  e2_v - f_u_2, e1_u - f_v_2, e1_v - f_v_1
        dot6 = self.G1.do_dot_product(self.G2, e2_u, e2_v, e1_u, e1_v, f, f_u_1, f_u_2, f_v_2, f_v_1)
        # e2_u - f_u_2,  e2_v - f_u_1, e1_u - f_v_1, e1_v - f_v_2
        dot7 = self.G1.do_dot_product(self.G2, e2_u, e2_v, e1_u, e1_v, f, f_u_2, f_u_1, f_v_1, f_v_2)
        # e2_u - f_u_2,  e2_v - f_u_1, e1_u - f_v_2, e1_v - f_v_1
        dot8 = self.G1.do_dot_product(self.G2, e2_u, e2_v, e1_u, e1_v, f, f_u_2, f_u_1, f_v_2, f_v_1)

        save_to_file([dot1,dot2,dot3,dot4,dot5,dot6,dot7,dot8])

    def get_int_from_labels_by_color(self, labels, color):
        for l in labels:
            if l.cget("background") == color:
                return int(l.cget("text")[6:])

    def do_correct_connections(self, label1, label2):
        label2.config(background=label1.cget("background"))
        if label1 == self.lbl_e1_u:

            if label2 == self.lbl_f_u_1:
                self.color_connect_two_labels(self.lbl_e1_v, self.lbl_f_u_2)
                self.do_correct_reconnection(self.lbl_e2_u, self.lbl_e2_v, self.lbl_f_v_1, self.lbl_f_v_2)
            elif label2 == self.lbl_f_u_2:
                self.color_connect_two_labels(self.lbl_e1_v, self.lbl_f_u_1)
                self.do_correct_reconnection(self.lbl_e2_u, self.lbl_e2_v, self.lbl_f_v_1, self.lbl_f_v_2)
            elif label2 == self.lbl_f_v_1:
                self.color_connect_two_labels(self.lbl_e1_v, self.lbl_f_v_2)
                self.do_correct_reconnection(self.lbl_e2_u, self.lbl_e2_v, self.lbl_f_u_1, self.lbl_f_u_2)
            elif label2 == self.lbl_f_v_2:
                self.color_connect_two_labels(self.lbl_e1_v, self.lbl_f_v_1)
                self.do_correct_reconnection(self.lbl_e2_u, self.lbl_e2_v, self.lbl_f_u_1, self.lbl_f_u_2)

        elif label1 == self.lbl_e1_v:

            if label2 == self.lbl_f_u_1:
                self.color_connect_two_labels(self.lbl_e1_u, self.lbl_f_u_2)
                self.do_correct_reconnection(self.lbl_e2_u, self.lbl_e2_v, self.lbl_f_v_1, self.lbl_f_v_2)
            elif label2 == self.lbl_f_u_2:
                self.color_connect_two_labels(self.lbl_e1_u, self.lbl_f_u_1)
                self.do_correct_reconnection(self.lbl_e2_u, self.lbl_e2_v, self.lbl_f_v_1, self.lbl_f_v_2)
            elif label2 == self.lbl_f_v_1:
                self.color_connect_two_labels(self.lbl_e1_u, self.lbl_f_v_2)
                self.do_correct_reconnection(self.lbl_e2_u, self.lbl_e2_v, self.lbl_f_u_1, self.lbl_f_u_2)
            elif label2 == self.lbl_f_v_2:
                self.color_connect_two_labels(self.lbl_e1_u, self.lbl_f_v_1)
                self.do_correct_reconnection(self.lbl_e2_u, self.lbl_e2_v, self.lbl_f_v_1, self.lbl_f_v_2)

        elif label1 == self.lbl_e2_u:

            if label2 == self.lbl_f_u_1:
                self.color_connect_two_labels(self.lbl_e2_v, self.lbl_f_u_2)
                self.do_correct_reconnection(self.lbl_e1_u, self.lbl_e1_v, self.lbl_f_v_1, self.lbl_f_v_2)
            elif label2 == self.lbl_f_u_2:
                self.color_connect_two_labels(self.lbl_e2_v, self.lbl_f_u_1)
                self.do_correct_reconnection(self.lbl_e1_u, self.lbl_e1_v, self.lbl_f_v_1, self.lbl_f_v_2)
            elif label2 == self.lbl_f_v_1:
                self.color_connect_two_labels(self.lbl_e2_v, self.lbl_f_v_2)
                self.do_correct_reconnection(self.lbl_e1_u, self.lbl_e1_v, self.lbl_f_u_1, self.lbl_f_u_2)
            elif label2 == self.lbl_f_v_2:
                self.color_connect_two_labels(self.lbl_e2_v, self.lbl_f_v_1)
                self.do_correct_reconnection(self.lbl_e1_u, self.lbl_e1_v, self.lbl_f_u_1, self.lbl_f_u_2)

        elif label1 == self.lbl_e2_v:

            if label2 == self.lbl_f_u_1:
                self.color_connect_two_labels(self.lbl_e2_u, self.lbl_f_u_2)
                self.do_correct_reconnection(self.lbl_e1_u, self.lbl_e1_v, self.lbl_f_v_1, self.lbl_f_v_2)
            elif label2 == self.lbl_f_u_2:
                self.color_connect_two_labels(self.lbl_e2_u, self.lbl_f_u_1)
                self.do_correct_reconnection(self.lbl_e1_u, self.lbl_e1_v, self.lbl_f_v_1, self.lbl_f_v_2)
            elif label2 == self.lbl_f_v_1:
                self.color_connect_two_labels(self.lbl_e2_u, self.lbl_f_v_2)
                self.do_correct_reconnection(self.lbl_e1_u, self.lbl_e1_v, self.lbl_f_u_1, self.lbl_f_u_2)
            elif label2 == self.lbl_f_v_2:
                self.color_connect_two_labels(self.lbl_e2_u, self.lbl_f_v_1)
                self.do_correct_reconnection(self.lbl_e1_u, self.lbl_e1_v, self.lbl_f_u_1, self.lbl_f_u_2)

    def color_connect_two_labels(self, label1, label2):
        label2.config(background=label1.cget("background"))

    # farba z lavych labelov musi byt aj v tych v pravo
    def do_correct_reconnection(self, label_left_1, label_left_2, label_right_1, label_right_2):
        color1 = label_left_1.cget("background")
        color2 = label_left_2.cget("background")
        color3 = label_right_1.cget("background")
        color4 = label_right_2.cget("background")

        if color1 == color3 or color1 == color4:
            if color2 == color3 or color2 == color4:
                return
        self.color_connect_two_labels(label_left_1, label_right_1)
        self.color_connect_two_labels(label_left_2, label_right_2)

    def reset_g1_adding_2factor(self):
        # odznacim labely, ak boli nejake zvyraznene
        if self.g1_e1_selected_lbl is not None:
            self.g1_e1_selected_lbl.config(relief="flat")
        if self.g1_e2_selected_lbl is not None:
            self.g1_e2_selected_lbl.config(relief="flat")

        # nastavim labely na None
        self.g1_e1_selected_lbl = None
        self.g1_e2_selected_lbl = None

        # vymazem napisy
        self.lbl_g1_e1u.config(text="")
        self.lbl_g1_e1v.config(text="")
        self.lbl_g1_e2u.config(text="")
        self.lbl_g1_e2v.config(text="")

        # vynulujem labely na zvolenie
        self.lbl_e1_u.config(text="e1_u:")
        self.lbl_e1_v.config(text="e1_v:")
        self.lbl_e2_u.config(text="e2_u:")
        self.lbl_e2_v.config(text="e2_v:")

    def reset_g2_adding_2factor(self):
        if self.g2_f_selected_lbl is not None:
            self.g2_f_selected_lbl.config(relief="flat")

        self.g2_f_selected_lbl = None

        self.lbl_g2_fu.config(text="")
        self.lbl_g2_fv.config(text="")

        self.lbl_f_u_1.config(text="f_u_1: ")
        self.lbl_f_u_2.config(text="f_u_2: ")
        self.lbl_f_v_1.config(text="f_v_1: ")
        self.lbl_f_v_2.config(text="f_v_2: ")

    def handle_setting_cursor_for_labels(self):
        set_cursor_hand_for_labels(self.g1_array_of_labels)
        set_cursor_hand_for_labels(self.g2_array_of_labels)