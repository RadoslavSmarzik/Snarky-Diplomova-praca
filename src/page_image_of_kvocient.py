from functools import partial
from tkinter import messagebox
from functions import *
from page import Page
import os
import math
import cairo

# trieda pre generovanie kvocientu ku involucnemu snarku
class Page_image_of_kvocient(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_inv_combo_boxes()

        self.g2_main_frame.destroy()
        self.g3_scrollbar_wrapper.main_frame.destroy()
        self.result_all_button.destroy()
        bind_function_to_button(self.g1_button_add_2factors, partial(self.function_load_2factor_g1, self.G1, self.g1_combo_box, self.g1_array_of_labels))
        bind_function_to_button(self.result_button, self.handle_saving_and_creating_image)

        self.g1_involutions_for_current_2factor = []
        self.current_involution = None

    def function_load_2factor_g1(self, graph, combo_box, array_of_labels):
        self.function_load_2factors_from_file(graph, combo_box, array_of_labels, filter_involution_2_factors=True)
        self.set_involution(graph)

    # pozeram ci nahodou selected 2factor nie je None (None je napriklad vtedy ked nahravam novy file 2faktorov)
    def set_involution(self, graph):
        if graph.selected_2factor is None:
            return
        self.g1_involutions_for_current_2factor = graph.find_all_involutions_for_twoFactor(graph.selected_2factor)
        self.combo_box_g1_inv["values"] = self.create_values_for_inv_combo_box(self.g1_involutions_for_current_2factor)
        self.combo_box_g1_inv.current(0)

        self.current_involution = self.g1_involutions_for_current_2factor[0]

    def handle_saving_and_creating_image(self):
        if self.check_if_you_can_execute() == False:
            return
        filename = filedialog.asksaveasfilename(filetypes=[("txt file", ".txt")], defaultextension=".txt")
        if filename is "":
            return
        involution_cycles = self.current_involution
        involution = self.G1.create_permutation(involution_cycles[0], involution_cycles[1])
        self.save_kvocient_txt(filename,involution)
        self.create_image_of_kvocient(filename,involution)

    def get_array_of_chords(self, involution):
        array = []
        for cycle in involution:
            if len(cycle) == 2:
                array.append(cycle)
        return array

    def create_string_of_perm_cycle(self, cycle):
        string = ""
        for i in range(len(cycle)):
            string += str(cycle[i])
            if i < len(cycle) - 1:
                string += " "
        return string

    def create_string_of_involution_part(self, involution):
        string_of_involution = ""

        for cycle in involution:
            string_of_involution += "("
            string_of_involution += self.create_string_of_perm_cycle(cycle)
            string_of_involution += ")"

        return string_of_involution

    def break_array_into_muliple_arrays(self, array):
        new_array = []
        start = 0
        end = len(array)
        step = 7
        for i in range(start, end, step):
            x = i
            new_array.append(array[x:x + step])
        return new_array

    def create_multiple_strings_of_involution(self, involution):
        array_of_strings = []
        multiple_arrays = self.break_array_into_muliple_arrays(involution)
        for i in range(len(multiple_arrays)):
            string = self.create_string_of_involution_part(multiple_arrays[i])
            array_of_strings.append(string)
        return array_of_strings

    def add_involution_text_to_image(self, context, involution):
        strings_of_involution = self.create_multiple_strings_of_involution(involution)

        context.set_font_size(35)

        for i in range(len(strings_of_involution)):
            part = strings_of_involution[i]
            xbearing, ybearing, width, height, dx, dy = context.text_extents(part)
            context.move_to(400 - (width / 2), 850 + i*35)
            context.show_text(part)

    def create_image_of_kvocient(self, file_name, involution):

        # iba do velkosti involucnych snarkov radu 100
        number_of_points = 2 * len(involution) - 1
        if number_of_points > 50:
            # prilis velky snark na obrazok kvocientu DOPLNIT
            return

        center_x = 400
        center_y = 400
        radius = 250
        if number_of_points > 25:
            radius = 350

        x_coords = []
        y_coords = []
        array_of_chords = self.get_array_of_chords(involution)

        svg_file_name = self.get_file_name_without_extension(file_name)+'.svg'

        with cairo.SVGSurface(svg_file_name, 800, 1000) as surface:
            # creating a cairo context object
            context = cairo.Context(surface)

            context.arc(center_x, center_y, radius, 0, 2 * math.pi)
            context.stroke()
            context.set_font_size(30)

            for i in range(number_of_points):
                x = radius * math.cos(math.radians(270 + i * (360 / number_of_points))) + center_x
                y = radius * math.sin(math.radians(270 + i * (360 / number_of_points))) + center_y
                context.arc(x, y, 10, 0, 2 * math.pi)
                context.fill()
                x_coords.append(x)
                y_coords.append(y)
                x2 = (radius + 35) * math.cos(math.radians(270 + i * (360 / number_of_points))) + center_x
                y2 = (radius + 35) * math.sin(math.radians(270 + i * (360 / number_of_points))) + center_y
                s = str(i)
                xbearing, ybearing, width, height, dx, dy = context.text_extents(s)
                context.move_to(x2 - (dx / 2), y2 + (height / 2))
                context.show_text(s)

            for chorda in array_of_chords:
                context.move_to(x_coords[chorda[0]], y_coords[chorda[0]])
                context.line_to(x_coords[chorda[1]], y_coords[chorda[1]])
                context.stroke()

            self.add_involution_text_to_image(context, involution)

            context.move_to(x_coords[0], y_coords[0])
            context.line_to(x_coords[0], y_coords[0] - 20)
            context.stroke()

            context.scale(800, 1000)

            surface.write_to_png(self.get_file_name_without_extension(file_name)+'.png')

    def get_file_name_without_extension(self, file_name):
        split = os.path.splitext(file_name)
        return split[0]

    def change_involution_from_combo_box(self, e, graph):
        index = e.widget.current()

        if graph is self.G1:
            self.current_involution = self.g1_involutions_for_current_2factor[index]

    def reset_g1_adding_2factor(self):
        self.g1_involutions_for_current_2factor = []
        self.combo_box_g1_inv["values"] = []
        self.combo_box_g1_inv.set("")

        self.set_involution(self.G1)

    def chord_neighbour_of_vertex(self, vertex, involution):
        for i in range(len(involution)):
            if len(involution[i]) == 2:
                if involution[i][0] == vertex:
                    return involution[i][1]
                if involution[i][1] == vertex:
                    return involution[i][0]

    # beriem, ze 0 nema chord suseda
    def create_kvocient_string(self, involution):
        number_of_points = 2 * len(involution) - 1
        string = str(number_of_points)+ "\n"
        for i in range(number_of_points):
            neighbour_before = i-1 if i>0 else number_of_points - 1
            neighbour_after = i+1 if i<number_of_points-1 else 0
            string += str(neighbour_before) + " " + str(neighbour_after)
            if i != 0:
                string += " " + str(self.chord_neighbour_of_vertex(i, involution))
            string += "\n"
        return string

    def save_kvocient_txt(self,filename, involution):
        string = self.create_kvocient_string(involution)
        file = open(filename, "w")
        file.write(string)
        file.close()

    def check_if_you_can_execute(self):
        if self.G1.adjacency_list is None:
            messagebox.showerror('CHYBA', 'Chyba G1')
            return False
        if len(self.G1.twoFactors) == 0:
            messagebox.showerror('CHYBA', 'Chyba G1 2-faktory')
            return False
        return True



