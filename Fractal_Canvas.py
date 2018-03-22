import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk, ImageFile
from shutil import copyfile
import os
import numpy as np

class FractalCanvas:
    def __init__(self, parent, parent_frame):
        self.parent = parent
        self.x = self.y = 0
        self.rect_start_x = self.rect_start_y = -2
        self.rect_end_x = self.rect_end_y = 2
        self.parent_frame = parent_frame
        self.image_memory = []
        self.make_canvas()
        self.the_canvas.create_image((0,0),anchor="nw", image=self.background, tag="background")
        self.load_new_picture(os.getcwd().replace('\\','/') + "/save/Fractal.png")
        self.rect = self.the_canvas.create_rectangle(self.image_start_x, self.image_start_y, self.image_start_x + self.image_size[0], self.image_start_y + self.image_size[1], dash=(3,2), width=2, outline="gray")
    def make_canvas(self):
        self.the_canvas_maximum_width = 955
        self.the_canvas_maximum_height = 955
        self.the_canvas_max_dimensions = (self.the_canvas_maximum_width, self.the_canvas_maximum_height)
        self.the_canvas = Canvas(self.parent_frame, cursor="cross")
        self.the_canvas.config(width=self.the_canvas_maximum_width, height=self.the_canvas_maximum_height)
        background = Image.open(os.getcwd().replace('\\','/') + "/Source/Checkerboard.png")
        self.background = ImageTk.PhotoImage(background)
        self.the_canvas.create_image((0,0), anchor="nw", image=self.background)
        self.the_canvas.pack(side="top", fill="both", expand=True)
        self.the_canvas.bind("<ButtonPress-1>", self.on_primary_button_press)
        self.the_canvas.bind("<B1-Motion>", self.on_primary_button_drag)
        self.the_canvas.bind("<ButtonRelease-1>", self.on_primary_button_release)
        self.the_canvas.bind("<ButtonPress-3>", self.on_secondary_button_press)
        self.the_canvas.bind("<B3-Motion>", self.on_secondary_button_drag)
        self.the_canvas.bind("<ButtonRelease-3>", self.on_secondary_button_release)
    def load_new_picture(self, picture_path, start_fresh=False):
        if start_fresh: 
            self.image_memory = []
            self.the_canvas.delete("fractal","rectangle")
        picture_path = picture_path.replace("\\","/")
        if os.path.isfile(picture_path):
            the_picture = Image.open(picture_path)
            self.image_size = self.display_resize_calc(self.the_canvas_max_dimensions, the_picture.size)
            the_picture = the_picture.resize(self.image_size, Image.ANTIALIAS)
            self.image_start_x = int((self.the_canvas_maximum_width-self.image_size[0])/2)
            self.image_start_y = int((self.the_canvas_maximum_height-self.image_size[1])/2)
            start_place = (self.image_start_x,self.image_start_y)
            self.fractal_pic = ImageTk.PhotoImage(the_picture)
            if len(self.image_memory) > 1:
                del(self.image_memory[0])
            self.image_memory.append(self.fractal_pic) #to keep the canvas from flashing whenever a new image is loaded
            self.the_canvas.create_image(start_place, anchor="nw", image=self.fractal_pic, tag="fractal")
            if not start_fresh:
                try: self.the_canvas.tag_raise(self.rect)
                except: pass
            else:
                self.the_canvas.delete(self.rect)
        else:
            self.image_start_x = 0
            self.image_start_y = 0
            self.image_size = self.the_canvas_max_dimensions
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
        self.rect_start_x = event.x
        self.rect_start_y = event.y
        self.rect = self.the_canvas.create_rectangle(self.x, self.y, 1, 1, dash=(3,2), width=2, outline="gray", tag="rectangle")
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
        self.parent.main_window.zoom_from_rectangle(zoom_out=self.parent.main_window.zoom_out_check.get())
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
        self.parent.main_window.zoom_from_rectangle(zoom_out=self.parent.main_window.zoom_out_check.get())
