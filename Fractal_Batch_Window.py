import tkinter as tk
from tkinter import Toplevel,Label,ttk,Entry,IntVar,Checkbutton,Frame,Button
from Vertical_Scroll import VerticalScrollGrid
import os

class BatchWindow:
    def __init__(self, grandmother):
        self.mother = grandmother #in a sense logical, but still weird
        self.batch_window = Toplevel()
        self.batch_window.wm_title("Batch Settings Panel")
        self.batch_window.minsize(width=850, height=955)
        self.batch_window.maxsize(width=850, height=955)
        self.scrolled_frame = VerticalScrollGrid(self.batch_window)
        self.scrolled_frame.grid(row=0,column=0,sticky='EW')
        self.batch_window.columnconfigure(0, weight=1)
        self.batch_window.rowconfigure(0, weight=1)

        # to be used to write batch data values to and from files. Otherwise would not be necessary
        self.batch_data_values = {}
        ##-----------------##
        Label(self.scrolled_frame.frame, text="Parameter").grid(row=0,column=0)
        Label(self.scrolled_frame.frame, text="Start").grid(row=0,column=1)
        Label(self.scrolled_frame.frame, text="End").grid(row=0,column=2)
        Label(self.scrolled_frame.frame, text="Delta Mode").grid(row=0,column=3)
        Label(self.scrolled_frame.frame, text="Delta").grid(row=0,column=4)
        Label(self.scrolled_frame.frame, text="Smooth Start").grid(row=0,column=5)
        Label(self.scrolled_frame.frame, text="Smooth End").grid(row=0,column=6)
        Label(self.scrolled_frame.frame, text="Cycle Mode").grid(row=0,column=7)
        Label(self.scrolled_frame.frame, text="Cycle Period").grid(row=0,column=8)
        ttk.Separator(self.scrolled_frame.frame, orient="horizontal").grid(row=1, columnspan=9, sticky="ew")
        ##-----------------##
        class line_item:
            def __init__(self, parameter_name, which_frame, row_number, start_value, end_value):
                #Label
                Label(which_frame, text=parameter_name + ": ").grid(row=row_number,column=0)
                self.current_value = start_value
                #Start Value
                self.start_entry = Entry(which_frame, justify = "right", width=8)
                self.start_entry.insert("end", str(start_value))
                self.start_entry.grid(row=row_number, column=1)
                #End Value
                self.end_entry = Entry(which_frame, justify = "right", width=8)
                self.end_entry.insert("end", str(end_value))
                self.end_entry.grid(row=row_number, column=2)
                self.end_entry.config(state = "disabled")
                #Delta Checkbox
                self.delta_check = IntVar()
                self.delta_check.set(1)
                self.delta_button = Checkbutton(which_frame, text = "Delta Method", variable = self.delta_check, command=self.delta_button_toggle)
                self.delta_button.grid(row=row_number,column=3)
                #Delta Value
                self.delta = Entry(which_frame, justify = "right", width=8)
                self.delta.insert("end", '0')
                self.delta.grid(row=row_number, column=4)
                #Smooth Start Checkbox
                self.smooth_start_check = IntVar()
                self.smooth_start_check.set(1)
                self.smooth_start_button = Checkbutton(which_frame, text = "Smooth Start", variable = self.smooth_start_check)
                self.smooth_start_button.grid(row=row_number,column=5)
                self.smooth_start_button.config(state = "disabled")
                #Smooth End Checkbox
                self.smooth_end_check = IntVar()
                self.smooth_end_check.set(1)
                self.smooth_end_button = Checkbutton(which_frame, text = "Smooth End", variable = self.smooth_end_check)
                self.smooth_end_button.grid(row=row_number,column=6)
                self.smooth_end_button.config(state = "disabled")
                #Cycle Checkbox
                self.cycle_check = IntVar()
                self.cycle_check.set(0)
                self.cycle_button = Checkbutton(which_frame, text = "Cycle", variable = self.cycle_check, command = self.cycle_button_toggle)
                self.cycle_button.grid(row=row_number,column=7)
                #Cycle Period
                self.cycle_period = Entry(which_frame, justify = "right", width=8)
                self.cycle_period.insert("end", '120')
                self.cycle_period.grid(row=row_number, column=8)
                self.cycle_period.config(state = "disabled")
                return
            def delta_button_toggle(self, event=None):
                checked = self.delta_check.get()
                if self.cycle_check.get() == self.delta_check.get() == 1:
                    self.cycle_button.invoke()
                if checked:
                    self.delta.config(state = NORMAL)
                    self.end_entry.config(state = "disabled")
                    self.smooth_start_check.set(0)
                    self.smooth_end_check.set(0)
                    self.smooth_start_button.config(state = "disabled")
                    self.smooth_end_button.config(state = "disabled")
                else:
                    self.delta.config(state = "disabled")
                    self.end_entry.config(state = NORMAL)
                    if self.cycle_check.get() == 0:
                        self.smooth_start_button.config(state = NORMAL)
                        self.smooth_end_button.config(state = NORMAL)
            def cycle_button_toggle(self, event=None):
                checked = self.cycle_check.get()
                if self.cycle_check.get() == self.delta_check.get() == 1:
                    self.delta_button.invoke()
                if checked:
                    self.cycle_period.config(state = NORMAL)
                    self.end_entry.config(state = NORMAL)
                    self.smooth_start_check.set(0)
                    self.smooth_end_check.set(0)
                    self.smooth_start_button.config(state = "disabled")
                    self.smooth_end_button.config(state = "disabled")
                else:
                    self.cycle_period.config(state = "disabled")
                    if self.delta_check.get() == 0:
                        self.smooth_start_button.config(state = NORMAL)
                        self.smooth_end_button.config(state = NORMAL)
                        self.end_entry.config(state = NORMAL)
        ##-----------------##
        self.batch_data={}
        self.batch_data['x_min'] = line_item('x_min',self.scrolled_frame.frame,2,-2,-1)
        self.batch_data['x_max'] = line_item('x_max',self.scrolled_frame.frame,3,2,-1)
        self.batch_data['y_min'] = line_item('y_min',self.scrolled_frame.frame,4,-2,-1)
        self.batch_data['y_max'] = line_item('y_max',self.scrolled_frame.frame,5,2,-1)
        self.batch_data['iterations'] = line_item('iterations',self.scrolled_frame.frame,6,30,40)
        self.batch_data['rotation'] = line_item('rotation',self.scrolled_frame.frame,9,270,0)
        self.batch_data['bailout_value'] = line_item('bailout_value',self.scrolled_frame.frame,10,30,40)
        self.batch_data['c_real'] = line_item('c_real',self.scrolled_frame.frame,11,-.5,.7)
        self.batch_data['c_imag'] = line_item('c_imag',self.scrolled_frame.frame,12,-.8,.1)
        self.batch_data['OT_focus1_x'] = line_item('OT_focus1_x',self.scrolled_frame.frame,13,30,40)
        self.batch_data['OT_focus1_y'] = line_item('OT_focus1_y',self.scrolled_frame.frame,14,30,40)
        self.batch_data['OT_focus2_x'] = line_item('OT_focus2_x',self.scrolled_frame.frame,15,30,40)
        self.batch_data['OT_focus2_y'] = line_item('OT_focus2_y',self.scrolled_frame.frame,16,30,40)
        self.batch_data['OT_focus3_x'] = line_item('OT_focus3_x',self.scrolled_frame.frame,17,30,40)
        self.batch_data['OT_focus3_y'] = line_item('OT_focus3_y',self.scrolled_frame.frame,18,30,40)
        self.batch_data['OT_focus4_x'] = line_item('OT_focus4_x',self.scrolled_frame.frame,19,30,40)
        self.batch_data['OT_focus4_y'] = line_item('OT_focus4_y',self.scrolled_frame.frame,20,30,40)
        self.batch_data['OT_rotation1'] = line_item('OT_rotation1',self.scrolled_frame.frame,21,30,40)
        self.batch_data['OT_rotation2'] = line_item('OT_rotation2',self.scrolled_frame.frame,22,30,40)
        self.batch_data['OT_rotation3'] = line_item('OT_rotation3',self.scrolled_frame.frame,23,30,40)
        self.batch_data['OT_rotation4'] = line_item('OT_rotation4',self.scrolled_frame.frame,24,30,40)
        self.batch_data['OT_radius1_1'] = line_item('OT_radius1_1',self.scrolled_frame.frame,25,30,40)
        self.batch_data['OT_radius1_2'] = line_item('OT_radius1_2',self.scrolled_frame.frame,26,30,40)
        self.batch_data['OT_radius1_3'] = line_item('OT_radius1_3',self.scrolled_frame.frame,27,30,40)
        self.batch_data['OT_radius1_4'] = line_item('OT_radius1_4',self.scrolled_frame.frame,28,30,40)
        self.batch_data['OT_radius2_1'] = line_item('OT_radius2_1',self.scrolled_frame.frame,29,30,40)
        self.batch_data['OT_radius2_2'] = line_item('OT_radius2_2',self.scrolled_frame.frame,30,30,40)
        self.batch_data['OT_radius2_3'] = line_item('OT_radius2_3',self.scrolled_frame.frame,31,30,40)
        self.batch_data['OT_radius2_4'] = line_item('OT_radius2_4',self.scrolled_frame.frame,32,30,40)
        self.batch_data['OT_trap_count1'] = line_item('OT_trap_count1',self.scrolled_frame.frame,33,30,40)
        self.batch_data['OT_trap_count2'] = line_item('OT_trap_count2',self.scrolled_frame.frame,34,30,40)
        self.batch_data['OT_trap_count3'] = line_item('OT_trap_count3',self.scrolled_frame.frame,35,30,40)
        self.batch_data['OT_trap_count4'] = line_item('OT_trap_count4',self.scrolled_frame.frame,36,30,40)
        self.batch_data['OT_starting_width1'] = line_item('OT_starting_width1',self.scrolled_frame.frame,37,30,40)
        self.batch_data['OT_starting_width2'] = line_item('OT_starting_width2',self.scrolled_frame.frame,38,30,40)
        self.batch_data['OT_starting_width3'] = line_item('OT_starting_width3',self.scrolled_frame.frame,39,30,40)
        self.batch_data['OT_starting_width4'] = line_item('OT_starting_width4',self.scrolled_frame.frame,40,30,40)
        self.batch_data['OT_width_deflection1'] = line_item('OT_width_deflection1',self.scrolled_frame.frame,41,30,40)
        self.batch_data['OT_width_deflection2'] = line_item('OT_width_deflection2',self.scrolled_frame.frame,42,30,40)
        self.batch_data['OT_width_deflection3'] = line_item('OT_width_deflection3',self.scrolled_frame.frame,43,30,40)
        self.batch_data['OT_width_deflection4'] = line_item('OT_width_deflection4',self.scrolled_frame.frame,44,30,40)
        self.batch_data['OT_measure_point1_x'] = line_item('OT_measure_point1_x',self.scrolled_frame.frame,45,30,40)
        self.batch_data['OT_measure_point1_y'] = line_item('OT_measure_point1_y',self.scrolled_frame.frame,46,30,40)
        self.batch_data['OT_measure_point2_x'] = line_item('OT_measure_point2_x',self.scrolled_frame.frame,47,30,40)
        self.batch_data['OT_measure_point2_y'] = line_item('OT_measure_point2_y',self.scrolled_frame.frame,48,30,40)
        self.batch_data['OT_measure_point3_x'] = line_item('OT_measure_point3_x',self.scrolled_frame.frame,49,30,40)
        self.batch_data['OT_measure_point3_y'] = line_item('OT_measure_point3_y',self.scrolled_frame.frame,50,30,40)
        self.batch_data['OT_measure_point4_x'] = line_item('OT_measure_point4_x',self.scrolled_frame.frame,51,30,40)
        self.batch_data['OT_measure_point4_y'] = line_item('OT_measure_point4_y',self.scrolled_frame.frame,52,30,40)
        self.batch_data['OT_loop_distance1'] = line_item('OT_loop_distance1',self.scrolled_frame.frame,53,5,5)
        self.batch_data['OT_loop_distance2'] = line_item('OT_loop_distance2',self.scrolled_frame.frame,54,5,5)
        self.batch_data['OT_loop_distance3'] = line_item('OT_loop_distance3',self.scrolled_frame.frame,55,5,5)
        self.batch_data['OT_loop_distance4'] = line_item('OT_loop_distance4',self.scrolled_frame.frame,56,5,5)
        ##-----------------##
        bottom_frame = Frame(self.batch_window)
        bottom_frame.grid(row=5,column=0,sticky="EW")
        ttk.Separator(bottom_frame, orient="horizontal").grid(row=64, columnspan=3, sticky="ew")
        Label(bottom_frame, text="Image Numbering Start: ").grid(row=65,column=0)
        self.image_numbering_entry = Entry(bottom_frame, justify = "right", width=8)
        self.image_numbering_entry.insert("end", '1')
        self.image_numbering_entry.grid(row=65, column=1)
        self.batch_data['image_number'] = int(self.image_numbering_entry.get())
        Label(bottom_frame, text="Number Of Steps: ").grid(row=66, column=0)
        self.number_of_steps_entry = Entry(bottom_frame, justify = "right", width=8)
        self.number_of_steps_entry.insert("end", '10')
        self.number_of_steps_entry.grid(row=66,column=1)
        self.batch_data['number_of_steps'] = int(self.number_of_steps_entry.get())
        self.begin_batch_button = Button(bottom_frame, text="Begin Batch", command=self.batch_thread)
        self.begin_batch_button.grid(row=66,column=2,sticky="ew")
        self.get_settings_button = Button(bottom_frame, text="Get Settings From Main Window", command=self.get_settings_from_fractal_object)
        self.get_settings_button.grid(row=65,column=2)
        self.save_batch_settings_button = Button(bottom_frame, text="Save Batch Settings", command=lambda: self.save_batch_settings(manual=True))
        self.save_batch_settings_button.grid(row=65, column=3,sticky="ew")
        self.load_batch_settings_button = Button(bottom_frame, text="Load Batch Settings", command=lambda: self.batch_settings_import_from_file(self.mother.fractal_object.settings['save_filename'][1]))
        self.load_batch_settings_button.grid(row=66,column=3,sticky="ew")
        return
    def save_batch_settings(self, manual=False):
        self.batch_GUI_settings_to_dict()
        if manual: f = open(self.mother.fractal_object.settings['save_filename'][1][:len(self.mother.fractal_object.settings['save_filename'][1])-4] + '_batch.txt', 'w')
        else:
            if os.path.isfile(os.getcwd().replace('\\','/') + "/save/recent_settings_batch.txt"):
                os.replace("/save/recent_settings.txt", "/save/recent_settings_old_batch.txt")
            f = open(os.getcwd().replace('\\','/') + '/save/recent_settings_batch.txt', 'w')
        json.dump(self.batch_data_values, f)
        # f.write('{')
        # for index, key in enumerate(self.batch_data.keys()):
        #    if index == len(self.batch_data)-1: line = "'" + key + "':" + str(self.batch_data[key]) + "\n" #if statement to make sure a comma doesn't get placed on the last line
        #    else: line = "'" + key + "':" + str(self.batch_data[key]) + ",\n"
        #    f.write(line)
        # f.write('}')
        f.close()
        self.parent.text_out.write("\nBatch settings have been saved!")
        return
    def batch_settings_import_from_file(self, filename):
        try:
            name = filename[:len(filename)-4] + "_batch.txt"
            self.batch_data_values = json.load(open(name))
            self.batch_values_from_dict_to_GUI()
            self.parent.text_out.write("\nBatch settings have been loaded!")
        except: self.parent.text_out.write("\nFailed to load batch settings!")
        return
    ##-----------------##
    def batch_GUI_settings_to_dict(self):
        for key in self.batch_data.keys():
            if key != 'image_number' and key != 'number_of_steps':
                self.batch_data_values[key]=[float(self.batch_data[key].start_entry.get()),float(self.batch_data[key].end_entry.get()),self.batch_data[key].delta_check.get(),float(self.batch_data[key].delta.get()),self.batch_data[key].smooth_start_check.get(),self.batch_data[key].smooth_end_check.get(),self.batch_data[key].cycle_check.get(),float(self.batch_data[key].cycle_period.get())]
                self.batch_data[key].current_value = float(self.batch_data[key].start_entry.get())
            else: self.batch_data_values[key]=int(self.batch_data[key])
    def batch_values_from_dict_to_GUI(self):
        for key in self.batch_data:
            if key != 'image_number' and key != 'number_of_steps':
                self.batch_data[key].start_entry.delete(0, "end")
                self.batch_data[key].start_entry.insert("end", str(self.batch_data_values[key][0]))
                self.batch_data[key].end_entry.delete(0, "end")
                self.batch_data[key].end_entry.insert("end", str(self.batch_data_values[key][1]))
                self.batch_data[key].delta.delete(0, "end")
                self.batch_data[key].delta.insert("end", str(self.batch_data_values[key][3]))
                self.batch_data[key].cycle_period.delete(0, "end")
                self.batch_data[key].cycle_period.insert("end", str(self.batch_data_values[key][7]))
                if self.batch_data[key].delta_check.get() != self.batch_data_values[key][2]:
                    self.batch_data[key].delta_check.invoke()
                if self.batch_data[key].smooth_start_check.get() != self.batch_data_values[key][4]:
                    self.batch_data[key].smooth_start_check.invoke()
                if self.batch_data[key].smooth_end_check.get() != self.batch_data_values[key][5]:
                    self.batch_data[key].smooth_end_check.invoke()
                if self.batch_data[key].cycle_check.get() != self.batch_data_values[key][6]:
                    self.batch_data[key].cycle_check.invoke()
        self.number_of_steps_entry.delete(0, "end")
        self.number_of_steps_entry.insert("end", str(self.batch_data_values['number_of_steps']))
        self.image_numbering_entry.delete(0, "end")
        self.image_numbering_entry.insert("end", str(self.batch_data_values['image_number']))
    def batch_thread(self):
        #self.mother.fractalobject.settings = self.mother.window1_object.GUI_settings_to_dict()
        self.batch_GUI_settings_to_dict()
        self.save_batch_settings()
        self.begin_batch_button.config(state="disabled")
        t = threading.Thread(target=self.batch_it)
        t.daemon = True
        t.start()
    def get_settings_from_fractal_object(self):
        self.mother.fractal_object.settings = self.mother.window1_object.GUI_settings_to_dict()
        for key in self.mother.fractal_object.settings:
            if key in self.batch_data:
                self.batch_data[key].start_entry.delete(0, "end")
                self.batch_data[key].start_entry.insert("end", str(self.mother.fractal_object.settings[key][1]))
        self.batch_GUI_settings_to_dict()
    def batch_it(self): #sounds like "bat shit"
        number_of_steps = int(self.number_of_steps_entry.get())
        self.batch_GUI_settings_to_dict()
        def batch_step(which_step):
            # batch data legend => [value,start,end,delta amount,delta toggle,smooth start,smooth end,cycle toggle,cycle period steps]
            for parameter in self.batch_data.keys():
                if parameter != 'image_number' and parameter != 'number_of_steps':
                    # print("parameter: " + str(parameter))
                    if self.batch_data[parameter].delta_check.get() == 1:
                        self.batch_data[parameter].current_value = self.batch_data_values[parameter][0] + which_step * self.batch_data_values[parameter][3]
                    else:
                        if (self.batch_data[parameter].smooth_start_check.get() != 1) and (self.batch_data[parameter].smooth_end_check.get() != 1) and (self.batch_data[parameter].cycle_check.get() != 1):
                            self.batch_data[parameter].current_value = which_step * (self.batch_data_values[parameter][1] - self.batch_data_values[parameter][0]) / self.batch_data['number_of_steps'] + self.batch_data_values[parameter][0]
                    # update mother.fractal_object settings
                    # recall, mother.fractal_object.settings[x][0] is the data type, and [x][1] is the value
                    if self.mother.fractal_object.settings[parameter][0] == 'int': self.mother.fractal_object.settings[parameter][1] = int(self.batch_data[parameter].current_value)
                    if self.mother.fractal_object.settings[parameter][0] == 'float': self.mother.fractal_object.settings[parameter][1] = self.batch_data[parameter].current_value
            self.mother.fractal_object.settings['image_name'][1] = self.mother.fractal_object.settings['image_name'][1][:len(self.mother.fractal_object.settings['image_name'][1])-4] + "-" + str(self.batch_data["image_number"]) + ".png"
            self.batch_data["image_number"]+=1
        starting_image_name = self.mother.fractal_object.settings['image_name'][1]
        for i in range(0,number_of_steps):
            self.mother.fractal_object.t = time.clock()
            self.mother.fractal_object.save_settings()
            batch_step(i+1)
            self.mother.window1_object.values_from_object_to_GUI()
            self.mother.fractal_object.compute()
            self.mother.fractal_object.settings['image_name'][1] = starting_image_name
        self.begin_batch_button.config(state="normal")
        return
