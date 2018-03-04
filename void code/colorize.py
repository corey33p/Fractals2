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
