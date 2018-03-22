from Fractal_Window import Window
from Fractal_Fractal import Fractal, Colorizer
import os
from tkinter import mainloop
import win32gui
import multiprocessing
import threading
import time
import copy
from PIL import Image
from queue import Queue

class Parent:
    def __init__(self,batch=False):
        self.main_window = Window(self,batch=batch)
        if os.path.isfile(os.getcwd().replace('\\','/')+"/save/default.txt"): self.main_window.load_settings_from_file(the_file=os.getcwd().replace('\\','/')+"/save/default.txt")
        elif os.path.isfile(os.getcwd().replace('\\','/')+"/save/recent_settings.txt"): self.main_window.load_settings_from_file(the_file=os.getcwd().replace('\\','/')+"/save/recent_settings.txt")
        self.resize_CLI_window()
        self.fractal_object = Fractal(self.main_window.GUI_settings_to_dict(),self)
        self.main_window.load_default_settings()
        self.fractal_colorizer = Colorizer(self.fractal_object.settings)
        
        self.process_queue = Queue()
        board_animator_thread = threading.Thread(target=self.main_queue)
        board_animator_thread.daemon = True
        board_animator_thread.start()
        mainloop()
    def main_queue(self):
        while True:
            time.sleep(.01)
            if not self.process_queue.empty():
                next_action = self.process_queue.get(False)
                next_action()
    def resize_CLI_window(self):
        def get_windows():
            def check(hwnd, param):
                title = win32gui.GetWindowText(hwnd)
                # print("title: " + str(title))
                if 'python  -u' in title:
                    param.append(hwnd)
            wind = []
            win32gui.EnumWindows(check, wind)
            return wind
        self.cli_handles = get_windows()
        for window in self.cli_handles:
            win32gui.MoveWindow(window,8,0,1300,1000,True)
    def colorize_process_start(self):
        # print("colorize process hello")
        t = multiprocessing.Process(target = self.fractal_colorizer.colorize)
        t.daemon = True
        t.start()
        t.join()
        
        img_name = self.fractal_colorizer.settings['image_name'][1]
        if self.fractal_colorizer.iteration == 0:
            self.process_queue.put(lambda: self.canvas_object.load_new_picture(img_name,start_fresh=True))
        else:
            # print("check2")
            self.process_queue.put(lambda: self.canvas_object.load_new_picture(img_name))
        os.remove(os.getcwd().replace("\\","/") + "/temp/colorizing")
    def colorize_thread(self):
        already_colorizing = lambda: os.path.isfile(os.getcwd().replace("\\","/") + "/temp/colorizing")
        on_last_iteration = self.fractal_object.iteration == self.fractal_object.settings['iterations'][1] - 1
        if (not already_colorizing()) or on_last_iteration:
            if on_last_iteration: self.process_queue.queue.clear()
            while already_colorizing():
                # print("Waiting for image to process.")
                time.sleep(.2)
            with open("temp/colorizing", 'w'): pass
            # copy some attributes
            self.fractal_colorizer.settings = self.fractal_object.settings
            self.fractal_colorizer.iteration = self.fractal_object.iteration
            self.fractal_colorizer.orbit_trap_dict = self.fractal_object.orbit_trap_dict
            self.fractal_colorizer.OT_trap_count = self.fractal_object.OT_trap_count
            self.fractal_colorizer.main_escape_iterations = self.fractal_object.main_escape_iterations
            self.fractal_colorizer.OT_RGBs = self.fractal_object.OT_RGBs
            self.fractal_colorizer.previously_trapped = self.fractal_object.previously_trapped
            self.fractal_colorizer.OT_which_trap = self.fractal_object.OT_which_trap
            self.fractal_colorizer.OT_escape_iterations = self.fractal_object.OT_escape_iterations
            self.fractal_colorizer.escape_distance = self.fractal_object.escape_distance
            self.fractal_colorizer.packed_settings = self.fractal_object.packed_settings
            self.fractal_colorizer.orbit_trap_list = self.fractal_object.orbit_trap_list
            #
            self.t = threading.Thread(target = lambda: self.colorize_process_start())
            self.t.daemon = True
            self.t.start()
    def start_fractal(self):
        self.process_queue.queue.clear()
        self.process_queue.put(lambda: self.fractal_object.setup_fractal())
        self.process_queue.put(lambda: self.fractal_object.iterate_fractal())
if __name__ == '__main__':
    Parent()
