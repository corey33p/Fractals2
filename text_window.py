from tkinter import Text
class TextWriter(object):
    def __init__(self, text_widget, center=False):
        self.text_widget = text_widget
        self.center = center
        if center: self.text_widget.tag_configure("center", justify='center')
        self.index_before_last_print = ""
        self.last_was_overwrite = False
        self.write(" ")
        self.flush = lambda: True
        if center: self.text_widget.tag_add("center", 1.0, "end")
    def write(self, the_string):
        self.text_widget.configure(state="normal")
        if self.last_was_overwrite: self.text_widget.insert("end", "\n")
        self.index_before_last_print = self.text_widget.index("end")
        self.text_widget.insert("end", the_string)
        self.text_widget.configure(state="disabled")
        self.last_was_overwrite = False
        self.text_widget.see("end")
        if self.center: self.text_widget.tag_add("center", 1.0, "end")
    def overwrite(self, the_string):
        self.text_widget.configure(state="normal")
        self.text_widget.delete(self.index_before_last_print + "-1c linestart", "end")
        # use this next line if and only if you're on windows. EOL nuance...
        self.text_widget.insert("end", "\n")
        #
        self.index_before_last_print = self.text_widget.index("end")
        self.text_widget.insert("end", the_string)
        self.text_widget.configure(state="disabled")
        self.last_was_overwrite = True
        self.text_widget.see("end")
        if self.center: self.text_widget.tag_add("center", 1.0, "end")
