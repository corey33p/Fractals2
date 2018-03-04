import time
import datetime
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import math
from PIL import Image, ImageTk
import threading
import numpy as np
import json

float_formatter = lambda x: "%.4f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})

class fractal:
    def __init__(self, dictionary_of_settings, mother):
        self.preliminary_tasks_done = False
        self.settings = dictionary_of_settings
        self.mother = mother
        # self.canvas_object = canvas_object
        self.orbit_trap_list = (2,3,4,5,6)
        self.previous_settings = None
        self.previous_iterations = 'NA'
        self.previous_previous_iterations ='NA'
        self.packed_settings={}
        return

    def print_tensor(self, the_ndarray):
        if type(the_ndarray)!=np.ndarray:
            print(str(the_ndarray))
            return
        if len(the_ndarray.shape)!=3:
            print(str(the_ndarray))
            return
        for i in range(the_ndarray.shape[2]): print("\n"+str(the_ndarray[...,i]))
        return

    def compare_previous_settings(self):
        # will return 2 booleans:
        # one to show if the old coordinates can be used
        # and one to show if new iterations can be built off of old iterations

        # used to check if can build on old iterations if no orbit traps are active
        basic_settings_check = ('x_min','x_max','y_min','y_max','c_formula','c_real','c_imag','equation','image_width','image_height','rotation','bailout_value')
        # used to check if can build on old iterations with orbit traps active
        all_settings_check = ('x_min', 'x_max', 'y_min', 'y_max', 'c_formula', 'c_real', 'c_imag', 'image_width', 'image_height', 'rotation', 'bailout_value', 'equation', 'scheme_check', 'scheme_dropdown', 'color_scale_dropdown', 'sequence_entry', 'OT_focus1_x', 'OT_focus1_y', 'OT_focus2_x', 'OT_focus2_y', 'OT_focus3_x', 'OT_focus3_y', 'OT_focus4_x', 'OT_focus4_y', 'OT_rotation1', 'OT_rotation2', 'OT_rotation3', 'OT_rotation4', 'OT_radius1_1', 'OT_radius1_2', 'OT_radius1_3', 'OT_radius1_4', 'OT_radius2_1', 'OT_radius2_2', 'OT_radius2_3', 'OT_radius2_4', 'OT_trap_count1', 'OT_trap_count2', 'OT_trap_count3', 'OT_trap_count4', 'OT_starting_width1', 'OT_starting_width2', 'OT_starting_width3', 'OT_starting_width4', 'OT_width_deflection1', 'OT_width_deflection2', 'OT_width_deflection3', 'OT_width_deflection4', 'OT_measure_point1_x', 'OT_measure_point1_y', 'OT_measure_point2_x', 'OT_measure_point2_y', 'OT_measure_point3_x', 'OT_measure_point3_y', 'OT_measure_point4_x', 'OT_measure_point4_y', 'OT_loop_distance1', 'OT_loop_distance2', 'OT_loop_distance3', 'OT_loop_distance4', 'black_background_check')
        # used to check if can use old coordinate calculations
        coordinate_settings = ('x_min','x_max','y_min','y_max','image_width','image_height','rotation')
        if self.previous_settings == None:
            self.previous_settings = {}
            for setting in all_settings_check:
                self.previous_settings[setting] = self.settings[setting][1]
                # if self.settings[setting][0] == 'int':
                #    self.previous_settings[setting] = int(self.settings[setting][1])
                # elif self.settings[setting][0] == 'float':
                #    self.previous_settings[setting] = float(self.settings[setting][1])
                # elif self.settings[setting][0] == 'str':
                    # self.previous_settings[setting] = str(self.settings[setting][1])
            self.previous_previous_iterations = self.previous_iterations
            self.previous_iterations = self.settings['iterations']
            return False, False
        else:
            can_build_on_iterations_with_OT = True
            can_build_on_iterations_without_OT = True
            coordinate_settings_match = True
            new_previous_settings = {}
            for setting in all_settings_check:
                if self.previous_settings[setting] != self.settings[setting][1]:
                    can_build_on_iterations_with_OT = False
                    if setting in basic_settings_check: can_build_on_iterations_without_OT = False
                    if setting in coordinate_settings: coordinate_settings_match = False
                new_previous_settings[setting] = self.settings[setting][1]
            # if any orbit traps have changed, iterations must be performed again
            self.previous_settings = new_previous_settings
            if self.previous_iterations[1] <= self.settings['iterations'][1]:
                self.previous_previous_iterations = self.previous_iterations
                self.previous_iterations = self.settings['iterations']
                # need to add logic and a new return to distinguish if orbit traps are active
                return coordinate_settings_match, can_build_on_iterations_with_OT
            else: return coordinate_settings_match, False

    def package_settings(self):
        self.packed_settings['OT_focus_x'] = [self.settings['OT_focus1_x'][1],self.settings['OT_focus2_x'][1],self.settings['OT_focus3_x'][1],self.settings['OT_focus4_x'][1]]
        self.packed_settings['OT_focus_y'] = [self.settings['OT_focus1_y'][1],self.settings['OT_focus2_y'][1],self.settings['OT_focus3_y'][1],self.settings['OT_focus4_y'][1]]
        self.packed_settings['OT_color_point_x'] = [self.settings['OT_measure_point1_x'][1],self.settings['OT_measure_point2_x'][1],self.settings['OT_measure_point3_x'][1],self.settings['OT_measure_point4_x'][1]]
        self.packed_settings['OT_color_point_y'] = [self.settings['OT_measure_point1_y'][1],self.settings['OT_measure_point2_y'][1],self.settings['OT_measure_point3_y'][1],self.settings['OT_measure_point4_y'][1]]
        # convert that shit to radians
        self.packed_settings['OT_rotation'] = [float(self.settings['OT_rotation1'][1]) * math.pi / 180, float(self.settings['OT_rotation2'][1]) * math.pi / 180, float(self.settings['OT_rotation3'][1]) * math.pi / 180, float(self.settings['OT_rotation4'][1]) * math.pi / 180]
        self.packed_settings['OT_radius1'] = [self.settings['OT_radius1_1'][1],self.settings['OT_radius1_2'][1],self.settings['OT_radius1_3'][1],self.settings['OT_radius1_4'][1]]
        self.packed_settings['OT_radius2'] = [self.settings['OT_radius2_1'][1],self.settings['OT_radius2_2'][1],self.settings['OT_radius2_3'][1],self.settings['OT_radius2_4'][1]]
        self.packed_settings['OT_starting_width'] = [self.settings['OT_starting_width1'][1],self.settings['OT_starting_width2'][1],self.settings['OT_starting_width3'][1],self.settings['OT_starting_width4'][1]]
        self.packed_settings['OT_width_deflection'] = [self.settings['OT_width_deflection1'][1],self.settings['OT_width_deflection2'][1],self.settings['OT_width_deflection3'][1],self.settings['OT_width_deflection4'][1]]
        self.packed_settings['OT_loop_distance'] = [self.settings['OT_loop_distance1'][1],self.settings['OT_loop_distance2'][1],self.settings['OT_loop_distance3'][1],self.settings['OT_loop_distance4'][1]]
        self.packed_settings['OT_trap_count'] = [self.settings['OT_trap_count1'][1],self.settings['OT_trap_count2'][1],self.settings['OT_trap_count3'][1],self.settings['OT_trap_count4'][1]]
        return

    def compute(self):
        x_center = (self.settings['x_min'][1] + self.settings['x_max'][1]) / 2
        y_center = (self.settings['y_min'][1] + self.settings['y_max'][1]) / 2
        radians = self.settings['rotation'][1] * math.pi / 180

        self.package_settings()
        keep_coordinates, build_on_old_iterations = self.compare_previous_settings()

        if not keep_coordinates:
            print("\nComputing coordinates...")

            # create complex number matrix for each pixel in coordinate plane
            self.coordinate_matrix = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1]),dtype=np.complex_)

            for i in range(0,self.coordinate_matrix.shape[0]*self.coordinate_matrix.shape[1]):
                x_pix = i//self.coordinate_matrix.shape[0]
                x = i//self.coordinate_matrix.shape[0] / (self.settings['image_width'][1] - 1) * (self.settings['x_max'][1] - self.settings['x_min'][1]) + self.settings['x_min'][1]
                y_pix = i%self.coordinate_matrix.shape[0]
                y = i%self.coordinate_matrix.shape[0] / (self.settings['image_height'][1] - 1) * (self.settings['y_max'][1] - self.settings['y_min'][1]) + self.settings['y_min'][1]
                self.coordinate_matrix[i%self.coordinate_matrix.shape[0]][i//self.coordinate_matrix.shape[0]] = complex(x, y)

            # calculate distance from center of image for each pixel
            distance_from_center_matrix = self.coordinate_matrix
            distance_from_center_matrix.real = distance_from_center_matrix.real - x_center
            distance_from_center_matrix.imag = distance_from_center_matrix.imag - y_center
            distance_from_center_matrix = abs(distance_from_center_matrix)

            # matrix True where the pixel is on the lower Y half of the coordinate plane
            lower_half = self.coordinate_matrix.imag < 0

            #rotation is calculated here
            angle_matrix = np.arccos((self.coordinate_matrix.real) / distance_from_center_matrix)
            angle_matrix[lower_half] = math.pi - angle_matrix[lower_half]
            angle_matrix[np.isnan(angle_matrix)] = 0

            # adjust complex numbers according to rotation setting "radians"
            self.coordinate_matrix.real[lower_half] = -np.cos(angle_matrix[lower_half] + radians) * distance_from_center_matrix[lower_half] + x_center
            self.coordinate_matrix.imag[lower_half] = -np.sin(angle_matrix[lower_half] + radians) * distance_from_center_matrix[lower_half] + y_center
            self.coordinate_matrix.real[np.invert(lower_half)] = np.cos(angle_matrix[np.invert(lower_half)] + radians) * distance_from_center_matrix[np.invert(lower_half)] + x_center
            self.coordinate_matrix.imag[np.invert(lower_half)] = np.sin(angle_matrix[np.invert(lower_half)] + radians) * distance_from_center_matrix[np.invert(lower_half)] + y_center
            print("\nCoordinates have been computed.")

        if not build_on_old_iterations:

            # gather info about orbit traps that will be used
            self.orbit_trap_dict = {}
            for i in range(0,4):
                if self.settings['scheme_check'][1][i] == 1 and self.settings['scheme_dropdown'][1][i] in self.orbit_trap_list:
                    self.orbit_trap_dict[i] = int(self.settings['scheme_dropdown'][1][i])

            # tensor of pre-colorized RGB values from orbit traps (between 0 and 1)
            self.OT_RGBs = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],4))

            # tensor to keep track of trap count. height by width by number of orbit traps
            self.OT_trap_count = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],4))

            # dict of matrices to keep track of where orbits are trapped, to stop the pixel updating when appropriate
            self.previously_trapped = self.OT_trap_count != self.OT_trap_count

            # tensor to keep track of which orbit trap caught which points
            # structured to allow point trapped by multiple orbit traps
            self.OT_which_trap = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],4))

            # matrix to keep track of iterations before point escapes bailout radius
            # initialized to -1. Will be understood that -1's have not escaped
            self.main_escape_iterations = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1]))-1

            # tensor to keep track of iterations at which orbit traps succeed
            self.OT_escape_iterations = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],4))-1

            # matrix to store the distance of a point at the moment of escape
            self.escape_distance = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1]))-1

            # create function of the iterative equation
            exec("self.iterate_calc = lambda Z, C: " + self.settings['equation'][1])

            self.z_current = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1]),dtype=np.complex_)

            # freakin ITERATE
            self.nan_mask = self.z_current == self.z_current
            for iteration in range(0, int(self.settings['iterations'][1])):
                self.current_iteration = iteration
                if iteration == 0: print("\niteration: " + str(iteration + 1) + " / " + str(int(self.settings['iterations'][1])))
                else: self.mother.text_out.overwrite("iteration: " + str(iteration + 1) + " / " + str(int(self.settings['iterations'][1])))
                if self.settings['c_formula'][1] == 1:
                    self.z_current[self.nan_mask] = self.iterate_calc(self.z_current[self.nan_mask], self.coordinate_matrix[self.nan_mask])
                elif self.settings['c_formula'][1] == 2:
                    if iteration != 0: self.z_current[self.nan_mask] = self.iterate_calc(self.z_current[self.nan_mask], complex(self.settings['c_real'][1], self.settings['c_imag'][1]))
                    else:
                        self.z_current[self.nan_mask] = self.iterate_calc(self.z_current[self.nan_mask], self.coordinate_matrix[self.nan_mask])
                self.nan_mask = np.invert(np.isnan(self.z_current))
                if len(self.orbit_trap_dict) > 0: self.orbit_traps(self.z_current)
                self.main_escape_iterations[np.logical_and((abs(self.z_current) > self.settings['bailout_value'][1]), self.main_escape_iterations == -1)] = iteration
                self.escape_distance[np.logical_and((abs(self.z_current) > self.settings['bailout_value'][1]), self.escape_distance == -1)] = np.abs(self.z_current[np.logical_and((abs(self.z_current) > self.settings['bailout_value'][1]), self.escape_distance == -1)])
        else: # if build_on_old_iterations
            for iteration in range(self.previous_previous_iterations[1], int(self.settings['iterations'][1])):
                self.current_iteration = iteration
                if iteration == self.previous_previous_iterations[1]: print("\niteration: " + str(iteration + 1) + " / " + str(int(self.settings['iterations'][1])))
                else: self.mother.text_out.overwrite("iteration: " + str(iteration + 1) + " / " + str(int(self.settings['iterations'][1])))
                if self.settings['c_formula'][1] == 1:
                    self.z_current[self.nan_mask] = self.iterate_calc(self.z_current[self.nan_mask], self.coordinate_matrix[self.nan_mask])
                elif self.settings['c_formula'][1] == 2:
                    if iteration != 0: self.z_current[self.nan_mask] = self.iterate_calc(self.z_current[self.nan_mask], complex(self.settings['c_real'][1], self.settings['c_imag'][1]))
                    else:
                        self.z_current[self.nan_mask] = self.iterate_calc(self.z_current[self.nan_mask], self.coordinate_matrix[self.nan_mask])
                self.nan_mask = np.invert(np.isnan(self.z_current))
                if len(self.orbit_trap_dict) > 0: self.orbit_traps(self.z_current)
                self.main_escape_iterations[np.logical_and((abs(self.z_current) > self.settings['bailout_value'][1]), self.main_escape_iterations == -1)] = iteration
                self.escape_distance[np.logical_and((abs(self.z_current) > self.settings['bailout_value'][1]), self.escape_distance == -1)] = np.abs(self.z_current[np.logical_and((abs(self.z_current) > self.settings['bailout_value'][1]), self.escape_distance == -1)])

        #
        # self.main_escape_iterations = self.main_escape_iterations - 1
        # print("self.main_escape_iterations: " + str(self.main_escape_iterations))

        # get rid of the -1's in self.escape_distance
        # because these values will be used in logarithmic formulas
        one_time_escape_distance = np.array(self.escape_distance)
        one_time_escape_distance[one_time_escape_distance == -1] = 1

        # build matrix with all the normalized values to be converted to RGB
        self.normalized_RGB_1 = self.main_escape_iterations / self.settings['iterations'][1]
        # # continuous potential
        # self.normalized_RGB_2 = np.log(one_time_escape_distance)/2**self.main_escape_iterations
        # continuous iteration count
        self.normalized_RGB_2 = (self.main_escape_iterations + 1 - np.log(np.log(one_time_escape_distance))/math.log(2))/self.settings['iterations'][1]

        # colorize
        self.colorize()

        # send the RGB values into an image and save the image
        Image.fromarray(np.uint8(self.final_RGB_vals)).save(self.settings['image_name'][1])

        # load the image into the canvas
        self.mother.canvas_object.load_new_picture(self.settings['image_name'][1])

        print("\nElapsed time: ", self.seconds_to_time(time.clock()-self.t))
        return

    def orbit_traps(self, current_complex_matrix):
        for i in self.orbit_trap_dict.keys():
            if (self.orbit_trap_dict[i] == 2) or (self.orbit_trap_dict[i] == 3):
                self.OT_ellipse(current_complex_matrix, i)
            elif self.orbit_trap_dict[i] == 4:
                self.OT_line(current_complex_matrix, i)
            elif self.orbit_trap_dict[i] == 5:
                self.OT_cross(current_complex_matrix, i)
            # elif self.orbit_trap_dict[i] == 6: #OT_spiral

    def colorize(self):
        # create HxWx3x4 tensor to be filled with the RGB values
        # 3: one for each color channel
        # 4: one for each color method
        self.RGB_vals = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],3,4))-1

        # to keep track of where we have colors, so I don't have to grind my teeth indexing RGB_vals
        # this is a cheap way to get a False boolean array of size LxWx4... use an existing, non-sequitur array
        is_colored = self.OT_trap_count != self.OT_trap_count
        iteration_based_color_schemes=[]

        # RGB_vals to be filled here
        for i in range(0,4):
            if self.settings['scheme_check'][1][i] == 1:
                if self.settings['scheme_dropdown'][1][i] not in self.orbit_trap_list:
                    iteration_based_color_schemes.append(i)
                    if self.settings['scheme_dropdown'][1][i] == 1:
                        # iteration count w/ gradient here
                        if self.settings['color_scale_dropdown'][1][i] == 0:
                            self.RGB_vals[...,i][self.main_escape_iterations!=-1] = self.RGB_arbitrary_scale(self.settings['sequence_entry'][1][i], self.normalized_RGB_2)[self.main_escape_iterations!=-1]
                        elif self.settings['color_scale_dropdown'][1][i] == 1:
                            self.RGB_vals[...,i][self.main_escape_iterations!=-1] = self.color_hierarchy(self.settings['sequence_entry'][1][i], self.normalized_RGB_2)[self.main_escape_iterations!=-1]
                    else:
                        # iteration count
                        if self.settings['color_scale_dropdown'][1][i] == 0:
                            self.RGB_vals[...,i][self.main_escape_iterations!=-1] = self.RGB_arbitrary_scale(self.settings['sequence_entry'][1][i], self.normalized_RGB_1)[self.main_escape_iterations!=-1]
                        elif self.settings['color_scale_dropdown'][1][i] == 1:
                            self.RGB_vals[...,i][self.main_escape_iterations!=-1] = self.color_hierarchy(self.settings['sequence_entry'][1][i], self.normalized_RGB_1)[self.main_escape_iterations!=-1]
                else:
                    if self.settings['color_scale_dropdown'][1][i] == 0:
                        self.RGB_vals[...,i][self.OT_RGBs[...,i]!=-1] = self.RGB_arbitrary_scale(self.settings['sequence_entry'][1][i], self.OT_RGBs[...,i])[self.OT_RGBs[...,i]!=-1]
                    elif self.settings['color_scale_dropdown'][1][i] == 1:
                        self.RGB_vals[...,i][self.OT_RGBs[...,i]!=-1] = self.color_hierarchy(self.settings['sequence_entry'][1][i], self.OT_RGBs[...,i])[self.OT_RGBs[...,i]!=-1]
                is_colored[...,i][self.RGB_vals[...,0,i] != -1] = True
        # to get final RGB values, all in one place
        if not self.settings['black_background_check'][1]==1: self.final_RGB_vals = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],3))+255
        else: self.final_RGB_vals = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],3))

        # get rid of those -1's in self.main_escape_iterations and self.OT_escape_iterations
        self.main_escape_iterations[self.main_escape_iterations==-1]=self.settings['iterations'][1]+1
        self.OT_escape_iterations[self.OT_escape_iterations==-1]=self.settings['iterations'][1]+1

        lowest_finish_iteration = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1]))+self.settings['iterations'][1]+1
        for i in range(0,4):
            lowest_finish_iteration = np.minimum(lowest_finish_iteration, np.minimum(self.main_escape_iterations,self.OT_escape_iterations[...,i]))
        lowest_finish_iteration[lowest_finish_iteration==self.settings['iterations'][1]+1]=0

        winning_color_scheme = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1]))-1
        for i in range(3,-1,-1):
            if self.settings['scheme_check'][1][i] == 1:
                if self.settings['scheme_dropdown'][1][i] not in self.orbit_trap_list:
                    winning_color_scheme[lowest_finish_iteration==self.main_escape_iterations]=i
                else:
                    winning_color_scheme[lowest_finish_iteration==self.OT_escape_iterations[...,i]]=i
        for i in range(0,4): self.final_RGB_vals[winning_color_scheme==i]=self.RGB_vals[...,i][winning_color_scheme==i]

        return

    def shortest_distance(self, equation, points): #calculates the minimum distance between a point and a line
        if equation[0] == 0:
            return abs(equation[1] - points.imag), points.real, points.real * 0 + equation[1]
        multiplicative_inverse = -1 / equation[0]

        # been some time since I wrote this, but I think perp_equation is
        # to the center line of the second arm of the trap, for each point
        perp_equation = (multiplicative_inverse, points.imag - multiplicative_inverse * points.real)
        intersection_point_x = (perp_equation[1] - equation[1]) / (equation[0] - perp_equation[0])
        intersection_point_y = intersection_point_x * equation[0] + equation[1]

        # returns the distance, and x and y coordinates of the intersection point, for each pixel
        return self.pythagoras(points.real - intersection_point_x, points.imag - intersection_point_y), intersection_point_x, intersection_point_y

    def seconds_to_time(self, seconds_in):
        try:
            seconds_in = float(seconds_in)
        except:
            print("Type error: non-number passed to the seconds_to_time function.")
            return
        if seconds_in > 3600:
            hours = int(seconds_in // 3600)
            minutes = int(seconds_in % 3600/60)
            seconds = format((seconds_in % 60), '.2f')
            result = str(hours) + "h " + str(minutes)+ "m "+ seconds + "s"
        elif seconds_in > 60:
            minutes = int(seconds_in // 60)
            seconds = format(seconds_in % 60, '.2f')
            result = str(minutes) + "m " + seconds + "s"
        else:
            seconds =  format(seconds_in, '.2f')
            result = seconds + "s"
        return result

    def pythagoras(self, a, b):
        if type(a) == np.ndarray or type(b) == np.ndarray:
            return np.power(np.power(a, 2) + np.power(b, 2), .5)
        return math.pow(math.pow(a, 2) + math.pow(b, 2), .5)

    def OT_ellipse(self, z_current, which_scheme):
        A = z_current.real
        B = z_current.imag
        # focus = self.packed_settings['OT_focus'][1][which_scheme].split(",")
        focus = (self.packed_settings['OT_focus_x'][which_scheme], self.packed_settings['OT_focus_y'][which_scheme])
        X = float(focus[0])
        Y = float(focus[1])
        XR = self.packed_settings['OT_radius1'][which_scheme]
        if self.settings['scheme_dropdown'][1][which_scheme] == 2: YR = XR
        else: YR = self.packed_settings['OT_radius2'][which_scheme]
        rotation = self.packed_settings['OT_rotation'][which_scheme]
        x_component = np.power((((A - X) * np.cos(rotation) - (B - Y) * np.sin(rotation)) / XR), 2)
        y_component = np.power((((A - X) * np.sin(rotation) - (B - Y) * np.cos(rotation)) / YR), 2)

        # check if point falls within orbit trap
        in_trap = x_component + y_component <= 1

        # where point falls within orbit trap, increment the trap count
        self.OT_trap_count[...,which_scheme][in_trap] = self.OT_trap_count[...,which_scheme][in_trap] + 1

        # where trap threshold met, show true
        threshold_met = self.OT_trap_count[...,which_scheme] == self.packed_settings['OT_trap_count'][which_scheme]

        # where trap count threshold newly reached, set normalized RGB value (between 0 and 1)
        self.OT_RGBs[...,which_scheme][np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))] = (self.pythagoras(A - X, B - Y) % self.packed_settings['OT_loop_distance'][which_scheme])[np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))]

        # where trap count threshold newly reached, record the current iteration count
        self.OT_escape_iterations[...,which_scheme][np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))]=self.current_iteration

        # show which color scheme trapped the pixel
        self.OT_which_trap[np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))] = which_scheme

        # turn to true where trap requirements met and RGB value is set
        self.previously_trapped[...,which_scheme] += threshold_met

        return

    def OT_cross(self, z_current, which_scheme):

        slope = math.tan(self.packed_settings['OT_rotation'][which_scheme] % 2*math.pi)
        if slope != 0: perpendicular_slope = -1/slope
        else: perpendicular_slope = 9999999
        focus = [self.packed_settings['OT_focus_x'][which_scheme], self.packed_settings['OT_focus_y'][which_scheme]]
        for i,j in enumerate(focus): focus[i]=float(j) #cast the entries as floats
        equation = (slope, focus[1] - slope * focus[0] )
        perpendicular_equation = (perpendicular_slope, focus[1] - perpendicular_slope * focus[0])

        # line 2 is perpendicular to line 1, for the second arm of the "cross"
        dist_to_line1 = self.shortest_distance(equation, z_current)
        dist_to_line2 = self.shortest_distance(perpendicular_equation, z_current)

        # trickery = np.array(z_current)
        # trickery.real = z_current.imag
        # trickery.imag = z_current.real
        # dist_to_line2 = self.shortest_distance(equation, trickery)

        starting_width = self.packed_settings['OT_starting_width'][which_scheme]
        width_deflection = self.packed_settings['OT_width_deflection'][which_scheme]

        # check if points fall within orbit trap
        in_trap = np.logical_or(dist_to_line1[0] <= starting_width / 2 + width_deflection * self.pythagoras(dist_to_line1[1] - focus[0], dist_to_line1[2] - focus[1]),
                                        dist_to_line2[0] <= starting_width / 2 + width_deflection * self.pythagoras(dist_to_line2[1] - focus[0], dist_to_line2[2] - focus[1]))

        # where points fall within orbit trap, increment the trap count
        self.OT_trap_count[...,which_scheme][in_trap] = self.OT_trap_count[...,which_scheme][in_trap] + 1

        # create mask for where the threshold is met
        threshold_met = self.OT_trap_count[...,which_scheme] == self.packed_settings['OT_trap_count'][which_scheme]

        color_loop_dist = self.packed_settings['OT_loop_distance'][which_scheme]

        # where trap count threshold newly reached, set normalized RGB value (between 0 and 1)
        self.OT_RGBs[...,which_scheme][np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))] = ((self.pythagoras(z_current.real - focus[0], z_current.imag - focus[1]) % color_loop_dist) / color_loop_dist)[np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))]

        # where trap count threshold newly reached, record the current iteration count
        self.OT_escape_iterations[...,which_scheme][np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))]=self.current_iteration

        # show which color scheme trapped the pixel
        self.OT_which_trap[np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))] = which_scheme

        # turn to true where trap requirements met and RGB value is set
        self.previously_trapped[...,which_scheme] += threshold_met

        return

    def OT_spiral(self, focus, rotation, starting_width, width_deflection):
        dist_point_from_focus = pythagoras(point[0] - focus[0], point[1] - focus[1])
        angle = asin((point[1] - focus[1]) / dist_point_from_focus)
        #calculate bounds of perspective in coordinate grid
        #analyze portions accordingly
        #find local minima
        #8-10 repetitions of dividing range by 2, determining if should be lower or higher
        #infer global minimum by finding smallest one before they start increasing again
        #thus determine distance from spiral orbit trap, and compute color accordingly

        def length(a, t): #calculates length of spiral r = a^t from its start, given a(arbitrary coefficient), and t(theta; the angle)
            term1 = math.log(a)**2
            term2 = a**t*math.log(a)*math.cos(t)
            term3 = -a**t*math.sin(t)
            term4 = a**t*math.cos(t)
            term5 = a**t*math.log(a)*math.sin(t)
            term6 = math.log(a)**3
            term7 = math.log(a)
            upper_bound = (term1 + 1) * ((term2 + term3)**2 + (term4 + term5)**2)**.5 / (term6 + term7)
            t = 0
            term1 = math.log(a)**2
            term2 = a**t*math.log(a)*math.cos(t)
            term3 = -a**t*math.sin(t)
            term4 = a**t*math.cos(t)
            term5 = a**t*math.log(a)*math.sin(t)
            term6 = math.log(a)**3
            term7 = math.log(a)
            lower_bound = (term1 + 1) * ((term2 + term3)**2 + (term4 + term5)**2)**.5 / (term6 + term7)
            return upper_bound - lower_bound

    def OT_line(self, z_current, which_scheme):

        slope = math.tan(self.packed_settings['OT_rotation'][which_scheme] % math.pi/2)
        focus = [self.packed_settings['OT_focus_x'][which_scheme], self.packed_settings['OT_focus_y'][which_scheme]]
        for i,j in enumerate(focus): focus[i]=float(j) #cast the entries as floats
        equation = (slope, focus[1] - slope * focus[0])

        # QC the "trickery". Convince yourself it's correct.
        # line 2 is perpendicular to line 1, for the second arm of the "cross"
        dist_to_line = self.shortest_distance(equation, z_current)

        starting_width = self.packed_settings['OT_starting_width'][which_scheme]
        width_deflection = self.packed_settings['OT_width_deflection'][which_scheme]

        # check if points fall within orbit trap
        in_trap = dist_to_line[0] <= starting_width / 2 + width_deflection * self.pythagoras(dist_to_line[1] - focus[0], dist_to_line[2] - focus[1])

        # where points fall within orbit trap, increment the trap count
        self.OT_trap_count[...,which_scheme][in_trap] = self.OT_trap_count[...,which_scheme][in_trap] + 1

        # create mask for where the threshold is met
        threshold_met = self.OT_trap_count[...,which_scheme] == self.packed_settings['OT_trap_count'][which_scheme]

        color_loop_dist = self.packed_settings['OT_loop_distance'][which_scheme]

        # where trap count threshold newly reached, set normalized RGB value (between 0 and 1)
        self.OT_RGBs[...,which_scheme][np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))] = ((self.pythagoras(z_current.real - focus[0], z_current.imag - focus[1]) % color_loop_dist) / color_loop_dist)[np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))]

        # where trap count threshold newly reached, record the current iteration count
        self.OT_escape_iterations[...,which_scheme][np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))]=self.current_iteration

        # show which color scheme trapped the pixel
        self.OT_which_trap[np.logical_and(threshold_met, np.invert(self.previously_trapped[...,which_scheme]))] = which_scheme

        # turn to true where trap requirements met and RGB value is set
        self.previously_trapped[...,which_scheme] += threshold_met

        return

    def color_hierarchy(self, order, RGB):

        # bool matrix for where the pixels did not escape
        no_RGB = RGB < 0

        RGB_matrix = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],3))
        if len(order) == 3:
            RGB = RGB * 256**3
            parent = RGB // (256*256)
            child = (RGB / 256) % 256
            grandchild = RGB % 256
        elif len(order) == 2:
            RGB = RGB * 256 ** 2
            parent = RGB // 256
            child = RGB % 256
            grandchild = 0
        else:
            RGB = RGB * 256
            parent = RGB
            child = 0
            grandchild = 0
        counter = 0
        set = (parent, child, grandchild)
        try:
            RGB_matrix[:,:,0]=set[order.index('R')]
        except:
            red = 0
        try:
            RGB_matrix[:,:,1]=set[order.index('G')]
        except:
            green = 0
        try:
            RGB_matrix[:,:,2]=set[order.index('B')]
        except:
            blue = 0
        RGB_matrix[no_RGB] = (0,0,0)
        return RGB_matrix

    def RGB_arbitrary_scale(self, color_string, RGB_array):
        color_table = {}
        color_table[0] = ('BLACK',(0,0,0))
        color_table[1] = ('WHITE',(255,255,255))
        color_table[2] = ('RED',(255,0,0))
        color_table[3] = ('LIME',(0,255,0))
        color_table[4] = ('BLUE',(0,0,255))
        color_table[5] = ('YELLOW',(255,255,0))
        color_table[6] = ('AQUA',(0,255,255))
        color_table[7] = ('FUCHSIA',(255,0,255))
        color_table[8] = ('SILVER',(192,192,192))
        color_table[9] = ('GRAY',(128,128,128))
        color_table[10] = ('MAROON',(128,0,0))   #A
        color_table[11] = ('OLIVE',(128,128,0))  #B
        color_table[12] = ('GREEN',(0,128,0))    #C
        color_table[13] = ('PURPLE',(128,0,128)) #D
        color_table[14] = ('TEAL',(0,128,128))   #E
        color_table[15] = ('NAVY',(0,0,128))     #F

        # convert color_string, which is received from GUI, which is why it is a string,
        # into a list of ints to use for referencing the color dictionary.
        # Using an array of strings seemed unweildy in numpy.
        color_sequence = []
        for c in color_string:
            if c == 'A': color_sequence.append(10)
            elif c == 'B': color_sequence.append(11)
            elif c == 'C': color_sequence.append(12)
            elif c == 'D': color_sequence.append(13)
            elif c == 'E': color_sequence.append(14)
            elif c == 'F': color_sequence.append(15)
            else: color_sequence.append(int(c))
        num_spectrums = len(color_string) - 1

        #create bool array with true values at pixels which escaped
        pixel_escaped = RGB_array >= 0

        #create an array of integers representing which color spectrum to use per pixel
        which_spectrum = (RGB_array // (1 / (num_spectrums))).astype(np.int, copy=False)

        # renormalize the RGB values based on how far along they are in their individual spectrums
        # triplicate each value, to have one for each color channel
        renormalized_RGB_array = np.repeat(((RGB_array % (1 / (num_spectrums))) * num_spectrums), 3).reshape(self.settings['image_height'][1],self.settings['image_width'][1],3)

        #find start and end RGB values at each pixel for the appropriate color spectrum
        #could use one 4d tensor for this... oh well, used 2-3d's instead
        color_start = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],3))
        color_end = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],3))
        for spectrum_index in range(num_spectrums):
            color_start[which_spectrum == spectrum_index] = color_table[color_sequence[spectrum_index]][1]
            color_end[which_spectrum == spectrum_index] = color_table[color_sequence[spectrum_index+1]][1]

        # create 3d matrix containing the RGB range of the pertinent spectrum at each R, G and B value
        color_range = color_end - color_start

        # do some arithmetic to get RGB values
        the_answer = renormalized_RGB_array * color_range + color_start

        return the_answer

    def save_to_log(self, time):
        if not os.path.isfile(os.getcwd().replace('\\','/') + "/log.csv"):
            f = open(os.getcwd().replace('\\','/') + "/log.csv","w")
            line = 'X Min,X Max,Y Min,Y Max,Image Width,Image Height,Iterations,Time\n'
            f.write(line)
        else:
            f = open(os.getcwd().replace('\\','/') + "/log.csv","a")
        line = str(self.settings['x_min'][1]) + ", " + str(self.settings['x_max'][1]) + ", " + str(self.settings['y_min'][1]) + ", " + str(self.settings['y_max'][1]) + ", " + str(self.settings['image_width'][1]) + ", " + str(self.settings['image_height'][1]) + ", " + str(self.settings['iterations'][1]) + ", " + str(time) + '\n'
        f.write(line)
        f.close()
        return

    def save_settings(self, manual=False):
        if manual: f = open(self.settings['save_filename'][1], 'w')
        else:
            if os.path.isfile(os.getcwd().replace('\\','/') + "/recent_settings.txt"):
                os.replace("recent_settings.txt", "recent_settings_old.txt")
            f = open(os.getcwd().replace('\\','/') + '/recent_settings.txt', 'w')
        f.write('{')
        for index, key in enumerate(self.settings.keys()):
            if index == len(self.settings)-1: line = "'" + key + "':" + str(self.settings[key]) + "\n" #if statement to make sure a comma doesn't get placed on the last line
            else: line = "'" + key + "':" + str(self.settings[key]) + ",\n"
            f.write(line)
        f.write('}')
        f.close()
        if manual: print("\n!!!!! Settings Have Been Saved !!!!!")
        else: print("\n!!!!! Settings Have Been Backed Up !!!!!")
        return

    def settings_import_from_file(self, filename):
        import ast
        f = open(filename)
        the_string = f.read()
        f.close()
        self.settings = ast.literal_eval(the_string)
        for key in self.settings.keys():
            if self.settings[key][0] == 'list':
                self.settings[key][1] = tuple(self.settings[key][1])
        return

