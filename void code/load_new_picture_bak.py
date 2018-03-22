    def load_new_picture(self, picture_path, start_fresh=False):
        if start_fresh: 
            self.image_memory = []
            copyfile(os.getcwd()+"\\source\\Checkerboard.png",
                     os.getcwd()+"\\temp\\background.png")
        else:
            self.background.save(os.getcwd()+'\\temp\\background.png')
        picture_path = picture_path.replace("\\","/")
        try: self.last_angle = self.parent.fractal_object.settings['rotation'][1]
        except: self.last_angle = 0
        if not os.path.isfile(picture_path):
            new_pic_array = np.zeros(shape=(10,10,3))
            picture_path = picture_path.replace("\\save\\","\\temp\\")
            picture_path = picture_path.replace('/save/','/temp/')
            Image.fromarray(np.uint8(new_pic_array)).save(picture_path)
        the_picture = Image.open(picture_path)
        self.image_size = self.display_resize_calc(self.the_canvas_max_dimensions, the_picture.size) #find new image size based on calculation
        the_picture = the_picture.resize(self.image_size, Image.ANTIALIAS)#resize image according to new size
        # the_picture.save(os.getcwd().replace('\\','/') + "/temp/Temp.png")#save the resized image
        # the_picture = Image.open(os.getcwd().replace('\\','/') + "/temp/Temp.png")#load the resized image into the_picture variable
        # self.background = Image.open(os.getcwd().replace('\\','/') + "/source/Checkerboard.png")
        self.image_start_x = int((self.the_canvas_maximum_width-self.image_size[0])/2)
        self.image_start_y = int((self.the_canvas_maximum_height-self.image_size[1])/2)
        self.background.paste(the_picture, (self.image_start_x, self.image_start_y)) #paste resized image into middle of canvas
        self.current_img = ImageTk.PhotoImage(self.background)
        self.image_memory.append(self.current_img) # in an attempt to keep the canvas from flashing whenever a new image is loaded
        # self.the_canvas.delete("image")
        self.the_canvas.create_image((0,0), anchor="nw", image=self.current_img, tag="image")#create the image in the canvas
        self.the_canvas.pack()#pack the canvas into the frame
        try: os.remove(os.getcwd().replace('\\','/') + "/temp/Temp.png")
        except: pass
        if not start_fresh:
            try: self.the_canvas.tag_raise(self.rect)
            except: pass
        else:
            self.the_canvas.delete(self.rect)
        return