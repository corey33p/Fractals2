import tkinter as tk
from tkinter import Tk,ttk,Label,Entry,Canvas,Button,IntVar,Radiobutton,Checkbutton,StringVar,Text,BooleanVar
import os
from Fractal_Canvas import FractalCanvas
import sys
from Fractal_Batch_Window import BatchWindow
from text_window import TextWriter
import time
import threading
import math
from Vertical_Scroll import VerticalScrollGrid
import win32gui
import win32con
from tkinter import filedialog

class Window:
    def __init__(self, parent, batch=False):
        self.parent = parent
        self.batch = batch
        self.font = ("Calibri",13)
        self.pythagoras = lambda a, b: (a**2 + b**2)**.5

        self.parent.fractal_processing = False
        self.parent.stop_early = False
        
        self.master = Tk()

        self.master.wm_title("Fractal Explorer")
        self.master.geometry('1900x863+0+8')

        self.master.minsize(width=1908, height=960)
        self.master.maxsize(width=1908, height=960)
        
        self.left_side_frame = ttk.Frame(self.master)
        self.left_side_frame.grid(row=0, column=0, sticky="nsew")
        self.scrolled_frame = VerticalScrollGrid(self.left_side_frame)
        self.scrolled_frame.grid(row=0,column=0,sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.left_side_frame.columnconfigure(0, weight=1)
        self.left_side_frame.rowconfigure(0, weight=1)
        
        self.fractal_settings_frame = ttk.Frame(self.scrolled_frame.frame)
        self.fractal_settings_frame.grid(row=0, column=0, sticky="ew")
        ttk.Separator(self.fractal_settings_frame, orient="horizontal").grid(row=0, columnspan=4, sticky="ew")
        Label(self.fractal_settings_frame, text="Fractal Settings",font=self.font).grid(row=0, column=1)

        Label(self.fractal_settings_frame, text="X Minimum: ",font=self.font).grid(row=1)
        self.x_min = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.x_min.insert("end", '-2')
        self.x_min.grid(row=1, column=1)
        Label(self.fractal_settings_frame, text="X Maximum: ",font=self.font).grid(row=2)
        self.x_max = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.x_max.insert("end", '2')
        self.x_max.grid(row=2, column=1)
        Label(self.fractal_settings_frame, text="Y Minimum: ",font=self.font).grid(row=3)
        self.y_min = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.y_min.insert("end", '-2')
        self.y_min.grid(row=3, column=1)
        Label(self.fractal_settings_frame, text="Y Maximum: ",font=self.font).grid(row=4)
        self.y_max = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.y_max.insert("end", '2')
        self.y_max.grid(row=4, column=1)
        Label(self.fractal_settings_frame, text="Iterations: ",font=self.font).grid(row=5)
        self.iterations = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.iterations.insert("end", '42')
        self.iterations.grid(row=5, column=1)
        #
        # Button(self.fractal_settings_frame, text='Get Rectangle', command=lambda: self.zoom_from_rectangle(by_button = True),font=self.font).grid(row=5, column=2)
        #
        Label(self.fractal_settings_frame, text="Image Width: ",font=self.font).grid(row=1, column=2)
        self.image_width = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.image_width.insert("end", '955')
        self.image_width.grid(row=1, column=3)
        Label(self.fractal_settings_frame, text="Image Height: ",font=self.font).grid(row=2, column=2)
        self.image_height = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.image_height.insert("end", '955')
        self.image_height.grid(row=2, column=3)
        Label(self.fractal_settings_frame, text="Rotation: ",font=self.font).grid(row=3, column=2)
        self.rotation = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.rotation.insert("end", '270')
        self.rotation.grid(row=3, column=3)
        Label(self.fractal_settings_frame, text="Bailout Value: ",font=self.font).grid(row=4, column=2)
        self.bailout_value = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.bailout_value.insert("end", '2')
        self.bailout_value.grid(row=4, column=3)
        #
        def coordinate_C():
            self.c_formula.set(1)
            self.c_real.delete(0, "end")
            self.c_real.insert("end", '.5')
            self.c_real.config(state = "disabled")
            self.c_imag.delete(0, "end")
            self.c_imag.insert("end", '.5')
            self.c_imag.config(state = "disabled")
            return
        def arbitrary_C():
            self.c_formula.set(2)
            self.c_real.config(state = "normal")
            self.c_imag.config(state = "normal")
            return
        self.c_formula_frame = ttk.Frame(self.fractal_settings_frame)
        self.c_formula_frame.grid(row=7,column=0,columnspan=4)
        self.c_formula = IntVar()
        self.c_formula.set(1)
        self.a_bi = Radiobutton(self.c_formula_frame, text="C = A + Bi", variable=self.c_formula, value=2, command=arbitrary_C,font=self.font)
        self.a_bi.grid(row=0, column=0, ipadx=50)
        self.x_yi = Radiobutton(self.c_formula_frame, text="C = X + Yi", variable=self.c_formula, value=1, command=coordinate_C,font=self.font)
        self.x_yi.grid(column=1, row=0, ipadx=50)
        Label(self.fractal_settings_frame, text="C Real (A): ",font=self.font).grid(row=8)
        self.c_real = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.c_real.insert("end", '.5')
        self.c_real.config(state = "disabled")
        self.c_real.grid(row=8, column=1)
        Label(self.fractal_settings_frame, text="C Imaginary (B): ",font=self.font).grid(row=8, column=2)
        self.c_imag = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        self.c_imag.insert("end", '.5')
        self.c_imag.config(state = "disabled")
        self.c_imag.grid(row=8, column=3)
        # Label(self.fractal_settings_frame, text="Thread Count: ",font=self.font).grid(row=9)
        # self.thread_count = Entry(self.fractal_settings_frame, justify = "right",font=self.font)
        # self.thread_count.insert("end", '3')
        # self.thread_count.grid(row=9, column=1)
        def verify_string(input_string):
            if input_string.count('(') != input_string.count(')'):
                if debug: print("Number of begin parenthesis does not match number of end parenthesis.")
                self.parent.text_out.write("\n!!!!! Equation Check Failed !!!!!")
                return False
            if " " in input_string: input_string = input_string.replace(" ", "")
            input_string += "          "
            def string_walk(string):
                debug = True
                super_debug = False
                if super_debug: print("\nTesting string '" + string.replace(" ","") + "'")
                list_advanced_operators = ("np.sin", "np.cos", "np.tan", "np.pi", "np.asin", "np.acos", "np.atan", "np.log", "np.exp", "complex", "abs")
                list_basic_operators = ("+", "-", "*", "/")
                variables_and_constants = ("Z", "C", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
                list_of_numbers = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
                count = 0
                begins_minus_ends = 0
                next_can_be_basic_operator = False
                next_must_be_begin_parenthesis = False
                skip_for_exponent_operator = False
                while count < len(string):
                    if super_debug: print("nested string walk count: " + str(count))
                    character = string[count]
                    if skip_for_exponent_operator:
                        if super_debug: print("check 1")
                        count += 1
                        skip_for_exponent_operator = False
                    elif character == "(":
                        if super_debug: print("check 2")
                        begins_minus_ends += 1
                        count += 1
                        substring_start = count
                        substring_end = count
                        while not ((substring_end >= len(string)) or begins_minus_ends == 0):
                            if string[substring_end] == "(":
                                begins_minus_ends += 1
                            elif string[substring_end] == ")":
                                begins_minus_ends -= 1
                            if begins_minus_ends != 0:
                                substring_end += 1
                            count += 1
                        if super_debug:
                            print("substring start and end: " + str(substring_start) + ", " + str(substring_end))
                            print("count after parenthesis: " + str(count))
                        if not string_walk(string[substring_start:substring_end]):
                            self.parent.text_out.write("\n!!!!! Equation Check Failed !!!!!")
                            return False
                        next_can_be_basic_operator = True
                        next_must_be_begin_parenthesis = False
                    elif (character in variables_and_constants) and (not next_must_be_begin_parenthesis):
                        if super_debug: print("check 3")
                        next_can_be_basic_operator = True
                        count += 1
                    elif character == "-" and (not next_can_be_basic_operator) and (not next_must_be_begin_parenthesis): #handles case of "-" serving as a negative sign in front of a number
                        if super_debug: print("check 14")
                        if not ((string[count+1] in list_of_numbers) or (string[count+1] == ".")):
                            self.parent.text_out.write("\n!!!!! Equation Check Failed !!!!!")
                            return False
                        else: count += 1
                    elif (character in list_basic_operators) and next_can_be_basic_operator and (not next_must_be_begin_parenthesis):
                        if super_debug: print("check 4")
                        if count + 1 < len(string):
                            if character == "*" and string[count+1] == "*":
                                skip_for_exponent_operator = True
                        count += 1
                        next_can_be_basic_operator = False
                    elif character == ".":
                        if super_debug: print("check 12")
                        subcount = count - 1
                        if count != 0:
                            while True:
                                if string[subcount] not in list_of_numbers:
                                    if (string[subcount] != "(") and (string[subcount] not in list_basic_operators):
                                        self.parent.text_out.write("\n!!!!! Equation Check Failed !!!!!")
                                        return False
                                    else: break
                                else: subcount -= 1
                            count += 1
                            if string[count] not in list_of_numbers:
                                self.parent.text_out.write("\n!!!!! Equation Check Failed !!!!!")
                                return False
                        else: count += 1
                    elif string[count:count+3] in list_advanced_operators and not next_must_be_begin_parenthesis:
                        if super_debug: print("check 5")
                        count += 3
                        next_can_be_basic_operator = False
                        next_must_be_begin_parenthesis = True
                    elif string[count:count+7] in list_advanced_operators and not next_must_be_begin_parenthesis:
                        if super_debug: print("check 6")
                        if string[count:count+7] == 'math.pi': next_must_be_begin_parenthesis = False
                        else: next_must_be_begin_parenthesis = True
                        count += 7
                        next_can_be_basic_operator = False
                    elif string[count:count+8] in list_advanced_operators and not next_must_be_begin_parenthesis:
                        if super_debug: print("check 7")
                        count += 8
                        next_can_be_basic_operator = False
                        next_must_be_begin_parenthesis = True
                    elif string[count:count+9] in list_advanced_operators and not next_must_be_begin_parenthesis:
                        if super_debug: print("check 8")
                        count += 9
                        next_can_be_basic_operator = False
                        next_must_be_begin_parenthesis = True
                    elif string[count:count+10] in list_advanced_operators and not next_must_be_begin_parenthesis:
                        if super_debug: print("check 13")
                        count += 10
                        next_can_be_basic_operator = False
                        next_must_be_begin_parenthesis = True
                    elif character == ")":
                        if super_debug: print("check 9")
                        if debug: print("Found unexpected end ')'")
                        self.parent.text_out.write("\n!!!!! Equation Check Failed !!!!!")
                        return False #in valid strings, these should all be caught by the earlier 'if' condition, where parenthetic expressions are handled recursively
                    elif character == " ":
                        string = input_string.replace(" ", "")
                    else:
                        if super_debug: print("check 10")
                        if debug:
                            print("\nEquation debugging:\nError handling character at position " + str(count) + " of string '" + string.replace(" ","") + "': '" + character + "'")
                            print("next_can_be_basic_operator:     " + str(next_can_be_basic_operator))
                            print("next_must_be_begin_parenthesis: " + str(next_must_be_begin_parenthesis))
                            print("skip_for_exponent_operator:     " + str(skip_for_exponent_operator))
                        self.parent.text_out.write("\n!!!!! Equation Check Failed !!!!!")
                        return False
                    if (next_must_be_begin_parenthesis or (character in list_basic_operators)) and count >= len(string):
                        if super_debug: print("check 11")
                        if debug: print("Incomplete or erroneous expression at end of string!")
                        self.parent.text_out.write("\n!!!!! Equation Check Failed !!!!!")
                        return False
                self.parent.text_out.write("\n!!!!! Equation Seems Valid !!!!!")
                return True
            return string_walk(input_string)
        self.equation_box_frame = ttk.Frame(self.fractal_settings_frame)
        self.equation_box_frame.grid(row=6, columnspan=4)
        Label(self.equation_box_frame, text="Iterative Equation:   Z(n + 1)=",font=self.font).grid(row=0, column=0)
        self.equation = Entry(self.equation_box_frame, width=45, justify = "left",font=self.font)
        self.equation.insert("end", "Z**2 + C")
        self.equation.grid(row=0, column=1)
        Button(self.equation_box_frame, text="Verify", command=lambda: verify_string(self.equation.get()),font=self.font).grid(row=0, column=2)
        #

        ###---------\/\/\/\/\/\/\--------COLORING SETTINGS-----------\/\/\/\/\/\/\----------###
        ###---------\/\/\/\/\/\/\--------COLORING SETTINGS-----------\/\/\/\/\/\/\----------###
        ###---------\/\/\/\/\/\/\--------COLORING SETTINGS-----------\/\/\/\/\/\/\----------###
        ###---------\/\/\/\/\/\/\--------COLORING SETTINGS-----------\/\/\/\/\/\/\----------###
        ###---------\/\/\/\/\/\/\--------COLORING SETTINGS-----------\/\/\/\/\/\/\----------###

        self.coloring_settings_frame = ttk.Frame(self.scrolled_frame.frame)
        self.coloring_settings_frame.grid(row=1, column=0, sticky="ew")
        ttk.Separator(self.coloring_settings_frame, orient="horizontal").grid(row=9, columnspan=4, sticky="ew")
        Label(self.coloring_settings_frame, text="Coloring Settings",font=self.font).grid(row=9, column=1)
        Label(self.coloring_settings_frame, text="Scheme Active",font=self.font).grid(row=10, column=0)
        Label(self.coloring_settings_frame, text="Coloring Technique",font=self.font).grid(row=10, column=1)
        Label(self.coloring_settings_frame, text="Coloring Scale",font=self.font).grid(row=10, column=2)
        Label(self.coloring_settings_frame, text="Coloring Sequence",font=self.font).grid(row=10, column=3)

        self.scheme_1_check = IntVar()
        self.scheme_1_check.set(1)
        self.scheme_1_button = Checkbutton(self.coloring_settings_frame, text="Color Scheme 1", variable=self.scheme_1_check,font=self.font)
        self.scheme_1_button.grid(row=11, column=0, sticky="w")
        self.scheme_2_check = IntVar()
        self.scheme_2_button = Checkbutton(self.coloring_settings_frame, text="Color Scheme 2", variable=self.scheme_2_check,font=self.font)
        self.scheme_2_button.grid(row=12, column=0, sticky="w")
        self.scheme_3_check = IntVar()
        self.scheme_3_button = Checkbutton(self.coloring_settings_frame, text="Color Scheme 3", variable=self.scheme_3_check,font=self.font)
        self.scheme_3_button.grid(row=13, column=0, sticky="w")
        self.scheme_4_check = IntVar()
        self.scheme_4_button = Checkbutton(self.coloring_settings_frame, text="Color Scheme 4", variable=self.scheme_4_check,font=self.font)
        self.scheme_4_button.grid(row=14, column=0, sticky="w")
        class color_scheme_dropdown:
            def __init__(self, parent_frame,font):
                self.font=font
                self.parent_frame = parent_frame
                self.value_of_combo = 'Iteration Count'
                self.combo()
                self.integer_value = 0
            def newselection(self, event):
                self.value_of_combo = self.box.get()
                self.integer_value = self.box['values'].index(str(self.value_of_combo))
            def box_update(self, value):
                self.integer_value = value
                self.box.current(int(value))
            def combo(self):
                self.box_value = StringVar()
                self.box = ttk.Combobox(self.parent_frame, textvariable=self.box_value, state='readonly',font=self.font)
                self.box.bind("<<ComboboxSelected>>", self.newselection)
                self.box['values'] = ('Iteration Count', 'Iteration Count w/ Gradient', 'Orbit Trap: Circle', 'Orbit Trap: Ellipse', 'Orbit Trap: Line', 'Orbit Trap: Cross', 'Orbit Trap: Spiral')
                self.box.current(0)
        self.scheme_1_dropdown = color_scheme_dropdown(self.coloring_settings_frame,self.font)
        self.scheme_1_dropdown.box_update(1) #set the default coloring scheme to iteration count w/ gradient
        self.scheme_1_dropdown.box.grid(column=1, row=11)
        self.scheme_2_dropdown = color_scheme_dropdown(self.coloring_settings_frame,self.font)
        self.scheme_2_dropdown.box.grid(column=1, row=12)
        self.scheme_3_dropdown = color_scheme_dropdown(self.coloring_settings_frame,self.font)
        self.scheme_3_dropdown.box.grid(column=1, row=13)
        self.scheme_4_dropdown = color_scheme_dropdown(self.coloring_settings_frame,self.font)
        self.scheme_4_dropdown.box.grid(column=1, row=14)
        class color_scale_dropdown:
            def __init__(self, parent_frame,font):
                self.font = font
                self.parent_frame = parent_frame
                self.value_of_combo = 'Color Spectrum'
                self.combo()
                self.integer_value = 0
            def newselection(self, event):
                self.value_of_combo = self.box.get()
                self.integer_value = self.box['values'].index(str(self.value_of_combo))
            def box_update(self, value):
                self.integer_value = value
                self.box.current(int(value))
            def combo(self):
                self.box_value = StringVar()
                self.box = ttk.Combobox(self.parent_frame, textvariable=self.box_value, state='readonly',font=self.font)
                self.box.bind("<<ComboboxSelected>>", self.newselection)
                self.box['values'] = ('Color Spectrum', 'Color Hierarchy')
                self.box.current(0)
        self.color_scale_1_dropdown = color_scale_dropdown(self.coloring_settings_frame,self.font)
        self.color_scale_1_dropdown.box.grid(column=2, row=11)
        self.color_scale_2_dropdown = color_scale_dropdown(self.coloring_settings_frame,self.font)
        self.color_scale_2_dropdown.box.grid(column=2, row=12)
        self.color_scale_3_dropdown = color_scale_dropdown(self.coloring_settings_frame,self.font)
        self.color_scale_3_dropdown.box.grid(column=2, row=13)
        self.color_scale_4_dropdown = color_scale_dropdown(self.coloring_settings_frame,self.font)
        self.color_scale_4_dropdown.box.grid(column=2, row=14)
        #
        self.sequence_1_entry = Entry(self.coloring_settings_frame, justify = "right",font=self.font)
        self.sequence_1_entry.insert("end", '0B263')
        self.sequence_1_entry.grid(row=11, column=3)
        self.sequence_2_entry = Entry(self.coloring_settings_frame, justify = "right",font=self.font)
        self.sequence_2_entry.insert("end", '02468')
        self.sequence_2_entry.grid(row=12, column=3)
        self.sequence_3_entry = Entry(self.coloring_settings_frame, justify = "right",font=self.font)
        self.sequence_3_entry.insert("end", '02468')
        self.sequence_3_entry.grid(row=13, column=3)
        self.sequence_4_entry = Entry(self.coloring_settings_frame, justify = "right",font=self.font)
        self.sequence_4_entry.insert("end", '02468')
        self.sequence_4_entry.grid(row=14, column=3)
        #--
        Label(self.coloring_settings_frame, text="Orbit Trap-Rotation: ",font=self.font).grid(row=17, column=0)
        self.OT_rotation_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_rotation_frame.grid(row=17, column=1, sticky="ew")
        self.OT_rotation1 = Entry(self.OT_rotation_frame, width=6, justify = "right",font=self.font)
        self.OT_rotation1.insert("end", '0')
        self.OT_rotation1.pack(side="left")
        self.OT_rotation2 = Entry(self.OT_rotation_frame, width=6, justify = "right",font=self.font)
        self.OT_rotation2.insert("end", '0')
        self.OT_rotation2.pack(side="left")
        self.OT_rotation3 = Entry(self.OT_rotation_frame, width=6, justify = "right",font=self.font)
        self.OT_rotation3.insert("end", '0')
        self.OT_rotation3.pack(side="left")
        self.OT_rotation4 = Entry(self.OT_rotation_frame, width=6, justify = "right",font=self.font)
        self.OT_rotation4.insert("end", '60')
        self.OT_rotation4.pack(side="left")
        Label(self.coloring_settings_frame, text="Orbit Trap-Radius 1: ",font=self.font).grid(row=18, column=0)
        self.OT_radius_frame1 = ttk.Frame(self.coloring_settings_frame)
        self.OT_radius_frame1.grid(row=18, column=1, sticky="ew")
        self.OT_radius1_1 = Entry(self.OT_radius_frame1, width=6, justify = "right",font=self.font)
        self.OT_radius1_1.insert("end", '.3')
        self.OT_radius1_1.pack(side="left")
        self.OT_radius1_2 = Entry(self.OT_radius_frame1, width=6, justify = "right",font=self.font)
        self.OT_radius1_2.insert("end", '1')
        self.OT_radius1_2.pack(side="left")
        self.OT_radius1_3 = Entry(self.OT_radius_frame1, width=6, justify = "right",font=self.font)
        self.OT_radius1_3.insert("end", '.25')
        self.OT_radius1_3.pack(side="left")
        self.OT_radius1_4 = Entry(self.OT_radius_frame1, width=6, justify = "right",font=self.font)
        self.OT_radius1_4.insert("end", '3')
        self.OT_radius1_4.pack(side="left")
        Label(self.coloring_settings_frame, text="Orbit Trap-Radius 2: ",font=self.font).grid(row=19, column=0)
        self.OT_radius_frame2 = ttk.Frame(self.coloring_settings_frame)
        self.OT_radius_frame2.grid(row=19, column=1, sticky="ew")
        self.OT_radius2_1 = Entry(self.OT_radius_frame2, width=6, justify = "right",font=self.font)
        self.OT_radius2_1.insert("end", '.5')
        self.OT_radius2_1.pack(side="left")
        self.OT_radius2_2 = Entry(self.OT_radius_frame2, width=6, justify = "right",font=self.font)
        self.OT_radius2_2.insert("end", '1')
        self.OT_radius2_2.pack(side="left")
        self.OT_radius2_3 = Entry(self.OT_radius_frame2, width=6, justify = "right",font=self.font)
        self.OT_radius2_3.insert("end", '.25')
        self.OT_radius2_3.pack(side="left")
        self.OT_radius2_4 = Entry(self.OT_radius_frame2, width=6, justify = "right",font=self.font)
        self.OT_radius2_4.insert("end", '2')
        self.OT_radius2_4.pack(side="left")
        #
        Label(self.coloring_settings_frame, text="Orbit Trap-Trap Count: ",font=self.font).grid(row=20, column=0)
        self.OT_trap_count_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_trap_count_frame.grid(row=20, column=1, sticky="ew")
        self.OT_trap_count1 = Entry(self.OT_trap_count_frame, width=6, justify = "right",font=self.font)
        self.OT_trap_count1.insert("end", '1')
        self.OT_trap_count1.pack(side="left")
        self.OT_trap_count2 = Entry(self.OT_trap_count_frame, width=6, justify = "right",font=self.font)
        self.OT_trap_count2.insert("end", '1')
        self.OT_trap_count2.pack(side="left")
        self.OT_trap_count3 = Entry(self.OT_trap_count_frame, width=6, justify = "right",font=self.font)
        self.OT_trap_count3.insert("end", '1')
        self.OT_trap_count3.pack(side="left")
        self.OT_trap_count4 = Entry(self.OT_trap_count_frame, width=6, justify = "right",font=self.font)
        self.OT_trap_count4.insert("end", '1')
        self.OT_trap_count4.pack(side="left")
        #
        Label(self.coloring_settings_frame, text="Orbit Trap-Starting Width: ",font=self.font).grid(row=17, column=2)
        self.OT_width_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_width_frame.grid(row=17, column=3, sticky="ew")
        self.OT_starting_width1 = Entry(self.OT_width_frame, width=6, justify = "right",font=self.font)
        self.OT_starting_width1.insert("end", '.5')
        self.OT_starting_width1.pack(side="left")
        self.OT_starting_width2 = Entry(self.OT_width_frame, width=6, justify = "right",font=self.font)
        self.OT_starting_width2.insert("end", '.5')
        self.OT_starting_width2.pack(side="left")
        self.OT_starting_width3 = Entry(self.OT_width_frame, width=6, justify = "right",font=self.font)
        self.OT_starting_width3.insert("end", '.5')
        self.OT_starting_width3.pack(side="left")
        self.OT_starting_width4 = Entry(self.OT_width_frame, width=6, justify = "right",font=self.font)
        self.OT_starting_width4.insert("end", '.5')
        self.OT_starting_width4.pack(side="left")
        Label(self.coloring_settings_frame, text="Orbit Trap-Width Deflection: ",font=self.font).grid(row=18, column=2)
        self.OT_width_deflection_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_width_deflection_frame.grid(row=18, column=3, sticky="ew")
        self.OT_width_deflection1 = Entry(self.OT_width_deflection_frame, width=6, justify = "right",font=self.font)
        self.OT_width_deflection1.insert("end", '.1')
        self.OT_width_deflection1.pack(side="left")
        self.OT_width_deflection2 = Entry(self.OT_width_deflection_frame, width=6, justify = "right",font=self.font)
        self.OT_width_deflection2.insert("end", '-.1')
        self.OT_width_deflection2.pack(side="left")
        self.OT_width_deflection3 = Entry(self.OT_width_deflection_frame, width=6, justify = "right",font=self.font)
        self.OT_width_deflection3.insert("end", '.005')
        self.OT_width_deflection3.pack(side="left")
        self.OT_width_deflection4 = Entry(self.OT_width_deflection_frame, width=6, justify = "right",font=self.font)
        self.OT_width_deflection4.insert("end", '0')
        self.OT_width_deflection4.pack(side="left")
        #--
        Label(self.coloring_settings_frame, text="Orbit Trap-Color Loop Distance: ",font=self.font).grid(row=19, column=2)
        self.OT_loop_distance_distance_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_loop_distance_distance_frame.grid(row=19, column=3, sticky="ew")
        self.OT_loop_distance1 = Entry(self.OT_loop_distance_distance_frame, width=6, justify = "right",font=self.font)
        self.OT_loop_distance1.insert("end", '7')
        self.OT_loop_distance1.pack(side="left")
        self.OT_loop_distance2 = Entry(self.OT_loop_distance_distance_frame, width=6, justify = "right",font=self.font)
        self.OT_loop_distance2.insert("end", '1')
        self.OT_loop_distance2.pack(side="left")
        self.OT_loop_distance3 = Entry(self.OT_loop_distance_distance_frame, width=6, justify = "right",font=self.font)
        self.OT_loop_distance3.insert("end", '.5')
        self.OT_loop_distance3.pack(side="left")
        self.OT_loop_distance4 = Entry(self.OT_loop_distance_distance_frame, width=6, justify = "right",font=self.font)
        self.OT_loop_distance4.insert("end", '1.2')
        self.OT_loop_distance4.pack(side="left")
        #
        #
        Label(self.coloring_settings_frame, text="Orbit Trap-Focus: ",font=self.font).grid(row=21, column=0)
        self.OT_focus_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_focus_frame.grid(row=21, column=1, sticky="ew", columnspan=3)
        self.OT_focus1_x = Entry(self.OT_focus_frame, width=6, justify = "right",font=self.font)
        self.OT_focus1_x.insert("end", '1.5')
        self.OT_focus1_x.pack(side="left")
        self.OT_focus1_y = Entry(self.OT_focus_frame, width=6, justify = "right",font=self.font)
        self.OT_focus1_y.insert("end", '1.5')
        self.OT_focus1_y.pack(side="left")
        ttk.Separator(self.OT_focus_frame, orient="vertical").pack(side="left",fill="y")
        ttk.Separator(self.OT_focus_frame, orient="vertical").pack(side="left",fill="y")
        #
        self.OT_focus2_x = Entry(self.OT_focus_frame, width=6, justify = "right",font=self.font)
        self.OT_focus2_x.insert("end", '1')
        self.OT_focus2_x.pack(side="left")
        self.OT_focus2_y = Entry(self.OT_focus_frame, width=6, justify = "right",font=self.font)
        self.OT_focus2_y.insert("end", '-.3')
        self.OT_focus2_y.pack(side="left")
        ttk.Separator(self.OT_focus_frame, orient="vertical").pack(side="left",fill="y")
        ttk.Separator(self.OT_focus_frame, orient="vertical").pack(side="left",fill="y")
        #
        self.OT_focus3_x = Entry(self.OT_focus_frame, width=6, justify = "right",font=self.font)
        self.OT_focus3_x.insert("end", '1.2')
        self.OT_focus3_x.pack(side="left")
        self.OT_focus3_y = Entry(self.OT_focus_frame, width=6, justify = "right",font=self.font)
        self.OT_focus3_y.insert("end", '.085')
        self.OT_focus3_y.pack(side="left")
        ttk.Separator(self.OT_focus_frame, orient="vertical").pack(side="left",fill="y")
        ttk.Separator(self.OT_focus_frame, orient="vertical").pack(side="left",fill="y")
        #
        self.OT_focus4_x = Entry(self.OT_focus_frame, width=6, justify = "right",font=self.font)
        self.OT_focus4_x.insert("end", '0')
        self.OT_focus4_x.pack(side="left")
        self.OT_focus4_y = Entry(self.OT_focus_frame, width=6, justify = "right",font=self.font)
        self.OT_focus4_y.insert("end", '0')
        self.OT_focus4_y.pack(side="left")
        #--
        Label(self.coloring_settings_frame, text="Orbit Trap-Measure Point: ",font=self.font).grid(row=22, column=0)
        self.OT_color_measure_point_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_color_measure_point_frame.grid(row=22, column=1, columnspan=3, sticky="ew")
        self.OT_measure_point1_x = Entry(self.OT_color_measure_point_frame, width=6, justify = "right",font=self.font)
        self.OT_measure_point1_x.insert("end", '0')
        self.OT_measure_point1_x.pack(side="left")
        self.OT_measure_point1_y = Entry(self.OT_color_measure_point_frame, width=6, justify = "right",font=self.font)
        self.OT_measure_point1_y.insert("end", '0')
        self.OT_measure_point1_y.pack(side="left")
        ttk.Separator(self.OT_color_measure_point_frame, orient="vertical").pack(side="left",fill="y")
        ttk.Separator(self.OT_color_measure_point_frame, orient="vertical").pack(side="left",fill="y")
        #
        self.OT_measure_point2_x = Entry(self.OT_color_measure_point_frame, width=6, justify = "right",font=self.font)
        self.OT_measure_point2_x.insert("end", '0')
        self.OT_measure_point2_x.pack(side="left")
        self.OT_measure_point2_y = Entry(self.OT_color_measure_point_frame, width=6, justify = "right",font=self.font)
        self.OT_measure_point2_y.insert("end", '0')
        self.OT_measure_point2_y.pack(side="left")
        ttk.Separator(self.OT_color_measure_point_frame, orient="vertical").pack(side="left",fill="y")
        ttk.Separator(self.OT_color_measure_point_frame, orient="vertical").pack(side="left",fill="y")
        #
        self.OT_measure_point3_x = Entry(self.OT_color_measure_point_frame, width=6, justify = "right",font=self.font)
        self.OT_measure_point3_x.insert("end", '0')
        self.OT_measure_point3_x.pack(side="left")
        self.OT_measure_point3_y = Entry(self.OT_color_measure_point_frame, width=6, justify = "right",font=self.font)
        self.OT_measure_point3_y.insert("end", '0')
        self.OT_measure_point3_y.pack(side="left")
        ttk.Separator(self.OT_color_measure_point_frame, orient="vertical").pack(side="left",fill="y")
        ttk.Separator(self.OT_color_measure_point_frame, orient="vertical").pack(side="left",fill="y")
        #
        self.OT_measure_point4_x = Entry(self.OT_color_measure_point_frame, width=6, justify = "right",font=self.font)
        self.OT_measure_point4_x.insert("end", '0')
        self.OT_measure_point4_x.pack(side="left")
        self.OT_measure_point4_y = Entry(self.OT_color_measure_point_frame, width=6, justify = "right",font=self.font)
        self.OT_measure_point4_y.insert("end", '0')
        self.OT_measure_point4_y.pack(side="left")
        #
        #
        self.black_background_check = IntVar()
        self.black_background_check.set(1)
        self.black_background_button = Checkbutton(self.coloring_settings_frame, text="Black Background",font=self.font, variable=self.black_background_check)
        self.black_background_button.grid(row=23, column=0, sticky="w")
        #
        self.repeat_colors_check = IntVar()
        self.repeat_colors_check.set(1)
        self.repeat_colors_button = Checkbutton(self.coloring_settings_frame, text="Repeat Colors",font=self.font, variable=self.repeat_colors_check)
        self.repeat_colors_button.grid(row=23,column=1,sticky="w")
        #
        Label(self.coloring_settings_frame, text="Color Repeat Value: ",font=self.font).grid(row=23, column=2)
        self.color_repeat_frame = ttk.Frame(self.coloring_settings_frame)
        self.color_repeat_frame.grid(row=23, column=3, sticky="ew")
        self.color_repeat = Entry(self.color_repeat_frame, width=6, justify = "right",font=self.font)
        self.color_repeat.insert("end", '21')
        self.color_repeat.pack(side="left")
        #----------------------------
        self.bottom_buttons_frame = ttk.Frame(self.scrolled_frame.frame)
        ttk.Separator(self.bottom_buttons_frame, orient="horizontal").grid(row=9, columnspan=4, sticky="ew")
        self.bottom_buttons_frame.grid(row=2, column=0, sticky="ew")
        Label(self.bottom_buttons_frame, text="Image Name: ",font=self.font).grid(row=20)
        self.image_name = Entry(self.bottom_buttons_frame, width=60, justify = "right",font=self.font)
        self.image_name.insert("end", os.getcwd().replace('\\','/') + "/save/Fractal.png")
        self.image_name.grid(row=20, column=1)
        Label(self.bottom_buttons_frame, text="Load Settings: ",font=self.font).grid(row=21, column=0)
        self.load_filename_frame = ttk.Frame(self.bottom_buttons_frame)
        self.load_filename_frame.grid(row=21, column=1, columnspan=2, sticky="ew")
        self.load_filename = Entry(self.load_filename_frame, width=60, justify = "right",font=self.font)
        self.load_filename.insert("end", os.getcwd().replace('\\','/') + "/save/recent_settings.json")
        self.load_filename.pack(side="left", expand=True, fill="x")
        self.load_filename_frame.grid_columnconfigure(0, weight=1)
        def browse_for_load_file():
            file = filedialog.askopenfilename(parent=self.load_filename_frame, initialdir=os.getcwd()+"\\save", title='Select A Settings File',filetypes = (("json files","*.json"),("all files","*.*")))
            self.load_filename.delete(0, "end")
            self.load_filename.insert("end", file)
            return
        self.load_browse = Button(self.load_filename_frame, text='...', command=browse_for_load_file,font=self.font)
        self.load_browse.pack(side="right")
        #
        Label(self.bottom_buttons_frame, text="Save Settings: ",font=self.font).grid(row=22, column=0)
        self.save_filename_frame = ttk.Frame(self.bottom_buttons_frame)
        self.save_filename_frame.grid(row=22, column=1, columnspan=2, sticky="ew")
        self.save_filename = Entry(self.save_filename_frame, width=60, justify="right",font=self.font)
        self.save_filename.insert("end", os.getcwd().replace('\\','/') + "/save/user_settings.json")
        self.save_filename.pack(side="left", expand=True, fill="x")
        self.save_filename_frame.grid_columnconfigure(0, weight=1)
        def browse_for_save_file():
            file = filedialog.askopenfilename(parent=self.save_filename_frame, initialdir=os.getcwd(), title='Select A Settings File')
            self.save_filename.delete(0, "end")
            self.save_filename.insert("end", file)
            return
        self.save_browse = Button(self.save_filename_frame, text='...', command=browse_for_save_file,font=self.font)
        self.save_browse.pack(side="left")
        #
        self.canvas_frame = ttk.Frame(self.master)
        self.parent.canvas_object = FractalCanvas(self.parent, self.canvas_frame)
        self.canvas_frame.grid(row=0,column=4)
        #
        self.parent.canvas_object.proportion_rectangle_check = IntVar()
        self.parent.canvas_object.proportion_rectangle_check.set(1)
        self.proportion_rectangle_button = Checkbutton(self.fractal_settings_frame,font=self.font, text="Scale Rectangle", variable=self.parent.canvas_object.proportion_rectangle_check)
        self.proportion_rectangle_button.grid(row=5, column=3)
        #
        self.zoom_out_check = BooleanVar()
        self.zoom_out_check.set(False)
        self.zoom_out_check_button = Checkbutton(self.fractal_settings_frame,font=self.font, text="Zoom Out", variable=self.zoom_out_check)
        self.zoom_out_check_button.grid(row=5,column=2)
        ##--------
        ##--------
        Button(self.bottom_buttons_frame, text='Load Settings', command=self.load_settings_from_file,font=self.font).grid(row=21, column=3, sticky="ew", pady=4)
        Button(self.bottom_buttons_frame, text='Save Settings', command=self.save_settings_file,font=self.font).grid(row=22, column=3, sticky="ew", pady=4)
        Button(self.bottom_buttons_frame, text='Set Default Settings',font=self.font, command=lambda: self.save_settings_file(default=True)).grid(row=23, column=1, sticky="ew", pady=4)
        Button(self.bottom_buttons_frame, text='Load Default Settings',font=self.font, command=self.load_default_settings).grid(row=23, column=3, sticky="ew", pady=4)
        self.generate_button = Button(self.bottom_buttons_frame, text='Generate', command=self.generate_fractal,font=self.font)
        self.generate_button.grid(row=24, column=1, sticky="ew", pady=4)
        def quit():
            for handle in self.parent.cli_handles:
                win32gui.PostMessage(handle,win32con.WM_CLOSE,0,0)
        Button(self.bottom_buttons_frame, text='Quit', command=quit,font=self.font).grid(row=24, column=3, sticky="ew", pady=4)
        ##--------
        ##--------
        self.CLI_frame = ttk.Frame(self.scrolled_frame.frame)
        self.CLI_frame.grid(row=3, column=0)
        self.textbox=Text(self.CLI_frame, background="black", height=4, width=110,foreground="green",font=self.font)
        self.textbox.pack()
        # sys.stdout = self.parent.text_out = TextWriter(self.textbox)
        self.parent.text_out = TextWriter(self.textbox)
        ##--------
        ##--------
        if self.batch: self.parent.window2_object = BatchWindow(self.parent)
        ##--------
    def zoom_from_rectangle(self,by_button=False,zoom_out=False):
        debug = False
        #----------------------
        #find rectangle centerpoint in pixels
        rectangle_centerpoint_x_in_pixels = (self.parent.canvas_object.rect_start_x + self.parent.canvas_object.rect_end_x) / 2 - self.parent.canvas_object.image_start_x
        rectangle_centerpoint_y_in_pixels = (self.parent.canvas_object.rect_start_y + self.parent.canvas_object.rect_end_y) / 2 - self.parent.canvas_object.image_start_y
        if debug: print("\nrect centerpoint (pixels): " + str(rectangle_centerpoint_x_in_pixels) + ", " + str(rectangle_centerpoint_y_in_pixels))
        #----------------------
        #find size, in pixels, of the rectangle
        rect_x_width = abs(self.parent.canvas_object.rect_end_x - self.parent.canvas_object.rect_start_x)
        rect_y_width = abs(self.parent.canvas_object.rect_end_y - self.parent.canvas_object.rect_start_y)
        if debug: print("rect dimensions: " + str(rect_x_width) + " x " + str(rect_y_width))
        #----------------------
        #find center of image in fractal coordinate plane
        image_center_x = (self.parent.fractal_object.settings['x_min'][1] + self.parent.fractal_object.settings['x_max'][1]) / 2
        image_center_y = (self.parent.fractal_object.settings['y_min'][1] + self.parent.fractal_object.settings['y_max'][1]) / 2
        if debug: print("image center in coordinate plane: " + str(image_center_x) + ", " + str(image_center_y))
        #----------------------
        #find original image size in fractal coordinate plane
        original_x_coordinate_width = self.parent.fractal_object.settings['x_max'][1] - self.parent.fractal_object.settings['x_min'][1]
        original_y_coordinate_width = self.parent.fractal_object.settings['y_max'][1] - self.parent.fractal_object.settings['y_min'][1]
        if debug: print("original coordinate width, height: " + str(original_x_coordinate_width) + " x " + str(original_y_coordinate_width))
        if zoom_out:
            #----------------------
            #find proportion of rectangle coordinate size vs original image size in coordinate plane
            rect_x_width = rect_x_width / (rect_x_width / self.parent.fractal_object.settings['image_width'][1])**2
            rect_y_width = rect_y_width / (rect_y_width / self.parent.fractal_object.settings['image_height'][1])**2
            if debug: print("zoom out rect dimensions: " + str(rect_x_width) + ", " + str(rect_y_width))
        #----------------------
        #find tentative rectangle coordinate widths by proportion
        tentative_rect_x_coordinate_width = original_x_coordinate_width * rect_x_width / self.parent.canvas_object.image_size[0]
        tentative_rect_y_coordinate_width = original_y_coordinate_width * rect_y_width / self.parent.canvas_object.image_size[1]
        if debug: print("tentative rect coord widths: " + str(tentative_rect_x_coordinate_width) + ", " + str(tentative_rect_y_coordinate_width))
        #----------------------
        #find centerpoint of rectangle in fractal coordinates, before accounting for rotation
        tentative_rectangle_centerpoint_x = self.parent.fractal_object.settings['x_min'][1] + (original_x_coordinate_width * rectangle_centerpoint_x_in_pixels / self.parent.canvas_object.image_size[0])
        tentative_rectangle_centerpoint_y = self.parent.fractal_object.settings['y_min'][1] + (original_y_coordinate_width * rectangle_centerpoint_y_in_pixels / self.parent.canvas_object.image_size[1])
        if debug: print("rect center point, pre adjusted: " + str(tentative_rectangle_centerpoint_x) + ", " + str(tentative_rectangle_centerpoint_y))
        #----------------------
        #calculate distance from center of rectangle to center of image
        center_rect_distance_from_center_image = self.pythagoras(tentative_rectangle_centerpoint_x - image_center_x, tentative_rectangle_centerpoint_y - image_center_y)
        if debug: print("dist center rect from center image: " + str(center_rect_distance_from_center_image))
        #----------------------
        #find the angle to the center of the rectangle relative to orientation of the image
        angle_to_rectangle_in_image = math.acos((tentative_rectangle_centerpoint_x - image_center_x) / center_rect_distance_from_center_image)
        if tentative_rectangle_centerpoint_y < image_center_y:
            angle_to_rectangle_in_image = 2 * math.pi - angle_to_rectangle_in_image
        if debug: print("angle from image orientation to center rect: " + str(angle_to_rectangle_in_image))
        #----------------------
        #adjust rectangle centerpoint for rotation of image. AKA, stretch diagonally
        angle_to_corner_image_from_image_axis = math.tan(original_y_coordinate_width / original_x_coordinate_width)
        if (angle_to_rectangle_in_image < angle_to_corner_image_from_image_axis) or (abs(math.pi - angle_to_rectangle_in_image) < angle_to_corner_image_from_image_axis) or (2 * math.pi - angle_to_rectangle_in_image < angle_to_corner_image_from_image_axis): rect_distance_scalar = (center_rect_distance_from_center_image / math.cos(angle_to_rectangle_in_image))
        else: rect_distance_scalar = (center_rect_distance_from_center_image / math.sin(angle_to_rectangle_in_image))
        scalar_rectangle_centerpoint_x = self.parent.fractal_object.settings['x_min'][1] + (rect_distance_scalar * rectangle_centerpoint_x_in_pixels / self.parent.canvas_object.image_size[0])
        scalar_rectangle_centerpoint_y = self.parent.fractal_object.settings['y_min'][1] + (rect_distance_scalar * rectangle_centerpoint_y_in_pixels / self.parent.canvas_object.image_size[1])
        denominator = self.pythagoras(original_x_coordinate_width / 2, original_y_coordinate_width / 2)
        adjusted_rectangle_centerpoint_x = (original_x_coordinate_width / 2) / scalar_rectangle_centerpoint_x * denominator
        adjusted_rectangle_centerpoint_y = (original_y_coordinate_width / 2) / scalar_rectangle_centerpoint_y * denominator
        if debug: print("new dist center rect from center image: " + str(center_rect_distance_from_center_image))
        if debug: print("adjusted rect center point: " + str(adjusted_rectangle_centerpoint_x) + ", " + str(adjusted_rectangle_centerpoint_y))
        #----------------------
        #get angle of image
        self.parent.fractal_object.settings['rotation'] = ['float', float(self.rotation.get())]
        image_angle_in_radians = self.parent.fractal_object.settings['rotation'][1] * math.pi / 180
        if debug: print("image angle: " + str(image_angle_in_radians))
        #----------------------
        #find the center of the rectangle in fractal coord plane adjusting for rotation of image
        x_coordinate_add = center_rect_distance_from_center_image * math.cos(image_angle_in_radians + angle_to_rectangle_in_image)
        y_coordinate_add = center_rect_distance_from_center_image * math.sin(image_angle_in_radians + angle_to_rectangle_in_image)
        x_coordinate_final = image_center_x + x_coordinate_add
        y_coordinate_final = image_center_y + y_coordinate_add
        if debug: print("rect centerpoint final: " + str(x_coordinate_final) + ", " + str(y_coordinate_final))
        #----------------------
        #calculate new coordinate bounds with new coordinate widths and new coordinate centerpoint
        new_min_x = x_coordinate_final - tentative_rect_x_coordinate_width / 2
        new_max_x = x_coordinate_final + tentative_rect_x_coordinate_width / 2
        new_min_y = y_coordinate_final - tentative_rect_y_coordinate_width / 2
        new_max_y = y_coordinate_final + tentative_rect_y_coordinate_width / 2
        #----------------------
        #finally, replace GUI coord bounds with newly calc'd coord bounds based on rectangle
        self.x_min.delete(0, "end")
        self.x_min.insert("end", str(new_min_x))
        self.x_max.delete(0, "end")
        self.x_max.insert("end", str(new_max_x))
        self.y_min.delete(0, "end")
        self.y_min.insert("end", str(new_min_y))
        self.y_max.delete(0, "end")
        self.y_max.insert("end", str(new_max_y))
        if by_button: self.parent.text_out.write("\n!!!!! Coordinates Updated !!!!!")
        return
    def GUI_settings_to_dict(self): #GUI gather settings into dictionary
        settings = {}
        settings['x_min'] = ['float', float(self.x_min.get())]
        settings['x_max'] = ['float', float(self.x_max.get())]
        settings['y_min'] = ['float', float(self.y_min.get())]
        settings['y_max'] = ['float', float(self.y_max.get())]
        settings['iterations'] = ['int', int(float(self.iterations.get()))]
        settings['c_formula'] = ['int', self.c_formula.get()]
        settings['c_real'] = ['float', float(self.c_real.get())]
        settings['c_imag'] = ['float', float(self.c_imag.get())]
        settings['image_width'] = ['int', int(self.image_width.get())]
        settings['image_height'] = ['int', int(self.image_height.get())]
        settings['rotation'] = ['float', float(self.rotation.get())]
        settings['image_name'] = ['str', self.image_name.get()]
        settings['proportion_rectangle_check'] = ['int', int(self.parent.canvas_object.proportion_rectangle_check.get())]
        settings['bailout_value'] = ['float', float(self.bailout_value.get())]
        settings['equation'] = ['str', self.equation.get().replace(" ","")]
        # settings['thread_count'] = ['int', int(self.thread_count.get())]
        settings['scheme_check'] = ['tuple', (int(self.scheme_1_check.get()), int(self.scheme_2_check.get()), int(self.scheme_3_check.get()), int(self.scheme_4_check.get()))]
        settings['scheme_dropdown'] = ['tuple', (int(self.scheme_1_dropdown.integer_value), int(self.scheme_2_dropdown.integer_value), int(self.scheme_3_dropdown.integer_value), int(self.scheme_4_dropdown.integer_value))]
        settings['color_scale_dropdown'] = ['tuple', (int(self.color_scale_1_dropdown.integer_value), int(self.color_scale_2_dropdown.integer_value), int(self.color_scale_3_dropdown.integer_value), int(self.color_scale_4_dropdown.integer_value))]
        settings['sequence_entry'] = ['tuple', (self.sequence_1_entry.get(), self.sequence_2_entry.get(), self.sequence_3_entry.get(), self.sequence_4_entry.get())]
        # settings['OT_focus_x'] = ['tuple', (float(self.OT_focus1_x.get()), float(self.OT_focus2_x.get()), float(self.OT_focus3_x.get()), float(self.OT_focus4_x.get()))]
        # settings['OT_focus_y'] = ['tuple', (float(self.OT_focus1_y.get()), float(self.OT_focus2_y.get()), float(self.OT_focus3_y.get()), float(self.OT_focus4_y.get()))]
        # settings['OT_color_point_x'] = ['tuple', (self.OT_measure_point1_x.get(), self.OT_measure_point2_x.get(), self.OT_measure_point3_x.get(), self.OT_measure_point4_x.get())]
        # settings['OT_color_point_y'] = ['tuple', (self.OT_measure_point1_y.get(), self.OT_measure_point2_y.get(), self.OT_measure_point3_y.get(), self.OT_measure_point4_y.get())]
        # settings['OT_rotation'] = ['tuple', (float(self.OT_rotation1.get()), float(self.OT_rotation2.get()), float(self.OT_rotation3.get()), float(self.OT_rotation4.get()))]
        # settings['OT_radius1'] = ['tuple', (float(self.OT_radius1_1.get()), float(self.OT_radius1_2.get()), float(self.OT_radius1_3.get()), float(self.OT_radius1_4.get()))]
        # settings['OT_radius2'] = ['tuple', (float(self.OT_radius2_1.get()), float(self.OT_radius2_2.get()), float(self.OT_radius2_3.get()), float(self.OT_radius2_4.get()))]
        # settings['OT_starting_width'] = ['tuple', (float(self.OT_starting_width1.get()), float(self.OT_starting_width2.get()), float(self.OT_starting_width3.get()), float(self.OT_starting_width4.get()))]
        # settings['OT_width_deflection'] = ['tuple', (float(self.OT_width_deflection1.get()), float(self.OT_width_deflection2.get()), float(self.OT_width_deflection3.get()), float(self.OT_width_deflection4.get()))]
        # settings['OT_loop_distance'] = ['tuple', (float(self.OT_loop_distance1.get()), float(self.OT_loop_distance2.get()), float(self.OT_loop_distance3.get()), float(self.OT_loop_distance4.get()))]
        # settings['OT_trap_count'] = ['tuple', (float(self.OT_trap_count1.get()), float(self.OT_trap_count2.get()), float(self.OT_trap_count3.get()), float(self.OT_trap_count4.get()))]
        settings['OT_focus1_x'] = ['float', float(self.OT_focus1_x.get())]
        settings['OT_focus1_y'] = ['float', float(self.OT_focus1_y.get())]
        settings['OT_focus2_x'] = ['float', float(self.OT_focus2_x.get())]
        settings['OT_focus2_y'] = ['float', float(self.OT_focus2_y.get())]
        settings['OT_focus3_x'] = ['float', float(self.OT_focus3_x.get())]
        settings['OT_focus3_y'] = ['float', float(self.OT_focus3_y.get())]
        settings['OT_focus4_x'] = ['float', float(self.OT_focus4_x.get())]
        settings['OT_focus4_y'] = ['float', float(self.OT_focus4_y.get())]
        settings['OT_rotation1'] = ['float', float(self.OT_rotation1.get())]
        settings['OT_rotation2'] = ['float', float(self.OT_rotation2.get())]
        settings['OT_rotation3'] = ['float', float(self.OT_rotation3.get())]
        settings['OT_rotation4'] = ['float', float(self.OT_rotation4.get())]
        settings['OT_radius1_1'] = ['float', float(self.OT_radius1_1.get())]
        settings['OT_radius1_2'] = ['float', float(self.OT_radius1_2.get())]
        settings['OT_radius1_3'] = ['float', float(self.OT_radius1_3.get())]
        settings['OT_radius1_4'] = ['float', float(self.OT_radius1_4.get())]
        settings['OT_radius2_1'] = ['float', float(self.OT_radius2_1.get())]
        settings['OT_radius2_2'] = ['float', float(self.OT_radius2_2.get())]
        settings['OT_radius2_3'] = ['float', float(self.OT_radius2_3.get())]
        settings['OT_radius2_4'] = ['float', float(self.OT_radius2_4.get())]
        settings['OT_trap_count1'] = ['int', int(self.OT_trap_count1.get())]
        settings['OT_trap_count2'] = ['int', int(self.OT_trap_count2.get())]
        settings['OT_trap_count3'] = ['int', int(self.OT_trap_count3.get())]
        settings['OT_trap_count4'] = ['int', int(self.OT_trap_count4.get())]
        settings['OT_starting_width1'] = ['float', float(self.OT_starting_width1.get())]
        settings['OT_starting_width2'] = ['float', float(self.OT_starting_width2.get())]
        settings['OT_starting_width3'] = ['float', float(self.OT_starting_width3.get())]
        settings['OT_starting_width4'] = ['float', float(self.OT_starting_width4.get())]
        settings['OT_width_deflection1'] = ['float', float(self.OT_width_deflection1.get())]
        settings['OT_width_deflection2'] = ['float', float(self.OT_width_deflection2.get())]
        settings['OT_width_deflection3'] = ['float', float(self.OT_width_deflection3.get())]
        settings['OT_width_deflection4'] = ['float', float(self.OT_width_deflection4.get())]
        settings['OT_measure_point1_x'] = ['float', float(self.OT_measure_point1_x.get())]
        settings['OT_measure_point1_y'] = ['float', float(self.OT_measure_point1_y.get())]
        settings['OT_measure_point2_x'] = ['float', float(self.OT_measure_point2_x.get())]
        settings['OT_measure_point2_y'] = ['float', float(self.OT_measure_point2_y.get())]
        settings['OT_measure_point3_x'] = ['float', float(self.OT_measure_point3_x.get())]
        settings['OT_measure_point3_y'] = ['float', float(self.OT_measure_point3_y.get())]
        settings['OT_measure_point4_x'] = ['float', float(self.OT_measure_point4_x.get())]
        settings['OT_measure_point4_y'] = ['float', float(self.OT_measure_point4_y.get())]
        settings['repeat_colors_check'] = ['int', int(self.repeat_colors_check.get())]
        settings['color_repeat'] = ['float', float(self.color_repeat.get())]
        settings['OT_loop_distance1'] = ['float', float(self.OT_loop_distance1.get())]
        settings['OT_loop_distance2'] = ['float', float(self.OT_loop_distance2.get())]
        settings['OT_loop_distance3'] = ['float', float(self.OT_loop_distance3.get())]
        settings['OT_loop_distance4'] = ['float', float(self.OT_loop_distance4.get())]
        settings['black_background_check'] = ['int', int(self.black_background_check.get())]
        settings['load_filename'] = ['str', self.load_filename.get()]
        settings['save_filename'] = ['str', self.save_filename.get()]
        ##/////////////////////////////////##
        # for key in settings.keys():
        #    if settings[key][0] == 'list':
        #       settings[key][1] = settings[key][1].replace(' ','')
        #       settings[key][1] = settings[key][1].split(',')
        #       settings[key][1][0] = float(settings[key][1][0])
        #       settings[key][1][1] = float(settings[key][1][1])
        return settings
    def values_from_object_to_GUI(self): #
        # entries = ['x_min','x_max','y_min','y_max','iterations',
                   # 'c_real','c_imag','image_width','image_height',
                   # 'rotation','image_name','bailout_value','equation',
                   # 'OT_focus1_x','OT_focus2_x','OT_focus3_x','OT_focus4_x',
                   # 'OT_focus1_y','OT_focus2_y','OT_focus3_y','OT_focus4_y',
                   # 'OT_rotation1','OT_rotation2','OT_rotation3','OT_rotation4',
                   # 'OT_radius1_1','OT_radius1_2','OT_radius1_3','OT_radius1_4',
                   # 'OT_radius2_1','OT_radius2_2','OT_radius2_3','OT_radius2_4',
                   # 'OT_starting_width1','OT_starting_width2','OT_starting_width3','OT_starting_width4',
                   # 'OT_width_deflection1','OT_width_deflection2','OT_width_deflection3','OT_width_deflection4',
                   # 'OT_measure_point1_x','OT_measure_point2_x','OT_measure_point3_x','OT_measure_point4_x',
                   # 'OT_measure_point1_y','OT_measure_point2_y','OT_measure_point3_y','OT_measure_point4_y',
                   # 'color_repeat',
                   # 'OT_loop_distance1','OT_loop_distance2','OT_loop_distance3','OT_loop_distance4',
                   # 'OT_trap_count1','OT_trap_count2','OT_trap_count3','OT_trap_count4']
        # checkbuttons = ['repeat_colors_check','black_background_check']
        try:
            self.x_min.delete(0, "end")
            self.x_min.insert("end", str(self.parent.fractal_object.settings['x_min'][1]))
            self.x_max.delete(0, "end")
            self.x_max.insert("end", self.parent.fractal_object.settings['x_max'][1])
            self.y_min.delete(0, "end")
            self.y_min.insert("end", self.parent.fractal_object.settings['y_min'][1])
            self.y_max.delete(0, "end")
            self.y_max.insert("end", self.parent.fractal_object.settings['y_max'][1])
            self.iterations.delete(0, "end")
            self.iterations.insert("end", self.parent.fractal_object.settings['iterations'][1])
            self.c_formula.set(self.parent.fractal_object.settings['c_formula'][1])
            if self.c_formula.get() == 1:
                self.x_yi.invoke()
            elif self.c_formula.get() == 2:
                self.a_bi.invoke()
            self.c_real.delete(0, "end")
            self.c_real.insert("end", self.parent.fractal_object.settings['c_real'][1])
            self.c_imag.delete(0, "end")
            self.c_imag.insert("end", self.parent.fractal_object.settings['c_imag'][1])
            self.image_width.delete(0, "end")
            self.image_width.insert("end", self.parent.fractal_object.settings['image_width'][1])
            self.image_height.delete(0, "end")
            self.image_height.insert("end", self.parent.fractal_object.settings['image_height'][1])
            self.rotation.delete(0, "end")
            self.rotation.insert("end", self.parent.fractal_object.settings['rotation'][1])
            self.image_name.delete(0, "end")
            self.image_name.insert("end", self.parent.fractal_object.settings['image_name'][1])
            self.bailout_value.delete(0, "end")
            self.bailout_value.insert("end", self.parent.fractal_object.settings['bailout_value'][1])
            # self.thread_count.delete(0, "end")
            # self.thread_count.insert("end", self.parent.fractal_object.settings['thread_count'][1])
            self.equation.delete(0, "end")
            self.equation.insert("end", self.parent.fractal_object.settings['equation'][1])
            if self.parent.canvas_object.proportion_rectangle_check.get() != self.parent.fractal_object.settings['proportion_rectangle_check'][1]:
                self.proportion_rectangle_button.invoke()
            if self.scheme_1_check.get() != self.parent.fractal_object.settings['scheme_check'][1][0]:
                self.scheme_1_button.invoke()
            self.scheme_1_dropdown_value = self.parent.fractal_object.settings['scheme_dropdown'][1][0]
            self.scheme_1_dropdown.box_update(self.scheme_1_dropdown_value)
            self.color_scale_1_dropdown_value = self.parent.fractal_object.settings['color_scale_dropdown'][1][0]
            self.color_scale_1_dropdown.box_update(self.color_scale_1_dropdown_value)
            if self.scheme_2_check.get() != self.parent.fractal_object.settings['scheme_check'][1][1]:
                self.scheme_2_button.invoke()
            self.scheme_2_dropdown_value = self.parent.fractal_object.settings['scheme_dropdown'][1][1]
            self.scheme_2_dropdown.box_update(self.scheme_2_dropdown_value)
            self.color_scale_2_dropdown_value = self.parent.fractal_object.settings['color_scale_dropdown'][1][1]
            self.color_scale_2_dropdown.box_update(self.color_scale_2_dropdown_value)
            self.scheme_3_check
            if self.scheme_3_check.get() != self.parent.fractal_object.settings['scheme_check'][1][2]:
                self.scheme_3_button.invoke()
            self.scheme_3_dropdown_value = self.parent.fractal_object.settings['scheme_dropdown'][1][2]
            self.scheme_3_dropdown.box_update(self.scheme_3_dropdown_value)
            self.color_scale_3_dropdown_value = self.parent.fractal_object.settings['color_scale_dropdown'][1][2]
            self.color_scale_3_dropdown.box_update(self.color_scale_3_dropdown_value)
            if self.scheme_4_check.get() != self.parent.fractal_object.settings['scheme_check'][1][3]:
                self.scheme_4_button.invoke()
            self.scheme_4_dropdown_value = self.parent.fractal_object.settings['scheme_dropdown'][1][3]
            self.scheme_4_dropdown.box_update(self.scheme_4_dropdown_value)
            self.color_scale_4_dropdown_value = self.parent.fractal_object.settings['color_scale_dropdown'][1][3]
            self.color_scale_4_dropdown.box_update(self.color_scale_4_dropdown_value)
            self.sequence_1_entry.delete(0, "end")
            self.sequence_1_entry.insert("end", self.parent.fractal_object.settings['sequence_entry'][1][0])
            self.sequence_2_entry.delete(0, "end")
            self.sequence_2_entry.insert("end", self.parent.fractal_object.settings['sequence_entry'][1][1])
            self.sequence_3_entry.delete(0, "end")
            self.sequence_3_entry.insert("end", self.parent.fractal_object.settings['sequence_entry'][1][2])
            self.sequence_4_entry.delete(0, "end")
            self.sequence_4_entry.insert("end", self.parent.fractal_object.settings['sequence_entry'][1][3])
            self.OT_focus1_x.delete(0, "end")
            self.OT_focus1_x.insert("end", str(self.parent.fractal_object.settings['OT_focus1_x'][1]))
            self.OT_focus2_x.delete(0, "end")
            self.OT_focus2_x.insert("end", str(self.parent.fractal_object.settings['OT_focus2_x'][1]))
            self.OT_focus3_x.delete(0, "end")
            self.OT_focus3_x.insert("end", str(self.parent.fractal_object.settings['OT_focus3_x'][1]))
            self.OT_focus4_x.delete(0, "end")
            self.OT_focus4_x.insert("end", str(self.parent.fractal_object.settings['OT_focus4_x'][1]))
            self.OT_focus1_y.delete(0, "end")
            self.OT_focus1_y.insert("end", str(self.parent.fractal_object.settings['OT_focus1_y'][1]))
            self.OT_focus2_y.delete(0, "end")
            self.OT_focus2_y.insert("end", str(self.parent.fractal_object.settings['OT_focus2_y'][1]))
            self.OT_focus3_y.delete(0, "end")
            self.OT_focus3_y.insert("end", str(self.parent.fractal_object.settings['OT_focus3_y'][1]))
            self.OT_focus4_y.delete(0, "end")
            self.OT_focus4_y.insert("end", str(self.parent.fractal_object.settings['OT_focus4_y'][1]))
            self.OT_rotation1.delete(0, "end")
            self.OT_rotation1.insert("end", self.parent.fractal_object.settings['OT_rotation1'][1])
            self.OT_rotation2.delete(0, "end")
            self.OT_rotation2.insert("end", self.parent.fractal_object.settings['OT_rotation2'][1])
            self.OT_rotation3.delete(0, "end")
            self.OT_rotation3.insert("end", self.parent.fractal_object.settings['OT_rotation3'][1])
            self.OT_rotation4.delete(0, "end")
            self.OT_rotation4.insert("end", self.parent.fractal_object.settings['OT_rotation4'][1])
            self.OT_radius1_1.delete(0, "end")
            self.OT_radius1_1.insert("end", self.parent.fractal_object.settings['OT_radius1_1'][1])
            self.OT_radius1_2.delete(0, "end")
            self.OT_radius1_2.insert("end", self.parent.fractal_object.settings['OT_radius1_2'][1])
            self.OT_radius1_3.delete(0, "end")
            self.OT_radius1_3.insert("end", self.parent.fractal_object.settings['OT_radius1_3'][1])
            self.OT_radius1_4.delete(0, "end")
            self.OT_radius1_4.insert("end", self.parent.fractal_object.settings['OT_radius1_4'][1])
            self.OT_radius2_1.delete(0, "end")
            self.OT_radius2_1.insert("end", self.parent.fractal_object.settings['OT_radius2_1'][1])
            self.OT_radius2_2.delete(0, "end")
            self.OT_radius2_2.insert("end", self.parent.fractal_object.settings['OT_radius2_2'][1])
            self.OT_radius2_3.delete(0, "end")
            self.OT_radius2_3.insert("end", self.parent.fractal_object.settings['OT_radius2_3'][1])
            self.OT_radius2_4.delete(0, "end")
            self.OT_radius2_4.insert("end", self.parent.fractal_object.settings['OT_radius2_4'][1])
            self.OT_starting_width1.delete(0, "end")
            self.OT_starting_width1.insert("end", self.parent.fractal_object.settings['OT_starting_width1'][1])
            self.OT_starting_width2.delete(0, "end")
            self.OT_starting_width2.insert("end", self.parent.fractal_object.settings['OT_starting_width2'][1])
            self.OT_starting_width3.delete(0, "end")
            self.OT_starting_width3.insert("end", self.parent.fractal_object.settings['OT_starting_width3'][1])
            self.OT_starting_width4.delete(0, "end")
            self.OT_starting_width4.insert("end", self.parent.fractal_object.settings['OT_starting_width4'][1])
            self.OT_width_deflection1.delete(0, "end")
            self.OT_width_deflection1.insert("end", self.parent.fractal_object.settings['OT_width_deflection1'][1])
            self.OT_width_deflection2.delete(0, "end")
            self.OT_width_deflection2.insert("end", self.parent.fractal_object.settings['OT_width_deflection2'][1])
            self.OT_width_deflection3.delete(0, "end")
            self.OT_width_deflection3.insert("end", self.parent.fractal_object.settings['OT_width_deflection3'][1])
            self.OT_width_deflection4.delete(0, "end")
            self.OT_width_deflection4.insert("end", self.parent.fractal_object.settings['OT_width_deflection4'][1])
            self.OT_measure_point1_x.delete(0, "end")
            self.OT_measure_point1_x.insert("end", str(self.parent.fractal_object.settings['OT_measure_point1_x'][1]))
            self.OT_measure_point2_x.delete(0, "end")
            self.OT_measure_point2_x.insert("end", str(self.parent.fractal_object.settings['OT_measure_point2_x'][1]))
            self.OT_measure_point3_x.delete(0, "end")
            self.OT_measure_point3_x.insert("end", str(self.parent.fractal_object.settings['OT_measure_point3_x'][1]))
            self.OT_measure_point4_x.delete(0, "end")
            self.OT_measure_point4_x.insert("end", str(self.parent.fractal_object.settings['OT_measure_point4_x'][1]))
            self.OT_measure_point1_y.delete(0, "end")
            self.OT_measure_point1_y.insert("end", str(self.parent.fractal_object.settings['OT_measure_point1_y'][1]))
            self.OT_measure_point2_y.delete(0, "end")
            self.OT_measure_point2_y.insert("end", str(self.parent.fractal_object.settings['OT_measure_point2_y'][1]))
            self.OT_measure_point3_y.delete(0, "end")
            self.OT_measure_point3_y.insert("end", str(self.parent.fractal_object.settings['OT_measure_point3_y'][1]))
            self.OT_measure_point4_y.delete(0, "end")
            self.OT_measure_point4_y.insert("end", str(self.parent.fractal_object.settings['OT_measure_point4_y'][1]))
            if self.repeat_colors_check.get() != self.parent.fractal_object.settings['repeat_colors_check'][1]:
                self.repeat_colors_button.invoke()
            self.color_repeat.delete(0, "end")
            self.color_repeat.insert("end", str(self.parent.fractal_object.settings['color_repeat'][1]))
            self.OT_loop_distance1.delete(0, "end")
            self.OT_loop_distance1.insert("end", self.parent.fractal_object.settings['OT_loop_distance1'][1])
            self.OT_loop_distance2.delete(0, "end")
            self.OT_loop_distance2.insert("end", self.parent.fractal_object.settings['OT_loop_distance2'][1])
            self.OT_loop_distance3.delete(0, "end")
            self.OT_loop_distance3.insert("end", self.parent.fractal_object.settings['OT_loop_distance3'][1])
            self.OT_loop_distance4.delete(0, "end")
            self.OT_loop_distance4.insert("end", self.parent.fractal_object.settings['OT_loop_distance4'][1])
            self.OT_trap_count1.delete(0, "end")
            self.OT_trap_count1.insert("end", self.parent.fractal_object.settings['OT_trap_count1'][1])
            self.OT_trap_count2.delete(0, "end")
            self.OT_trap_count2.insert("end", self.parent.fractal_object.settings['OT_trap_count2'][1])
            self.OT_trap_count3.delete(0, "end")
            self.OT_trap_count3.insert("end", self.parent.fractal_object.settings['OT_trap_count3'][1])
            self.OT_trap_count4.delete(0, "end")
            self.OT_trap_count4.insert("end", self.parent.fractal_object.settings['OT_trap_count4'][1])
            if self.black_background_check.get() != self.parent.fractal_object.settings['black_background_check'][1]:
                self.black_background_button.invoke()
            self.parent.text_out.write("\n!!!!! Settings Have Been Loaded !!!!!")
        except: self.parent.text_out.write("\n!!!!! Failure In Loading Settings !!!!!")
    def save_settings_file(self,default=False):
        self.parent.fractal_object.settings = self.GUI_settings_to_dict() #GUI gather settings into dictionary, dictionary given to object
        self.parent.fractal_object.save_settings(default=default)
        if self.batch: self.parent.window2_object.batch_GUI_settings_to_dict()
        if self.batch: self.parent.window2_object.save_batch_settings(manual=True)
    def load_settings_from_file(self, the_file=None):
        if the_file == None: the_file = self.parent.fractal_object.settings['load_filename'][1] = self.load_filename.get()
        self.parent.fractal_object.settings_import_from_file(the_file)
        if self.batch: self.parent.window2_object.batch_settings_import_from_file(the_file)
        self.values_from_object_to_GUI()
        # self.parent.window2_object.batch_values_from_object_to_GUI()
    def generate_fractal(self):
        self.parent.fractal_object.t = time.clock()
        self.parent.fractal_object.settings = self.GUI_settings_to_dict()
        self.parent.fractal_object.save_settings()
        self.parent.start_fractal()
        self.master.after(1, lambda: self.master.focus_force())
    def load_default_settings(self):
        if os.path.isfile(os.getcwd().replace('\\','/') + "/save/default.json"):
            self.load_settings_from_file(os.getcwd().replace('\\','/') + "/save/default.json")
            self.parent.text_out.write("\nDefault settings have been loaded!")
        else: self.parent.text_out.write("\nFound no default settings!")