class the_canvas:
    def __init__(self, mother, parent_frame):
        self.mother = mother
        self.x = self.y = 0
        self.rect_start_x = self.rect_start_y = -2
        self.rect_end_x = self.rect_end_y = 2
        self.parent_frame = parent_frame
        self.make_canvas()
        self.load_new_picture("Fractal.png")
        self.rect = self.the_canvas.create_rectangle(self.image_start_x, self.image_start_y, self.image_start_x + self.resize_image_size[0], self.image_start_y + self.resize_image_size[1], dash=(3,2), width=2, outline="gray")
    def make_canvas(self):
        self.the_canvas_maximum_width = 1064
        self.the_canvas_maximum_height = 955
        self.the_canvas_max_dimensions = (self.the_canvas_maximum_width, self.the_canvas_maximum_height)
        self.the_canvas = Canvas(self.parent_frame, cursor="cross")
        self.the_canvas.config(width=self.the_canvas_maximum_width, height=self.the_canvas_maximum_height)
        background = Image.open(os.getcwd().replace('\\','/') + "/Code/Checkerboard.png")
        background = ImageTk.PhotoImage(background)
        self.img = background
        self.the_canvas.create_image((0,0), anchor=NW, image=background)
        self.the_canvas.pack(side="top", fill="both", expand=True)
        self.the_canvas.bind("<ButtonPress-1>", self.on_primary_button_press)
        self.the_canvas.bind("<B1-Motion>", self.on_primary_button_drag)
        self.the_canvas.bind("<ButtonRelease-1>", self.on_primary_button_release)
        self.the_canvas.bind("<ButtonPress-3>", self.on_secondary_button_press)
        self.the_canvas.bind("<B3-Motion>", self.on_secondary_button_drag)
        self.the_canvas.bind("<ButtonRelease-3>", self.on_secondary_button_release)
    def load_new_picture(self, picture_path):
        try: self.last_angle = self.mother.fractal_object.settings['rotation'][1]
        except: self.last_angle = 0
        if not os.path.isfile(os.getcwd().replace('\\','/') + "/Fractal.png"):
            new_pic_array = np.zeros(shape=(10,10,3))
            Image.fromarray(np.uint8(new_pic_array)).save(os.getcwd().replace('\\','/') + "/Fractal.png")
        the_picture = Image.open(picture_path) #open base image
        self.resize_image_size = self.display_resize_calc(self.the_canvas_max_dimensions, the_picture.size) #find new image size based on calculation
        the_picture = the_picture.resize(self.resize_image_size, Image.ANTIALIAS)#resize image according to new size
        the_picture.save(os.getcwd().replace('\\','/') + "/temp/Temp.png")#save the resized image
        the_picture = Image.open(os.getcwd().replace('\\','/') + "/temp/Temp.png")#load the resized image into the_picture variable
        background = Image.open(os.getcwd().replace('\\','/') + "/Code/Checkerboard.png")
        self.image_start_x = int((self.the_canvas_maximum_width-self.resize_image_size[0])/2)
        self.image_start_y = int((self.the_canvas_maximum_height-self.resize_image_size[1])/2)
        background.paste(the_picture, (self.image_start_x, self.image_start_y)) #paste resized image into middle of canvas
        self.img = ImageTk.PhotoImage(background)
        self.the_canvas.create_image((0,0), anchor=NW, image=self.img)#create the image in the canvas
        self.the_canvas.pack()#pack the canvas into the frame
        os.remove(os.getcwd().replace('\\','/') + "/temp/Temp.png")
        return
    def display_resize_calc(self, frame_size, image_size):
        if (image_size[0] != frame_size[0]) or (image_size[1] != frame_size[1]):
            if (image_size[0] > frame_size[0]) or (image_size[1] > frame_size[1]):
                if image_size[0]/image_size[1] > frame_size[0]/frame_size[1]:
                    the_resized_size=(int(frame_size[0]),int(frame_size[0]*image_size[1]/image_size[0]))
                else:
                    the_resized_size=(int(frame_size[1]*image_size[0]/image_size[1]),int(frame_size[1]))
            else:
                if image_size[0]/image_size[1] < frame_size[0]/frame_size[1]:
                    the_resized_size=(int(frame_size[1]*image_size[0]/image_size[1]),int(frame_size[1]))
                else:
                    the_resized_size=(int(frame_size[0]),int(frame_size[0]*image_size[1]/image_size[0]))
        else: the_resized_size = image_size
        return the_resized_size
    def on_primary_button_press(self, event):
        self.the_canvas.create_image(0,0,anchor="nw",image=self.img)
        self.rect_start_x = event.x
        self.rect_start_y = event.y
        self.rect = self.the_canvas.create_rectangle(self.x, self.y, 1, 1, dash=(3,2), width=2, outline="gray")
    def on_primary_button_drag(self, event):
        current_x, current_y = (event.x, event.y)
        if self.proportion_rectangle_check.get() == 1: #if proportion setting is on
            if abs(current_y - self.rect_start_y) >= abs(current_x - self.rect_start_x): #if the magnitude of y is greater than the magnitude of x
                if current_y >= self.rect_start_y: #cursor moved down
                    if self.rect_start_x >= current_x: #cursor moved left
                        self.the_canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, self.rect_start_x - (current_y - self.rect_start_y), current_y)
                    else: #cursor moved right
                        self.the_canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, self.rect_start_x + current_y - self.rect_start_y, current_y)
                else: #cursor moved up
                    if self.rect_start_x >= current_x: #cursor moved left
                        self.the_canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, self.rect_start_x + current_y - self.rect_start_y, current_y)
                    else: #cursor moved right
                        self.the_canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, self.rect_start_x - (current_y - self.rect_start_y), current_y)
            else: #the magnitude of x is greater the magnitude of y
                if current_x >= self.rect_start_x: #cursor moved right
                    if self.rect_start_y >= current_y: #cursor moved up
                        self.the_canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, current_x, self.rect_start_y - (current_x - self.rect_start_x))
                    else: #cursor moved down
                        self.the_canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, current_x, self.rect_start_y + current_x - self.rect_start_x)
                else: #cursor moved left
                    if self.rect_start_y >= current_y: #cursor moved up
                        self.the_canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, current_x, self.rect_start_y + current_x - self.rect_start_x)
                    else: #cursor moved down
                        self.the_canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, current_x, self.rect_start_y - (current_x - self.rect_start_x))
        else: self.the_canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, current_x, current_y)
    def on_primary_button_release(self, event):
        current_x, current_y = (event.x, event.y)
        if self.proportion_rectangle_check.get() == 1: #if proportion setting is on
            if abs(current_y - self.rect_start_y) >= abs(current_x - self.rect_start_x): #if the magnitude of y is greater than the magnitude of x
                if current_y >= self.rect_start_y: #cursor moved down
                    if self.rect_start_x >= current_x: #cursor moved left
                        self.rect_end_x = self.rect_start_x - (current_y - self.rect_start_y)
                        self.rect_end_y = current_y
                    else: #cursor moved right
                        self.rect_end_x = self.rect_start_x + current_y - self.rect_start_y
                        self.rect_end_y = current_y
                else: #cursor moved up
                    if self.rect_start_x >= current_x: #cursor moved left
                        self.rect_end_x = self.rect_start_x + current_y - self.rect_start_y
                        self.rect_end_y = current_y
                    else: #cursor moved right
                        self.rect_end_x = self.rect_start_x - (current_y - self.rect_start_y)
                        self.rect_end_y = current_y
            else: #the magnitude of x is greater the magnitude of y
                if current_x >= self.rect_start_x: #cursor moved right
                    if self.rect_start_y >= current_y: #cursor moved up
                        self.rect_end_x = current_x
                        self.rect_end_y = self.rect_start_y - (current_x - self.rect_start_x)
                    else: #cursor moved down
                        self.rect_end_x = current_x
                        self.rect_end_y = self.rect_start_y + current_x - self.rect_start_x
                else: #cursor moved left
                    if self.rect_start_y >= current_y: #cursor moved up
                        self.rect_end_x = current_x
                        self.rect_end_y = self.rect_start_y + current_x - self.rect_start_x
                    else: #cursor moved down
                        self.rect_end_x = current_x
                        self.rect_end_y = self.rect_start_y - (current_x - self.rect_start_x)
        else: self.the_canvas.coords(self.rect, self.rect_start_x, self.rect_start_y, current_x, current_y)
    def on_secondary_button_press(self, event):
        self.drag_x = self.start_drag_x = event.x
        self.drag_y = self.start_drag_y = event.y
    def on_secondary_button_drag(self, event):
        self.the_canvas.move(self.rect, event.x - self.drag_x, event.y - self.drag_y)
        self.drag_x = event.x
        self.drag_y = event.y
    def on_secondary_button_release(self, event):
        delta_x = event.x - self.start_drag_x
        delta_y = event.y - self.start_drag_y
        self.rect_start_x += delta_x
        self.rect_start_y += delta_y
        self.rect_end_x += delta_x
        self.rect_end_y += delta_y
        pass

