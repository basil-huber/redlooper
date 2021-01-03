import tkinter


class MainWindow(tkinter.Frame):
    def __init__(self, fullscreen=True, **kwargs):
        super().__init__(**kwargs)
        if fullscreen:
            self.master.attributes("-fullscreen", True)
        self.pack()
