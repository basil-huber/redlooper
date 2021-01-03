import tkinter


class MainWindow(tkinter.Frame):
    def __init__(self, fullscreen=True, **kwargs):
        super().__init__(**kwargs)
        self.show_cursor(False)
        self.set_fullscreen(fullscreen)
        self.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

    def set_fullscreen(self, fullscreen):
        self.master.attributes("-fullscreen", fullscreen)

    def show_cursor(self, show):
        if show:
            self.config(cursor='')
        else:
            self.config(cursor='none')