class window1:
    def __init__(self, mother):
        self.mother = mother
        self.pythagoras = lambda a, b: (a**2 + b**2)**.5

        self.master = Tk()

        self.master.wm_title("Fractal Explorer")

        self.master.minsize(width=1908, height=960)
        self.master.maxsize(width=1908, height=960)

        self.fractal_settings_frame = ttk.Frame(self.master)
        self.fractal_settings_frame.grid(row=0, column=0, sticky="EW")
        ttk.Separator(self.fractal_settings_frame, orient=HORIZONTAL).grid(row=0, columnspan=4, sticky="ew")
        Label(self.fractal_settings_frame, text="Fractal Settings").grid(row=0, column=1)

        Label(self.fractal_settings_frame, text="X Minimum: ").grid(row=1)
        self.x_min = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.x_min.insert(END, '-2')
        self.x_min.grid(row=1, column=1)
        Label(self.fractal_settings_frame, text="X Maximum: ").grid(row=2)
        self.x_max = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.x_max.insert(END, '2')
        self.x_max.grid(row=2, column=1)
        Label(self.fractal_settings_frame, text="Y Minimum: ").grid(row=3)
        self.y_min = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.y_min.insert(END, '-2')
        self.y_min.grid(row=3, column=1)
        Label(self.fractal_settings_frame, text="Y Maximum: ").grid(row=4)
        self.y_max = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.y_max.insert(END, '2')
        self.y_max.grid(row=4, column=1)
        Label(self.fractal_settings_frame, text="Iterations: ").grid(row=5)
        self.iterations = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.iterations.insert(END, '42')
        self.iterations.grid(row=5, column=1)
        #
        def zoom_from_rectangle():
            debug = False
            #find center point of user rectangle in the rotated coordinate plane
            #fill minimums and maximums with same dimensions as user rectangle about said center point
            #----------------------
            #find rectangle centerpoint in pixels
            rectangle_centerpoint_x_in_pixels = (self.mother.canvas_object.rect_start_x + self.mother.canvas_object.rect_end_x) / 2 - self.mother.canvas_object.image_start_x
            rectangle_centerpoint_y_in_pixels = (self.mother.canvas_object.rect_start_y + self.mother.canvas_object.rect_end_y) / 2 - self.mother.canvas_object.image_start_y
            if debug: print("\nrect centerpoint (pixels): " + str(rectangle_centerpoint_x_in_pixels) + ", " + str(rectangle_centerpoint_y_in_pixels))
            #----------------------
            #find size, in pixels, of the rectangle
            rect_x_width = abs(self.mother.canvas_object.rect_end_x - self.mother.canvas_object.rect_start_x)
            rect_y_width = abs(self.mother.canvas_object.rect_end_y - self.mother.canvas_object.rect_start_y)
            if debug: print("rect dimensions: " + str(rect_x_width) + " x " + str(rect_y_width))
            #----------------------
            #find center of image in fractal coordinate plane
            image_center_x = (mother.fractal_object.settings['x_min'][1] + mother.fractal_object.settings['x_max'][1]) / 2
            image_center_y = (mother.fractal_object.settings['y_min'][1] + mother.fractal_object.settings['y_max'][1]) / 2
            if debug: print("image center in coordinate plane: " + str(image_center_x) + ", " + str(image_center_y))
            #----------------------
            #find original image size in fractal coordinate plane
            original_x_coordinate_width = mother.fractal_object.settings['x_max'][1] - mother.fractal_object.settings['x_min'][1]
            original_y_coordinate_width = mother.fractal_object.settings['y_max'][1] - mother.fractal_object.settings['y_min'][1]
            if debug: print("original coordinate width, height: " + str(original_x_coordinate_width) + " x " + str(original_y_coordinate_width))
            #----------------------
            #find tentative rectangle coordinate widths by proportion
            tentative_rect_x_coordinate_width = original_x_coordinate_width * rect_x_width / self.mother.canvas_object.resize_image_size[0]
            tentative_rect_y_coordinate_width = original_y_coordinate_width * rect_y_width / self.mother.canvas_object.resize_image_size[1]
            if debug: print("tentative rect coord widths: " + str(tentative_rect_x_coordinate_width) + ", " + str(tentative_rect_y_coordinate_width))
            #----------------------
            #find centerpoint of rectangle in fractal coordinates, before accounting for rotation
            tentative_rectangle_centerpoint_x = mother.fractal_object.settings['x_min'][1] + (original_x_coordinate_width * rectangle_centerpoint_x_in_pixels / self.mother.canvas_object.resize_image_size[0])
            tentative_rectangle_centerpoint_y = mother.fractal_object.settings['y_min'][1] + (original_y_coordinate_width * rectangle_centerpoint_y_in_pixels / self.mother.canvas_object.resize_image_size[1])
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
            scalar_rectangle_centerpoint_x = mother.fractal_object.settings['x_min'][1] + (rect_distance_scalar * rectangle_centerpoint_x_in_pixels / self.mother.canvas_object.resize_image_size[0])
            scalar_rectangle_centerpoint_y = mother.fractal_object.settings['y_min'][1] + (rect_distance_scalar * rectangle_centerpoint_y_in_pixels / self.mother.canvas_object.resize_image_size[1])
            denominator = self.pythagoras(original_x_coordinate_width / 2, original_y_coordinate_width / 2)
            adjusted_rectangle_centerpoint_x = (original_x_coordinate_width / 2) / scalar_rectangle_centerpoint_x * denominator
            adjusted_rectangle_centerpoint_y = (original_y_coordinate_width / 2) / scalar_rectangle_centerpoint_y * denominator
            if debug: print("new dist center rect from center image: " + str(center_rect_distance_from_center_image))
            if debug: print("adjusted rect center point: " + str(adjusted_rectangle_centerpoint_x) + ", " + str(adjusted_rectangle_centerpoint_y))
            #----------------------
            #get angle of image
            mother.fractal_object.settings['rotation'] = ['float', float(self.rotation.get())]
            image_angle_in_radians = mother.fractal_object.settings['rotation'][1] * math.pi / 180
            if debug: print("image angle: " + str(image_angle_in_radians))
            #----------------------
            #find the center of the rectangle in fractal coord plane adjusting for rotation of image
            x_coordinate_add = center_rect_distance_from_center_image * math.cos(image_angle_in_radians + angle_to_rectangle_in_image)
            y_coordinate_add = center_rect_distance_from_center_image * math.sin(image_angle_in_radians + angle_to_rectangle_in_image)
            x_coordinate_final = image_center_x + x_coordinate_add
            y_coordinate_final = image_center_y + y_coordinate_add
            if debug: print("rect centerpoint final: " + str(x_coordinate_final) + ", " + str(y_coordinate_final))
            #----------------------
            #calculate final coordinate widths??
            #----------------------
            #calculate new coordinate bounds with new coordinate widths and new coordinate centerpoint
            new_min_x = x_coordinate_final - tentative_rect_x_coordinate_width / 2
            new_max_x = x_coordinate_final + tentative_rect_x_coordinate_width / 2
            new_min_y = y_coordinate_final - tentative_rect_y_coordinate_width / 2
            new_max_y = y_coordinate_final + tentative_rect_y_coordinate_width / 2
            #finally, replace GUI coord bounds with newly calc'd coord bounds based on rectangle
            self.x_min.delete(0, END)
            self.x_min.insert(END, str(new_min_x))
            self.x_max.delete(0, END)
            self.x_max.insert(END, str(new_max_x))
            self.y_min.delete(0, END)
            self.y_min.insert(END, str(new_min_y))
            self.y_max.delete(0, END)
            self.y_max.insert(END, str(new_max_y))
            print("\n!!!!! Coordinates Updated !!!!!")
            return
        Button(self.fractal_settings_frame, text='Get Rectangle', command=zoom_from_rectangle).grid(row=5, column=2)
        #
        Label(self.fractal_settings_frame, text="Image Width: ").grid(row=1, column=2)
        self.image_width = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.image_width.insert(END, '955')
        self.image_width.grid(row=1, column=3)
        Label(self.fractal_settings_frame, text="Image Height: ").grid(row=2, column=2)
        self.image_height = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.image_height.insert(END, '955')
        self.image_height.grid(row=2, column=3)
        Label(self.fractal_settings_frame, text="Rotation: ").grid(row=3, column=2)
        self.rotation = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.rotation.insert(END, '270')
        self.rotation.grid(row=3, column=3)
        Label(self.fractal_settings_frame, text="Bailout Value: ").grid(row=4, column=2)
        self.bailout_value = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.bailout_value.insert(END, '2')
        self.bailout_value.grid(row=4, column=3)
        #
        def coordinate_C():
            self.c_formula.set(1)
            self.c_real.delete(0, END)
            self.c_real.insert(END, '.5')
            self.c_real.config(state = DISABLED)
            self.c_imag.delete(0, END)
            self.c_imag.insert(END, '.5')
            self.c_imag.config(state = DISABLED)
            return
        def arbitrary_C():
            self.c_formula.set(2)
            self.c_real.config(state = NORMAL)
            self.c_imag.config(state = NORMAL)
            return
        self.c_formula_frame = ttk.Frame(self.fractal_settings_frame)
        self.c_formula_frame.grid(row=7,column=0,columnspan=4)
        self.c_formula = IntVar()
        self.c_formula.set(1)
        self.a_bi = Radiobutton(self.c_formula_frame, text="C = A + Bi", variable=self.c_formula, value=2, command=arbitrary_C)
        self.a_bi.grid(row=0, column=0, ipadx=50)
        self.x_yi = Radiobutton(self.c_formula_frame, text="C = X + Yi", variable=self.c_formula, value=1, command=coordinate_C)
        self.x_yi.grid(column=1, row=0, ipadx=50)
        Label(self.fractal_settings_frame, text="C Real (A): ").grid(row=8)
        self.c_real = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.c_real.insert(END, '.5')
        self.c_real.config(state = DISABLED)
        self.c_real.grid(row=8, column=1)
        Label(self.fractal_settings_frame, text="C Imaginary (B): ").grid(row=8, column=2)
        self.c_imag = Entry(self.fractal_settings_frame, justify = RIGHT)
        self.c_imag.insert(END, '.5')
        self.c_imag.config(state = DISABLED)
        self.c_imag.grid(row=8, column=3)
        # Label(self.fractal_settings_frame, text="Thread Count: ").grid(row=9)
        # self.thread_count = Entry(self.fractal_settings_frame, justify = RIGHT)
        # self.thread_count.insert(END, '3')
        # self.thread_count.grid(row=9, column=1)
        def verify_string(input_string):
            if input_string.count('(') != input_string.count(')'):
                if debug: print("Number of begin parenthesis does not match number of end parenthesis.")
                print("\n!!!!! Equation Check Failed !!!!!")
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
                            print("\n!!!!! Equation Check Failed !!!!!")
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
                            print("\n!!!!! Equation Check Failed !!!!!")
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
                                        print("\n!!!!! Equation Check Failed !!!!!")
                                        return False
                                    else: break
                                else: subcount -= 1
                            count += 1
                            if string[count] not in list_of_numbers:
                                print("\n!!!!! Equation Check Failed !!!!!")
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
                        print("\n!!!!! Equation Check Failed !!!!!")
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
                        print("\n!!!!! Equation Check Failed !!!!!")
                        return False
                    if (next_must_be_begin_parenthesis or (character in list_basic_operators)) and count >= len(string):
                        if super_debug: print("check 11")
                        if debug: print("Incomplete or erroneous expression at end of string!")
                        print("\n!!!!! Equation Check Failed !!!!!")
                        return False
                print("\n!!!!! Equation Seems Valid !!!!!")
                return True
            return string_walk(input_string)
        self.equation_box_frame = ttk.Frame(self.fractal_settings_frame)
        self.equation_box_frame.grid(row=6, columnspan=4)
        Label(self.equation_box_frame, text="Iterative Equation:   Z(n + 1)=").grid(row=0, column=0)
        self.equation = Entry(self.equation_box_frame, width=45, justify = LEFT)
        self.equation.insert(END, "Z**2 + C")
        self.equation.grid(row=0, column=1)
        Button(self.equation_box_frame, text="Verify", command=lambda: verify_string(self.equation.get())).grid(row=0, column=2)
        #

        ###---------\/\/\/\/\/\/\--------COLORING SETTINGS-----------\/\/\/\/\/\/\----------###
        ###---------\/\/\/\/\/\/\--------COLORING SETTINGS-----------\/\/\/\/\/\/\----------###
        ###---------\/\/\/\/\/\/\--------COLORING SETTINGS-----------\/\/\/\/\/\/\----------###
        ###---------\/\/\/\/\/\/\--------COLORING SETTINGS-----------\/\/\/\/\/\/\----------###
        ###---------\/\/\/\/\/\/\--------COLORING SETTINGS-----------\/\/\/\/\/\/\----------###

        self.coloring_settings_frame = ttk.Frame(self.master)
        self.coloring_settings_frame.grid(row=1, column=0, sticky="ew")
        ttk.Separator(self.coloring_settings_frame, orient=HORIZONTAL).grid(row=9, columnspan=4, sticky="ew")
        Label(self.coloring_settings_frame, text="Coloring Settings").grid(row=9, column=1)
        Label(self.coloring_settings_frame, text="Scheme Active").grid(row=10, column=0)
        Label(self.coloring_settings_frame, text="Coloring Technique").grid(row=10, column=1)
        Label(self.coloring_settings_frame, text="Coloring Scale").grid(row=10, column=2)
        Label(self.coloring_settings_frame, text="Coloring Sequence").grid(row=10, column=3)

        self.scheme_1_check = IntVar()
        self.scheme_1_check.set(1)
        self.scheme_1_button = Checkbutton(self.coloring_settings_frame, text="Color Scheme 1", variable=self.scheme_1_check)
        self.scheme_1_button.grid(row=11, column=0, sticky=W)
        self.scheme_2_check = IntVar()
        self.scheme_2_button = Checkbutton(self.coloring_settings_frame, text="Color Scheme 2", variable=self.scheme_2_check)
        self.scheme_2_button.grid(row=12, column=0, sticky=W)
        self.scheme_3_check = IntVar()
        self.scheme_3_button = Checkbutton(self.coloring_settings_frame, text="Color Scheme 3", variable=self.scheme_3_check)
        self.scheme_3_button.grid(row=13, column=0, sticky=W)
        self.scheme_4_check = IntVar()
        self.scheme_4_button = Checkbutton(self.coloring_settings_frame, text="Color Scheme 4", variable=self.scheme_4_check)
        self.scheme_4_button.grid(row=14, column=0, sticky=W)
        class color_scheme_dropdown:
            def __init__(self, parent_frame):
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
                self.box = ttk.Combobox(self.parent_frame, textvariable=self.box_value, state='readonly')
                self.box.bind("<<ComboboxSelected>>", self.newselection)
                self.box['values'] = ('Iteration Count', 'Iteration Count w/ Gradient', 'Orbit Trap: Circle', 'Orbit Trap: Ellipse', 'Orbit Trap: Line', 'Orbit Trap: Cross', 'Orbit Trap: Spiral')
                self.box.current(0)
        self.scheme_1_dropdown = color_scheme_dropdown(self.coloring_settings_frame)
        self.scheme_1_dropdown.box_update(1) #set the default coloring scheme to iteration count w/ gradient
        self.scheme_1_dropdown.box.grid(column=1, row=11)
        self.scheme_2_dropdown = color_scheme_dropdown(self.coloring_settings_frame)
        self.scheme_2_dropdown.box.grid(column=1, row=12)
        self.scheme_3_dropdown = color_scheme_dropdown(self.coloring_settings_frame)
        self.scheme_3_dropdown.box.grid(column=1, row=13)
        self.scheme_4_dropdown = color_scheme_dropdown(self.coloring_settings_frame)
        self.scheme_4_dropdown.box.grid(column=1, row=14)
        class color_scale_dropdown:
            def __init__(self, parent_frame):
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
                self.box = ttk.Combobox(self.parent_frame, textvariable=self.box_value, state='readonly')
                self.box.bind("<<ComboboxSelected>>", self.newselection)
                self.box['values'] = ('Color Spectrum', 'Color Hierarchy')
                self.box.current(0)
        self.color_scale_1_dropdown = color_scale_dropdown(self.coloring_settings_frame)
        self.color_scale_1_dropdown.box.grid(column=2, row=11)
        self.color_scale_2_dropdown = color_scale_dropdown(self.coloring_settings_frame)
        self.color_scale_2_dropdown.box.grid(column=2, row=12)
        self.color_scale_3_dropdown = color_scale_dropdown(self.coloring_settings_frame)
        self.color_scale_3_dropdown.box.grid(column=2, row=13)
        self.color_scale_4_dropdown = color_scale_dropdown(self.coloring_settings_frame)
        self.color_scale_4_dropdown.box.grid(column=2, row=14)
        #
        self.sequence_1_entry = Entry(self.coloring_settings_frame, justify = RIGHT)
        self.sequence_1_entry.insert(END, '0B263')
        self.sequence_1_entry.grid(row=11, column=3)
        self.sequence_2_entry = Entry(self.coloring_settings_frame, justify = RIGHT)
        self.sequence_2_entry.insert(END, '02468')
        self.sequence_2_entry.grid(row=12, column=3)
        self.sequence_3_entry = Entry(self.coloring_settings_frame, justify = RIGHT)
        self.sequence_3_entry.insert(END, '02468')
        self.sequence_3_entry.grid(row=13, column=3)
        self.sequence_4_entry = Entry(self.coloring_settings_frame, justify = RIGHT)
        self.sequence_4_entry.insert(END, '02468')
        self.sequence_4_entry.grid(row=14, column=3)
        #--
        Label(self.coloring_settings_frame, text="Orbit Trap-Rotation: ").grid(row=17, column=0)
        self.OT_rotation_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_rotation_frame.grid(row=17, column=1, sticky="ew")
        self.OT_rotation1 = Entry(self.OT_rotation_frame, width=6, justify = RIGHT)
        self.OT_rotation1.insert(END, '0')
        self.OT_rotation1.pack(side="left")
        self.OT_rotation2 = Entry(self.OT_rotation_frame, width=6, justify = RIGHT)
        self.OT_rotation2.insert(END, '0')
        self.OT_rotation2.pack(side="left")
        self.OT_rotation3 = Entry(self.OT_rotation_frame, width=6, justify = RIGHT)
        self.OT_rotation3.insert(END, '0')
        self.OT_rotation3.pack(side="left")
        self.OT_rotation4 = Entry(self.OT_rotation_frame, width=6, justify = RIGHT)
        self.OT_rotation4.insert(END, '60')
        self.OT_rotation4.pack(side="left")
        Label(self.coloring_settings_frame, text="Orbit Trap-Radius 1: ").grid(row=18, column=0)
        self.OT_radius_frame1 = ttk.Frame(self.coloring_settings_frame)
        self.OT_radius_frame1.grid(row=18, column=1, sticky="ew")
        self.OT_radius1_1 = Entry(self.OT_radius_frame1, width=6, justify = RIGHT)
        self.OT_radius1_1.insert(END, '.3')
        self.OT_radius1_1.pack(side="left")
        self.OT_radius1_2 = Entry(self.OT_radius_frame1, width=6, justify = RIGHT)
        self.OT_radius1_2.insert(END, '1')
        self.OT_radius1_2.pack(side="left")
        self.OT_radius1_3 = Entry(self.OT_radius_frame1, width=6, justify = RIGHT)
        self.OT_radius1_3.insert(END, '.25')
        self.OT_radius1_3.pack(side="left")
        self.OT_radius1_4 = Entry(self.OT_radius_frame1, width=6, justify = RIGHT)
        self.OT_radius1_4.insert(END, '3')
        self.OT_radius1_4.pack(side="left")
        Label(self.coloring_settings_frame, text="Orbit Trap-Radius 2: ").grid(row=19, column=0)
        self.OT_radius_frame2 = ttk.Frame(self.coloring_settings_frame)
        self.OT_radius_frame2.grid(row=19, column=1, sticky="ew")
        self.OT_radius2_1 = Entry(self.OT_radius_frame2, width=6, justify = RIGHT)
        self.OT_radius2_1.insert(END, '.5')
        self.OT_radius2_1.pack(side="left")
        self.OT_radius2_2 = Entry(self.OT_radius_frame2, width=6, justify = RIGHT)
        self.OT_radius2_2.insert(END, '1')
        self.OT_radius2_2.pack(side="left")
        self.OT_radius2_3 = Entry(self.OT_radius_frame2, width=6, justify = RIGHT)
        self.OT_radius2_3.insert(END, '.25')
        self.OT_radius2_3.pack(side="left")
        self.OT_radius2_4 = Entry(self.OT_radius_frame2, width=6, justify = RIGHT)
        self.OT_radius2_4.insert(END, '2')
        self.OT_radius2_4.pack(side="left")
        #
        Label(self.coloring_settings_frame, text="Orbit Trap-Trap Count: ").grid(row=20, column=0)
        self.OT_trap_count_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_trap_count_frame.grid(row=20, column=1, sticky="ew")
        self.OT_trap_count1 = Entry(self.OT_trap_count_frame, width=6, justify = RIGHT)
        self.OT_trap_count1.insert(END, '1')
        self.OT_trap_count1.pack(side="left")
        self.OT_trap_count2 = Entry(self.OT_trap_count_frame, width=6, justify = RIGHT)
        self.OT_trap_count2.insert(END, '1')
        self.OT_trap_count2.pack(side="left")
        self.OT_trap_count3 = Entry(self.OT_trap_count_frame, width=6, justify = RIGHT)
        self.OT_trap_count3.insert(END, '1')
        self.OT_trap_count3.pack(side="left")
        self.OT_trap_count4 = Entry(self.OT_trap_count_frame, width=6, justify = RIGHT)
        self.OT_trap_count4.insert(END, '1')
        self.OT_trap_count4.pack(side="left")
        #
        Label(self.coloring_settings_frame, text="Orbit Trap-Starting Width: ").grid(row=17, column=2)
        self.OT_width_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_width_frame.grid(row=17, column=3, sticky="ew")
        self.OT_starting_width1 = Entry(self.OT_width_frame, width=6, justify = RIGHT)
        self.OT_starting_width1.insert(END, '.5')
        self.OT_starting_width1.pack(side="left")
        self.OT_starting_width2 = Entry(self.OT_width_frame, width=6, justify = RIGHT)
        self.OT_starting_width2.insert(END, '.5')
        self.OT_starting_width2.pack(side="left")
        self.OT_starting_width3 = Entry(self.OT_width_frame, width=6, justify = RIGHT)
        self.OT_starting_width3.insert(END, '.5')
        self.OT_starting_width3.pack(side="left")
        self.OT_starting_width4 = Entry(self.OT_width_frame, width=6, justify = RIGHT)
        self.OT_starting_width4.insert(END, '.5')
        self.OT_starting_width4.pack(side="left")
        Label(self.coloring_settings_frame, text="Orbit Trap-Width Deflection: ").grid(row=18, column=2)
        self.OT_width_deflection_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_width_deflection_frame.grid(row=18, column=3, sticky="ew")
        self.OT_width_deflection1 = Entry(self.OT_width_deflection_frame, width=6, justify = RIGHT)
        self.OT_width_deflection1.insert(END, '.1')
        self.OT_width_deflection1.pack(side="left")
        self.OT_width_deflection2 = Entry(self.OT_width_deflection_frame, width=6, justify = RIGHT)
        self.OT_width_deflection2.insert(END, '-.1')
        self.OT_width_deflection2.pack(side="left")
        self.OT_width_deflection3 = Entry(self.OT_width_deflection_frame, width=6, justify = RIGHT)
        self.OT_width_deflection3.insert(END, '.005')
        self.OT_width_deflection3.pack(side="left")
        self.OT_width_deflection4 = Entry(self.OT_width_deflection_frame, width=6, justify = RIGHT)
        self.OT_width_deflection4.insert(END, '0')
        self.OT_width_deflection4.pack(side="left")
        #--
        Label(self.coloring_settings_frame, text="Orbit Trap-Color Loop Distance: ").grid(row=19, column=2)
        self.OT_loop_distance_distance_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_loop_distance_distance_frame.grid(row=19, column=3, sticky="ew")
        self.OT_loop_distance1 = Entry(self.OT_loop_distance_distance_frame, width=6, justify = RIGHT)
        self.OT_loop_distance1.insert(END, '7')
        self.OT_loop_distance1.pack(side="left")
        self.OT_loop_distance2 = Entry(self.OT_loop_distance_distance_frame, width=6, justify = RIGHT)
        self.OT_loop_distance2.insert(END, '1')
        self.OT_loop_distance2.pack(side="left")
        self.OT_loop_distance3 = Entry(self.OT_loop_distance_distance_frame, width=6, justify = RIGHT)
        self.OT_loop_distance3.insert(END, '.5')
        self.OT_loop_distance3.pack(side="left")
        self.OT_loop_distance4 = Entry(self.OT_loop_distance_distance_frame, width=6, justify = RIGHT)
        self.OT_loop_distance4.insert(END, '1.2')
        self.OT_loop_distance4.pack(side="left")
        #
        #
        Label(self.coloring_settings_frame, text="Orbit Trap-Focus: ").grid(row=21, column=0)
        self.OT_focus_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_focus_frame.grid(row=21, column=1, sticky="ew", columnspan=3)
        self.OT_focus1_x = Entry(self.OT_focus_frame, width=6, justify = RIGHT)
        self.OT_focus1_x.insert(END, '1.5')
        self.OT_focus1_x.pack(side="left")
        self.OT_focus1_y = Entry(self.OT_focus_frame, width=6, justify = RIGHT)
        self.OT_focus1_y.insert(END, '1.5')
        self.OT_focus1_y.pack(side="left")
        ttk.Separator(self.OT_focus_frame, orient=VERTICAL).pack(side="left",fill=Y)
        ttk.Separator(self.OT_focus_frame, orient=VERTICAL).pack(side="left",fill=Y)
        #
        self.OT_focus2_x = Entry(self.OT_focus_frame, width=6, justify = RIGHT)
        self.OT_focus2_x.insert(END, '1')
        self.OT_focus2_x.pack(side="left")
        self.OT_focus2_y = Entry(self.OT_focus_frame, width=6, justify = RIGHT)
        self.OT_focus2_y.insert(END, '-.3')
        self.OT_focus2_y.pack(side="left")
        ttk.Separator(self.OT_focus_frame, orient=VERTICAL).pack(side="left",fill=Y)
        ttk.Separator(self.OT_focus_frame, orient=VERTICAL).pack(side="left",fill=Y)
        #
        self.OT_focus3_x = Entry(self.OT_focus_frame, width=6, justify = RIGHT)
        self.OT_focus3_x.insert(END, '1.2')
        self.OT_focus3_x.pack(side="left")
        self.OT_focus3_y = Entry(self.OT_focus_frame, width=6, justify = RIGHT)
        self.OT_focus3_y.insert(END, '.085')
        self.OT_focus3_y.pack(side="left")
        ttk.Separator(self.OT_focus_frame, orient=VERTICAL).pack(side="left",fill=Y)
        ttk.Separator(self.OT_focus_frame, orient=VERTICAL).pack(side="left",fill=Y)
        #
        self.OT_focus4_x = Entry(self.OT_focus_frame, width=6, justify = RIGHT)
        self.OT_focus4_x.insert(END, '0')
        self.OT_focus4_x.pack(side="left")
        self.OT_focus4_y = Entry(self.OT_focus_frame, width=6, justify = RIGHT)
        self.OT_focus4_y.insert(END, '0')
        self.OT_focus4_y.pack(side="left")
        #--
        Label(self.coloring_settings_frame, text="Orbit Trap-Measure Point: ").grid(row=22, column=0)
        self.OT_color_measure_point_frame = ttk.Frame(self.coloring_settings_frame)
        self.OT_color_measure_point_frame.grid(row=22, column=1, columnspan=3, sticky="ew")
        self.OT_measure_point1_x = Entry(self.OT_color_measure_point_frame, width=6, justify = RIGHT)
        self.OT_measure_point1_x.insert(END, '0')
        self.OT_measure_point1_x.pack(side="left")
        self.OT_measure_point1_y = Entry(self.OT_color_measure_point_frame, width=6, justify = RIGHT)
        self.OT_measure_point1_y.insert(END, '0')
        self.OT_measure_point1_y.pack(side="left")
        ttk.Separator(self.OT_color_measure_point_frame, orient=VERTICAL).pack(side="left",fill=Y)
        ttk.Separator(self.OT_color_measure_point_frame, orient=VERTICAL).pack(side="left",fill=Y)
        #
        self.OT_measure_point2_x = Entry(self.OT_color_measure_point_frame, width=6, justify = RIGHT)
        self.OT_measure_point2_x.insert(END, '0')
        self.OT_measure_point2_x.pack(side="left")
        self.OT_measure_point2_y = Entry(self.OT_color_measure_point_frame, width=6, justify = RIGHT)
        self.OT_measure_point2_y.insert(END, '0')
        self.OT_measure_point2_y.pack(side="left")
        ttk.Separator(self.OT_color_measure_point_frame, orient=VERTICAL).pack(side="left",fill=Y)
        ttk.Separator(self.OT_color_measure_point_frame, orient=VERTICAL).pack(side="left",fill=Y)
        #
        self.OT_measure_point3_x = Entry(self.OT_color_measure_point_frame, width=6, justify = RIGHT)
        self.OT_measure_point3_x.insert(END, '0')
        self.OT_measure_point3_x.pack(side="left")
        self.OT_measure_point3_y = Entry(self.OT_color_measure_point_frame, width=6, justify = RIGHT)
        self.OT_measure_point3_y.insert(END, '0')
        self.OT_measure_point3_y.pack(side="left")
        ttk.Separator(self.OT_color_measure_point_frame, orient=VERTICAL).pack(side="left",fill=Y)
        ttk.Separator(self.OT_color_measure_point_frame, orient=VERTICAL).pack(side="left",fill=Y)
        #
        self.OT_measure_point4_x = Entry(self.OT_color_measure_point_frame, width=6, justify = RIGHT)
        self.OT_measure_point4_x.insert(END, '0')
        self.OT_measure_point4_x.pack(side="left")
        self.OT_measure_point4_y = Entry(self.OT_color_measure_point_frame, width=6, justify = RIGHT)
        self.OT_measure_point4_y.insert(END, '0')
        self.OT_measure_point4_y.pack(side="left")
        #
        #
        self.black_background_check = IntVar()
        self.black_background_check.set(1)
        self.black_background_button = Checkbutton(self.coloring_settings_frame, text="Black Background", variable=self.black_background_check)
        self.black_background_button.grid(row=23, column=0, sticky=W)
        #----------------------------
        self.bottom_buttons_frame = ttk.Frame(self.master)
        ttk.Separator(self.bottom_buttons_frame, orient=HORIZONTAL).grid(row=9, columnspan=4, sticky="ew")
        self.bottom_buttons_frame.grid(row=2, column=0, sticky="ew")
        Label(self.bottom_buttons_frame, text="Image Name: ").grid(row=20)
        self.image_name = Entry(self.bottom_buttons_frame, width=60, justify = RIGHT)
        self.image_name.insert(END, os.getcwd().replace('\\','/') + "/Fractal.png")
        self.image_name.grid(row=20, column=1)
        Label(self.bottom_buttons_frame, text="Load Settings: ").grid(row=21, column=0)
        self.load_filename_frame = ttk.Frame(self.bottom_buttons_frame)
        self.load_filename_frame.grid(row=21, column=1, columnspan=2, sticky=EW)
        self.load_filename = Entry(self.load_filename_frame, width=60, justify = RIGHT)
        self.load_filename.insert(END, os.getcwd().replace('\\','/') + "/recent_settings.txt")
        self.load_filename.pack(side="left", expand=True, fill=X)
        self.load_filename_frame.grid_columnconfigure(0, weight=1)
        def browse_for_load_file():
            file = filedialog.askopenfilename(parent=self.load_filename_frame, initialdir=os.getcwd(), title='Select A Settings File',filetypes = (("text files","*.txt"),("all files","*.*")))
            self.load_filename.delete(0, END)
            self.load_filename.insert(END, file)
            return
        self.load_browse = Button(self.load_filename_frame, text='...', command=browse_for_load_file)
        self.load_browse.pack(side="right")
        #
        Label(self.bottom_buttons_frame, text="Save Settings: ").grid(row=22, column=0)
        self.save_filename_frame = ttk.Frame(self.bottom_buttons_frame)
        self.save_filename_frame.grid(row=22, column=1, columnspan=2, sticky=EW)
        self.save_filename = Entry(self.save_filename_frame, width=60, justify=RIGHT)
        self.save_filename.insert(END, os.getcwd().replace('\\','/') + "/user_settings.txt")
        self.save_filename.pack(side="left", expand=True, fill=X)
        self.save_filename_frame.grid_columnconfigure(0, weight=1)
        def browse_for_save_file():
            file = filedialog.askopenfilename(parent=self.save_filename_frame, initialdir=os.getcwd(), title='Select A Settings File')
            self.save_filename.delete(0, END)
            self.save_filename.insert(END, file)
            return
        self.save_browse = Button(self.save_filename_frame, text='...', command=browse_for_save_file)
        self.save_browse.pack(side="left")
        #
        self.canvas_frame = ttk.Frame(self.master)
        self.mother.canvas_object = the_canvas(self.mother, self.canvas_frame)
        self.canvas_frame.grid(row=0,column=4,rowspan=25,columnspan=8)
        #
        self.mother.canvas_object.proportion_rectangle_check = IntVar()
        self.mother.canvas_object.proportion_rectangle_check.set(1)
        self.proportion_rectangle_button = Checkbutton(self.fractal_settings_frame, text="Scale Rectangle", variable=self.mother.canvas_object.proportion_rectangle_check)
        self.proportion_rectangle_button.grid(row=5, column=3)
        ##--------
        ##--------
        Button(self.bottom_buttons_frame, text='Load Settings', command=self.load_settings_from_file).grid(row=21, column=3, sticky=EW, pady=4)
        Button(self.bottom_buttons_frame, text='Save Settings', command=self.save_settings_file).grid(row=22, column=3, sticky=EW, pady=4)
        Button(self.bottom_buttons_frame, text='Set Default Settings', command=lambda: save_settings_file(the_file=os.getcwd().replace('\\','/')+"/default.txt")).grid(row=23, column=1, sticky=EW, pady=4)
        Button(self.bottom_buttons_frame, text='Reset Default Settings', command=self.reset_default_settings).grid(row=23, column=3, sticky=EW, pady=4)
        self.generate_button = Button(self.bottom_buttons_frame, text='Generate', command=self.fractal_thread)
        self.generate_button.grid(row=24, column=1, sticky=EW, pady=4)
        Button(self.bottom_buttons_frame, text='Quit', command=self.master.destroy).grid(row=24, column=3, sticky=EW, pady=4)
        ##--------
        ##--------
        self.CLI_frame = ttk.Frame(self.master)
        self.CLI_frame.grid(row=3, column=0)
        self.textbox=Text(self.CLI_frame, background="black", height=19, width=110,foreground="green")
        self.textbox.pack()
        # def redirector(self, inputStr):
            # self.textbox.insert(INSERT, inputStr)
            # self.textbox.see(END)
            # sys.stdout.flush()
        # sys.stdout.write = redirector
        class TextRedirector(object):
            def __init__(self, text_widget):
                self.text_widget = text_widget
                self.index_before_last_print = ""
                self.last_was_overwrite = False
            def write(self, the_string):
                self.text_widget.configure(state="normal")
                if self.last_was_overwrite:
                    self.text_widget.insert("end", "\n")
                self.index_before_last_print = self.text_widget.index("end")
                self.text_widget.insert("end", the_string)
                self.text_widget.see(END)
                self.text_widget.configure(state="disabled")
                self.last_was_overwrite = False
            def overwrite(self, the_string):
                self.text_widget.configure(state="normal")
                self.text_widget.delete(self.index_before_last_print + "-1c linestart", "end")
                self.text_widget.insert("end", "\n")
                self.index_before_last_print = self.text_widget.index("end")
                self.text_widget.insert("end", the_string)
                self.text_widget.see(END)
                self.text_widget.configure(state="disabled")
                self.last_was_overwrite = True

        sys.stdout = self.mother.text_out = TextRedirector(self.textbox)
        ##--------
        ##--------
        self.mother.fractal_object = fractal(self.GUI_settings_to_dict(), self.mother)
        ##--------
        ##--------
        self.mother.window2_object = window2(self.mother)
        return
        #
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
        settings['proportion_rectangle_check'] = ['int', int(self.mother.canvas_object.proportion_rectangle_check.get())]
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
        try:
            self.x_min.delete(0, END)
            self.x_min.insert(END, str(self.mother.fractal_object.settings['x_min'][1]))
            self.x_max.delete(0, END)
            self.x_max.insert(END, self.mother.fractal_object.settings['x_max'][1])
            self.y_min.delete(0, END)
            self.y_min.insert(END, self.mother.fractal_object.settings['y_min'][1])
            self.y_max.delete(0, END)
            self.y_max.insert(END, self.mother.fractal_object.settings['y_max'][1])
            self.iterations.delete(0, END)
            self.iterations.insert(END, self.mother.fractal_object.settings['iterations'][1])
            self.c_formula.set(self.mother.fractal_object.settings['c_formula'][1])
            if self.c_formula.get() == 1:
                self.x_yi.invoke()
            elif self.c_formula.get() == 2:
                self.a_bi.invoke()
            self.c_real.delete(0, END)
            self.c_real.insert(END, self.mother.fractal_object.settings['c_real'][1])
            self.c_imag.delete(0, END)
            self.c_imag.insert(END, self.mother.fractal_object.settings['c_imag'][1])
            self.image_width.delete(0, END)
            self.image_width.insert(END, self.mother.fractal_object.settings['image_width'][1])
            self.image_height.delete(0, END)
            self.image_height.insert(END, self.mother.fractal_object.settings['image_height'][1])
            self.rotation.delete(0, END)
            self.rotation.insert(END, self.mother.fractal_object.settings['rotation'][1])
            self.image_name.delete(0, END)
            self.image_name.insert(END, self.mother.fractal_object.settings['image_name'][1])
            self.bailout_value.delete(0, END)
            self.bailout_value.insert(END, self.mother.fractal_object.settings['bailout_value'][1])
            # self.thread_count.delete(0, END)
            # self.thread_count.insert(END, self.mother.fractal_object.settings['thread_count'][1])
            self.equation.delete(0, END)
            self.equation.insert(END, self.mother.fractal_object.settings['equation'][1])
            if self.mother.canvas_object.proportion_rectangle_check.get() != self.mother.fractal_object.settings['proportion_rectangle_check'][1]:
                self.proportion_rectangle_button.invoke()
            if self.scheme_1_check.get() != self.mother.fractal_object.settings['scheme_check'][1][0]:
                self.scheme_1_button.invoke()
            self.scheme_1_dropdown_value = self.mother.fractal_object.settings['scheme_dropdown'][1][0]
            self.scheme_1_dropdown.box_update(self.scheme_1_dropdown_value)
            self.color_scale_1_dropdown_value = self.mother.fractal_object.settings['color_scale_dropdown'][1][0]
            self.color_scale_1_dropdown.box_update(self.color_scale_1_dropdown_value)
            if self.scheme_2_check.get() != self.mother.fractal_object.settings['scheme_check'][1][1]:
                self.scheme_2_button.invoke()
            self.scheme_2_dropdown_value = self.mother.fractal_object.settings['scheme_dropdown'][1][1]
            self.scheme_2_dropdown.box_update(self.scheme_2_dropdown_value)
            self.color_scale_2_dropdown_value = self.mother.fractal_object.settings['color_scale_dropdown'][1][1]
            self.color_scale_2_dropdown.box_update(self.color_scale_2_dropdown_value)
            self.scheme_3_check
            if self.scheme_3_check.get() != self.mother.fractal_object.settings['scheme_check'][1][2]:
                self.scheme_3_button.invoke()
            self.scheme_3_dropdown_value = self.mother.fractal_object.settings['scheme_dropdown'][1][2]
            self.scheme_3_dropdown.box_update(self.scheme_3_dropdown_value)
            self.color_scale_3_dropdown_value = self.mother.fractal_object.settings['color_scale_dropdown'][1][2]
            self.color_scale_3_dropdown.box_update(self.color_scale_3_dropdown_value)
            if self.scheme_4_check.get() != self.mother.fractal_object.settings['scheme_check'][1][3]:
                self.scheme_4_button.invoke()
            self.scheme_4_dropdown_value = self.mother.fractal_object.settings['scheme_dropdown'][1][3]
            self.scheme_4_dropdown.box_update(self.scheme_4_dropdown_value)
            self.color_scale_4_dropdown_value = self.mother.fractal_object.settings['color_scale_dropdown'][1][3]
            self.color_scale_4_dropdown.box_update(self.color_scale_4_dropdown_value)
            self.sequence_1_entry.delete(0, END)
            self.sequence_1_entry.insert(END, self.mother.fractal_object.settings['sequence_entry'][1][0])
            self.sequence_2_entry.delete(0, END)
            self.sequence_2_entry.insert(END, self.mother.fractal_object.settings['sequence_entry'][1][1])
            self.sequence_3_entry.delete(0, END)
            self.sequence_3_entry.insert(END, self.mother.fractal_object.settings['sequence_entry'][1][2])
            self.sequence_4_entry.delete(0, END)
            self.sequence_4_entry.insert(END, self.mother.fractal_object.settings['sequence_entry'][1][3])
            self.OT_focus1_x.delete(0, END)
            self.OT_focus1_x.insert(END, str(self.mother.fractal_object.settings['OT_focus1_x'][1]))
            self.OT_focus2_x.delete(0, END)
            self.OT_focus2_x.insert(END, str(self.mother.fractal_object.settings['OT_focus2_x'][1]))
            self.OT_focus3_x.delete(0, END)
            self.OT_focus3_x.insert(END, str(self.mother.fractal_object.settings['OT_focus3_x'][1]))
            self.OT_focus4_x.delete(0, END)
            self.OT_focus4_x.insert(END, str(self.mother.fractal_object.settings['OT_focus4_x'][1]))
            self.OT_focus1_y.delete(0, END)
            self.OT_focus1_y.insert(END, str(self.mother.fractal_object.settings['OT_focus1_y'][1]))
            self.OT_focus2_y.delete(0, END)
            self.OT_focus2_y.insert(END, str(self.mother.fractal_object.settings['OT_focus2_y'][1]))
            self.OT_focus3_y.delete(0, END)
            self.OT_focus3_y.insert(END, str(self.mother.fractal_object.settings['OT_focus3_y'][1]))
            self.OT_focus4_y.delete(0, END)
            self.OT_focus4_y.insert(END, str(self.mother.fractal_object.settings['OT_focus4_y'][1]))
            self.OT_rotation1.delete(0, END)
            self.OT_rotation1.insert(END, self.mother.fractal_object.settings['OT_rotation1'][1])
            self.OT_rotation2.delete(0, END)
            self.OT_rotation2.insert(END, self.mother.fractal_object.settings['OT_rotation2'][1])
            self.OT_rotation3.delete(0, END)
            self.OT_rotation3.insert(END, self.mother.fractal_object.settings['OT_rotation3'][1])
            self.OT_rotation4.delete(0, END)
            self.OT_rotation4.insert(END, self.mother.fractal_object.settings['OT_rotation4'][1])
            self.OT_radius1_1.delete(0, END)
            self.OT_radius1_1.insert(END, self.mother.fractal_object.settings['OT_radius1_1'][1])
            self.OT_radius1_2.delete(0, END)
            self.OT_radius1_2.insert(END, self.mother.fractal_object.settings['OT_radius1_2'][1])
            self.OT_radius1_3.delete(0, END)
            self.OT_radius1_3.insert(END, self.mother.fractal_object.settings['OT_radius1_3'][1])
            self.OT_radius1_4.delete(0, END)
            self.OT_radius1_4.insert(END, self.mother.fractal_object.settings['OT_radius1_4'][1])
            self.OT_radius2_1.delete(0, END)
            self.OT_radius2_1.insert(END, self.mother.fractal_object.settings['OT_radius2_1'][1])
            self.OT_radius2_2.delete(0, END)
            self.OT_radius2_2.insert(END, self.mother.fractal_object.settings['OT_radius2_2'][1])
            self.OT_radius2_3.delete(0, END)
            self.OT_radius2_3.insert(END, self.mother.fractal_object.settings['OT_radius2_3'][1])
            self.OT_radius2_4.delete(0, END)
            self.OT_radius2_4.insert(END, self.mother.fractal_object.settings['OT_radius2_4'][1])
            self.OT_starting_width1.delete(0, END)
            self.OT_starting_width1.insert(END, self.mother.fractal_object.settings['OT_starting_width1'][1])
            self.OT_starting_width2.delete(0, END)
            self.OT_starting_width2.insert(END, self.mother.fractal_object.settings['OT_starting_width2'][1])
            self.OT_starting_width3.delete(0, END)
            self.OT_starting_width3.insert(END, self.mother.fractal_object.settings['OT_starting_width3'][1])
            self.OT_starting_width4.delete(0, END)
            self.OT_starting_width4.insert(END, self.mother.fractal_object.settings['OT_starting_width4'][1])
            self.OT_width_deflection1.delete(0, END)
            self.OT_width_deflection1.insert(END, self.mother.fractal_object.settings['OT_width_deflection1'][1])
            self.OT_width_deflection2.delete(0, END)
            self.OT_width_deflection2.insert(END, self.mother.fractal_object.settings['OT_width_deflection2'][1])
            self.OT_width_deflection3.delete(0, END)
            self.OT_width_deflection3.insert(END, self.mother.fractal_object.settings['OT_width_deflection3'][1])
            self.OT_width_deflection4.delete(0, END)
            self.OT_width_deflection4.insert(END, self.mother.fractal_object.settings['OT_width_deflection4'][1])
            self.OT_measure_point1_x.delete(0, END)
            self.OT_measure_point1_x.insert(END, str(self.mother.fractal_object.settings['OT_measure_point1_x'][1]))
            self.OT_measure_point2_x.delete(0, END)
            self.OT_measure_point2_x.insert(END, str(self.mother.fractal_object.settings['OT_measure_point2_x'][1]))
            self.OT_measure_point3_x.delete(0, END)
            self.OT_measure_point3_x.insert(END, str(self.mother.fractal_object.settings['OT_measure_point3_x'][1]))
            self.OT_measure_point4_x.delete(0, END)
            self.OT_measure_point4_x.insert(END, str(self.mother.fractal_object.settings['OT_measure_point4_x'][1]))
            self.OT_measure_point1_y.delete(0, END)
            self.OT_measure_point1_y.insert(END, str(self.mother.fractal_object.settings['OT_measure_point1_y'][1]))
            self.OT_measure_point2_y.delete(0, END)
            self.OT_measure_point2_y.insert(END, str(self.mother.fractal_object.settings['OT_measure_point2_y'][1]))
            self.OT_measure_point3_y.delete(0, END)
            self.OT_measure_point3_y.insert(END, str(self.mother.fractal_object.settings['OT_measure_point3_y'][1]))
            self.OT_measure_point4_y.delete(0, END)
            self.OT_measure_point4_y.insert(END, str(self.mother.fractal_object.settings['OT_measure_point4_y'][1]))
            self.OT_loop_distance1.delete(0, END)
            self.OT_loop_distance1.insert(END, self.mother.fractal_object.settings['OT_loop_distance1'][1])
            self.OT_loop_distance2.delete(0, END)
            self.OT_loop_distance2.insert(END, self.mother.fractal_object.settings['OT_loop_distance2'][1])
            self.OT_loop_distance3.delete(0, END)
            self.OT_loop_distance3.insert(END, self.mother.fractal_object.settings['OT_loop_distance3'][1])
            self.OT_loop_distance4.delete(0, END)
            self.OT_loop_distance4.insert(END, self.mother.fractal_object.settings['OT_loop_distance4'][1])
            self.OT_trap_count1.delete(0, END)
            self.OT_trap_count1.insert(END, self.mother.fractal_object.settings['OT_trap_count1'][1])
            self.OT_trap_count2.delete(0, END)
            self.OT_trap_count2.insert(END, self.mother.fractal_object.settings['OT_trap_count2'][1])
            self.OT_trap_count3.delete(0, END)
            self.OT_trap_count3.insert(END, self.mother.fractal_object.settings['OT_trap_count3'][1])
            self.OT_trap_count4.delete(0, END)
            self.OT_trap_count4.insert(END, self.mother.fractal_object.settings['OT_trap_count4'][1])
            if self.black_background_check.get() != self.mother.fractal_object.settings['black_background_check'][1]:
                self.black_background_button.invoke()
            print("\n!!!!! Settings Have Been Loaded !!!!!")
        except: print("\n!!!!! Failure In Loading Settings !!!!!")
        return

    def save_settings_file(self):
        self.mother.fractal_object.settings = self.GUI_settings_to_dict() #GUI gather settings into dictionary, dictionary given to object
        self.mother.fractal_object.save_settings(manual=True)
        self.mother.window2_object.batch_GUI_settings_to_dict()
        self.mother.window2_object.save_batch_settings(manual=True)
        return

    def load_settings_from_file(self, the_file=None):
        if the_file == None: the_file = self.mother.fractal_object.settings['load_filename'][1] = self.load_filename.get()
        self.mother.fractal_object.settings_import_from_file(the_file)
        self.mother.window2_object.batch_settings_import_from_file(the_file)
        self.values_from_object_to_GUI()
        # self.mother.window2_object.batch_values_from_object_to_GUI()
        return

    def fractal_thread(self):
        self.generate_button.config(state="disabled")
        self.mother.fractal_object.t = time.clock()
        self.mother.fractal_object.settings = self.GUI_settings_to_dict()
        self.mother.fractal_object.save_settings()
        t = threading.Thread(target=self.fractal_thread_sequence)
        t.daemon = True
        t.start()
        return

    def reset_default_settings(self):
        if os.path.isfile(os.getcwd().replace('\\','/') + "/default.txt"):
            os.remove(os.getcwd().replace('\\','/') + "/default.txt")
            print("\nDefault settings have been cleared!")
        else: print("\nFound no settings to clear!")
        return

    def fractal_thread_sequence(self):
        self.mother.fractal_object.compute()
        # self.mother.canvas_object.load_new_picture(self.mother.fractal_object.settings['image_name'][1])
        self.generate_button.config(state="normal")
        self.master.after(1, lambda: self.master.focus_force())
        return

