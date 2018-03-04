import numpy as np
import os
import math
from PIL import Image
import time
import json

class Fractal:
    def __init__(self, dictionary_of_settings, parent):
        self.preliminary_tasks_done = False
        self.settings = dictionary_of_settings
        self.parent = parent
        # self.canvas_object = canvas_object
        self.orbit_trap_list = (2,3,4,5,6)
        self.previous_settings = None
        self.previous_iterations = 'NA'
        self.previous_previous_iterations ='NA'
        self.packed_settings={}
    def print_tensor(self, the_ndarray):
        if type(the_ndarray)!=np.ndarray:
            print(str(the_ndarray))
            return
        if len(the_ndarray.shape)!=3:
            print(str(the_ndarray))
            return
        for i in range(the_ndarray.shape[2]): print("\n"+str(the_ndarray[...,i]))
        return
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
    def generate_refinement_steps(self,ar):
        smallest_dim = min(ar.shape[0],ar.shape[1])
        divide_size = 1
        while divide_size*2 < smallest_dim:
            divide_size *= 2
        done_matrix = np.zeros((ar.shape[0],ar.shape[1]))==1
        old_relevant_mask = None
        if divide_size > 8: divide_size = int(divide_size / 2)
        while divide_size >= 1:
            tentative_row_count = ar.shape[0]/divide_size
            tentative_col_count = ar.shape[1]/divide_size
            row_count = math.ceil(tentative_row_count)
            col_count = math.ceil(tentative_col_count)
            relevant_values = np.zeros((row_count,col_count))
            for row in range(row_count):
                for col in range(col_count):
                    if not done_matrix[row*divide_size,col*divide_size]:
                        relevant_values[row,col] = ar[row*divide_size,col*divide_size]
                        done_matrix[row*divide_size,col*divide_size] = True
                    else:
                        relevant_values[row,col] = old_values[int(row/2),int(col/2)]
            relevant_mask = np.zeros(ar.shape) == 1
            relevant_mask[0::divide_size,0::divide_size] = True
            base_mask = np.copy(relevant_mask)
            if old_relevant_mask is not None: relevant_mask[old_relevant_mask] = False
            yield relevant_values,divide_size,relevant_mask,base_mask
            old_values = np.copy(relevant_values)
            old_relevant_mask = np.copy(relevant_mask)
            divide_size = int(divide_size / 2)
    def expand_array(self,ar,template):
        if ar.size != template.sum(): 
            print("template.sum(): " + str(template.sum()))
            print("ar.shape: " + str(ar.shape))
            # np.save(os.getcwd()+"/ar",ar)
            # np.save(os.getcwd()+"/template",template)
            1/0
        else: 
            new_ar = np.zeros(template.shape)
            new_ar[template] = ar.flatten()
            return new_ar
    def compute(self):
        x_center = (self.settings['x_min'][1] + self.settings['x_max'][1]) / 2
        y_center = (self.settings['y_min'][1] + self.settings['y_max'][1]) / 2
        radians = self.settings['rotation'][1] * math.pi / 180

        self.package_settings()

        self.parent.text_out.write("\nComputing coordinates...")

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
        self.parent.text_out.write("\nCoordinates have been computed.")

        # gather info about orbit traps that will be used
        self.orbit_trap_dict = {}
        for i in range(0,4):
            if self.settings['scheme_check'][1][i] == 1 and self.settings['scheme_dropdown'][1][i] in self.orbit_trap_list:
                self.orbit_trap_dict[i] = int(self.settings['scheme_dropdown'][1][i])

        # tensor of pre-colorized RGB values from orbit traps (between 0 and 1)
        self.OT_RGBs = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],4))

        # tensor to keep track of trap count. height by width by number of orbit traps
        self.OT_trap_count = np.zeros((self.settings['image_height'][1],self.settings['image_width'][1],4))

        # tensor to keep track of where orbits are trapped, to stop the pixel updating when appropriate
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
        
        self.saved_RGB_vals = False
        for sub_matrix,step_size,relevant_mask,base_mask in self.generate_refinement_steps(self.coordinate_matrix):
            # reset some erroneous calculations from previous refinement step
            self.main_escape_iterations[relevant_mask]=-1
            self.OT_escape_iterations[relevant_mask]=-1
            self.escape_distance[relevant_mask]=-1
            self.OT_escape_iterations[relevant_mask]=-1
            
            rows,columns=sub_matrix.shape[0],sub_matrix.shape[1]
            self.parent.text_out.write("\n"+str(rows)+"x"+str(columns)+" out of "+str(self.settings['image_height'][1])+"x"+str(self.settings['image_width'][1]))
            self.z_current = np.zeros((relevant_mask.shape[0],relevant_mask.shape[1]),dtype=np.complex_)

            iteration_mask = np.copy(relevant_mask)
            # freakin ITERATE
            for iteration in range(0, int(self.settings['iterations'][1])):
                if self.parent.stop_early: 
                    self.parent.fractal_processing = False
                    return
                self.current_iteration = iteration
                if self.settings['c_formula'][1] == 1:
                    self.z_current[iteration_mask] = self.iterate_calc(self.z_current[iteration_mask], 
                                                                      self.coordinate_matrix[iteration_mask])
                elif self.settings['c_formula'][1] == 2:
                    if iteration != 0: self.z_current[iteration_mask] = self.iterate_calc(self.z_current[iteration_mask], 
                                                                                         complex(self.settings['c_real'][1], 
                                                                                         self.settings['c_imag'][1]))
                    else:
                        self.z_current[iteration_mask] = self.iterate_calc(self.z_current[iteration_mask], 
                                                                          self.coordinate_matrix[iteration_mask])
                where_nan = np.isnan(self.z_current)
                iteration_mask[where_nan] = False
                if len(self.orbit_trap_dict) > 0: self.orbit_traps(self.z_current)
                
                bailout_escaped = (abs(self.z_current) > self.settings['bailout_value'][1])
                
                not_yet_escaped = (self.main_escape_iterations[relevant_mask] == -1)
                
                where_escaped = np.logical_and(bailout_escaped[relevant_mask],not_yet_escaped)
                where_escaped = self.expand_array(where_escaped,relevant_mask).astype(np.bool)
                
                self.main_escape_iterations[where_escaped] = iteration
                
                esc_distance_not_set = self.escape_distance == -1
                # esc_distance_not_set = self.expand_array(esc_distance_not_set,relevant_mask)
                
                # expanded_z_current = self.expand_array(self.z_current,base_mask)
                self.escape_distance[np.logical_and(bailout_escaped, 
                                                    esc_distance_not_set)] = np.abs(self.z_current[np.logical_and((abs(self.z_current) > self.settings['bailout_value'][1]), self.escape_distance == -1)])
            
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
            if not isinstance(self.saved_RGB_vals,np.ndarray):
                self.saved_RGB_vals = np.copy(self.final_RGB_vals)
            else:
                diff = base_mask.astype(np.int32) - relevant_mask.astype(np.int32)
                diff = diff.astype(np.bool)
                self.final_RGB_vals[diff] = self.saved_RGB_vals[diff]
                self.saved_RGB_vals = np.copy(self.final_RGB_vals)
            picture = self.saved_RGB_vals[base_mask].reshape(list(sub_matrix.shape)+[3])
            Image.fromarray(np.uint8(picture)).save(self.settings['image_name'][1])
            
            # load the image into the canvas
            self.parent.canvas_object.load_new_picture(self.settings['image_name'][1])

            self.tt = time.clock()
            self.parent.text_out.write("\nElapsed time: " + self.seconds_to_time(self.tt-self.t))
            self.t = self.tt
    def orbit_traps(self, current_complex_matrix):
        for i in self.orbit_trap_dict.keys():
            if (self.orbit_trap_dict[i] == 2) or (self.orbit_trap_dict[i] == 3):
                self.OT_ellipse(current_complex_matrix, i)
            elif self.orbit_trap_dict[i] == 4:
                self.OT_line(current_complex_matrix, i)
            elif self.orbit_trap_dict[i] == 5:
                self.OT_cross(current_complex_matrix, i)
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
            self.parent.text_out.write("Type error: non-number passed to the seconds_to_time function.")
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
        if not os.path.isfile(os.getcwd().replace('\\','/') + "/save/log.csv"):
            f = open(os.getcwd().replace('\\','/') + "/save/log.csv","w")
            line = 'X Min,X Max,Y Min,Y Max,Image Width,Image Height,Iterations,Time\n'
            f.write(line)
        else:
            f = open(os.getcwd().replace('\\','/') + "/save/log.csv","a")
        line = str(self.settings['x_min'][1]) + ", " + str(self.settings['x_max'][1]) + ", " + str(self.settings['y_min'][1]) + ", " + str(self.settings['y_max'][1]) + ", " + str(self.settings['image_width'][1]) + ", " + str(self.settings['image_height'][1]) + ", " + str(self.settings['iterations'][1]) + ", " + str(time) + '\n'
        f.write(line)
        f.close()
    def save_settings(self, manual=False, default=False):
        if default: f = os.getcwd().replace('\\','/')+"/save/default.json"
        elif manual: f = self.settings['save_filename'][1]
        else:
            if os.path.isfile(os.getcwd().replace('\\','/') + "/save/recent_settings.json"):
                if os.path.isfile(os.getcwd().replace('\\','/') + "/save/recent_settings_old.json"):
                    os.remove(os.getcwd().replace('\\','/') + "/save/recent_settings_old.json")
                os.rename(os.getcwd().replace('\\','/') + "/save/recent_settings.json", 
                          os.getcwd().replace('\\','/') + "/save/recent_settings_old.json")
            f = os.getcwd().replace('\\','/') + '/save/recent_settings.json'
        with open(f, 'w') as fp:
            json.dump(self.settings, fp, sort_keys=True, indent=4)
        if default: 
            self.parent.text_out.write("\n!!!!! Default Settings Have Been Set !!!!!")
        elif manual: self.parent.text_out.write("\n!!!!! Settings Have Been Saved !!!!!")
        else: self.parent.text_out.write("\n!!!!! Settings Have Been Backed Up !!!!!")
    def settings_import_from_file(self, filename):
        try:
            with open(filename, 'r') as fp:
                self.settings = json.load(fp)
        except: 
            print("Couldn't import file settings from " + filename)
        return
