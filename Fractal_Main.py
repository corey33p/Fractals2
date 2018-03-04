from Fractal_Window import Window
import os
from tkinter import mainloop
import win32gui

class Parent:
    def __init__(self,batch=False):
        self.main_window = Window(self,batch=batch)
        if os.path.isfile(os.getcwd().replace('\\','/')+"/save/default.txt"): self.main_window.load_settings_from_file(the_file=os.getcwd().replace('\\','/')+"/save/default.txt")
        elif os.path.isfile(os.getcwd().replace('\\','/')+"/save/recent_settings.txt"): self.main_window.load_settings_from_file(the_file=os.getcwd().replace('\\','/')+"/save/recent_settings.txt")
        self.resize_CLI_window()
        mainloop()
    def resize_CLI_window(self):
        def get_windows():
            def check(hwnd, param):
                title = win32gui.GetWindowText(hwnd)
                # print("title: " + str(title))
                if 'python  -u' in title:
                    param.append(hwnd)
            winds = []
            win32gui.EnumWindows(check, winds)
            return winds
        for window in get_windows():
            win32gui.MoveWindow(window,8,0,1300,1000,True)

if __name__ == '__main__':
    Parent()