class VerticalScrollPack(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.canvas = Canvas(root, borderwidth=0)
        self.frame = Frame(self.canvas)
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class VerticalScrollGrid(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.canvas = Canvas(root, borderwidth=0)
        self.frame = Frame(self.canvas)
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky='NS')
        self.canvas.grid(row=0, column=0, sticky='NSEW')
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        #self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Button-4>", self.on_mousewheel_up)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel_down)
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def on_mousewheel_down(self, event): self.canvas.yview_scroll(1, "units")
    def on_mousewheel_up(self, event): self.canvas.yview_scroll(-1, "units")

class window2:
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
        ttk.Separator(self.scrolled_frame.frame, orient=HORIZONTAL).grid(row=1, columnspan=9, sticky="ew")
        ##-----------------##
        class line_item:
            def __init__(self, parameter_name, which_frame, row_number, start_value, end_value):
                #Label
                Label(which_frame, text=parameter_name + ": ").grid(row=row_number,column=0)
                self.current_value = start_value
                #Start Value
                self.start_entry = Entry(which_frame, justify = RIGHT, width=8)
                self.start_entry.insert(END, str(start_value))
                self.start_entry.grid(row=row_number, column=1)
                #End Value
                self.end_entry = Entry(which_frame, justify = RIGHT, width=8)
                self.end_entry.insert(END, str(end_value))
                self.end_entry.grid(row=row_number, column=2)
                self.end_entry.config(state = DISABLED)
                #Delta Checkbox
                self.delta_check = IntVar()
                self.delta_check.set(1)
                self.delta_button = Checkbutton(which_frame, text = "Delta Method", variable = self.delta_check, command=self.delta_button_toggle)
                self.delta_button.grid(row=row_number,column=3)
                #Delta Value
                self.delta = Entry(which_frame, justify = RIGHT, width=8)
                self.delta.insert(END, '0')
                self.delta.grid(row=row_number, column=4)
                #Smooth Start Checkbox
                self.smooth_start_check = IntVar()
                self.smooth_start_check.set(1)
                self.smooth_start_button = Checkbutton(which_frame, text = "Smooth Start", variable = self.smooth_start_check)
                self.smooth_start_button.grid(row=row_number,column=5)
                self.smooth_start_button.config(state = DISABLED)
                #Smooth End Checkbox
                self.smooth_end_check = IntVar()
                self.smooth_end_check.set(1)
                self.smooth_end_button = Checkbutton(which_frame, text = "Smooth End", variable = self.smooth_end_check)
                self.smooth_end_button.grid(row=row_number,column=6)
                self.smooth_end_button.config(state = DISABLED)
                #Cycle Checkbox
                self.cycle_check = IntVar()
                self.cycle_check.set(0)
                self.cycle_button = Checkbutton(which_frame, text = "Cycle", variable = self.cycle_check, command = self.cycle_button_toggle)
                self.cycle_button.grid(row=row_number,column=7)
                #Cycle Period
                self.cycle_period = Entry(which_frame, justify = RIGHT, width=8)
                self.cycle_period.insert(END, '120')
                self.cycle_period.grid(row=row_number, column=8)
                self.cycle_period.config(state = DISABLED)
                return
            def delta_button_toggle(self, event=None):
                checked = self.delta_check.get()
                if self.cycle_check.get() == self.delta_check.get() == 1:
                    self.cycle_button.invoke()
                if checked:
                    self.delta.config(state = NORMAL)
                    self.end_entry.config(state = DISABLED)
                    self.smooth_start_check.set(0)
                    self.smooth_end_check.set(0)
                    self.smooth_start_button.config(state = DISABLED)
                    self.smooth_end_button.config(state = DISABLED)
                else:
                    self.delta.config(state = DISABLED)
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
                    self.smooth_start_button.config(state = DISABLED)
                    self.smooth_end_button.config(state = DISABLED)
                else:
                    self.cycle_period.config(state = DISABLED)
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
        ttk.Separator(bottom_frame, orient=HORIZONTAL).grid(row=64, columnspan=3, sticky="ew")
        Label(bottom_frame, text="Image Numbering Start: ").grid(row=65,column=0)
        self.image_numbering_entry = Entry(bottom_frame, justify = RIGHT, width=8)
        self.image_numbering_entry.insert(END, '1')
        self.image_numbering_entry.grid(row=65, column=1)
        self.batch_data['image_number'] = int(self.image_numbering_entry.get())
        Label(bottom_frame, text="Number Of Steps: ").grid(row=66, column=0)
        self.number_of_steps_entry = Entry(bottom_frame, justify = RIGHT, width=8)
        self.number_of_steps_entry.insert(END, '10')
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
            if os.path.isfile(os.getcwd().replace('\\','/') + "/recent_settings_batch.txt"):
                os.replace("recent_settings.txt", "recent_settings_old_batch.txt")
            f = open(os.getcwd().replace('\\','/') + '/recent_settings_batch.txt', 'w')
        json.dump(self.batch_data_values, f)
        # f.write('{')
        # for index, key in enumerate(self.batch_data.keys()):
        #    if index == len(self.batch_data)-1: line = "'" + key + "':" + str(self.batch_data[key]) + "\n" #if statement to make sure a comma doesn't get placed on the last line
        #    else: line = "'" + key + "':" + str(self.batch_data[key]) + ",\n"
        #    f.write(line)
        # f.write('}')
        f.close()
        print("\nBatch settings have been saved!")
        return
    def batch_settings_import_from_file(self, filename):
        try:
            name = filename[:len(filename)-4] + "_batch.txt"
            self.batch_data_values = json.load(open(name))
            self.batch_values_from_dict_to_GUI()
            print("\nBatch settings have been loaded!")
        except: print("\nFailed to load batch settings!")
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
                self.batch_data[key].start_entry.delete(0, END)
                self.batch_data[key].start_entry.insert(END, str(self.batch_data_values[key][0]))
                self.batch_data[key].end_entry.delete(0, END)
                self.batch_data[key].end_entry.insert(END, str(self.batch_data_values[key][1]))
                self.batch_data[key].delta.delete(0, END)
                self.batch_data[key].delta.insert(END, str(self.batch_data_values[key][3]))
                self.batch_data[key].cycle_period.delete(0, END)
                self.batch_data[key].cycle_period.insert(END, str(self.batch_data_values[key][7]))
                if self.batch_data[key].delta_check.get() != self.batch_data_values[key][2]:
                    self.batch_data[key].delta_check.invoke()
                if self.batch_data[key].smooth_start_check.get() != self.batch_data_values[key][4]:
                    self.batch_data[key].smooth_start_check.invoke()
                if self.batch_data[key].smooth_end_check.get() != self.batch_data_values[key][5]:
                    self.batch_data[key].smooth_end_check.invoke()
                if self.batch_data[key].cycle_check.get() != self.batch_data_values[key][6]:
                    self.batch_data[key].cycle_check.invoke()
        self.number_of_steps_entry.delete(0, END)
        self.number_of_steps_entry.insert(END, str(self.batch_data_values['number_of_steps']))
        self.image_numbering_entry.delete(0, END)
        self.image_numbering_entry.insert(END, str(self.batch_data_values['image_number']))
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
                self.batch_data[key].start_entry.delete(0, END)
                self.batch_data[key].start_entry.insert(END, str(self.mother.fractal_object.settings[key][1]))
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

class mother_object:
    def __init__(self):
        self.window1_object = window1(self)
        if os.path.isfile(os.getcwd().replace('\\','/')+"/default.txt"): self.window1_object.load_settings_from_file(the_file=os.getcwd().replace('\\','/')+"/default.txt")
        elif os.path.isfile(os.getcwd().replace('\\','/')+"/recent_settings.txt"): self.window1_object.load_settings_from_file(the_file=os.getcwd().replace('\\','/')+"/recent_settings.txt")
        mainloop()

if __name__ == '__main__':
    mother_object()
