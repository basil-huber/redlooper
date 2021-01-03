from tkinter import Canvas, BOTH


class LoopProgressWidget(Canvas):
    RADIUS_RATIO = 0.7

    def __init__(self, master=None, width=None, height=None):
        super().__init__(master=master, width=width, height=height)
        self.arc_id = None
        self.center_circle_id = None

        self.pack()
        self.draw_(width, height)

    def set_progress(self, progress_percent):
        self.itemconfigure(self.arc_id, extent=progress_percent / -100 * 360.0)

    def draw_(self, width, height):
        radius_outer = min(width, height)/2.0
        radius_inner = radius_outer * self.RADIUS_RATIO
        center = width/2, height/2
        self.arc_id = self.draw_arc_(center, radius_outer, start=90, extent=0, fill='blue')
        self.center_circle_id = self.draw_oval_(center, radius_inner, fill=self['background'])

    def draw_arc_(self, center, radius, **kwargs):
        top_left = center[0] - radius, center[1] - radius
        bottom_right = center[0] + radius, center[1] + radius
        return self.create_arc(*top_left, *bottom_right, **kwargs)

    def draw_oval_(self, center, radius, **kwargs):
        top_left = center[0] - radius, center[1] - radius
        bottom_right = center[0] + radius, center[1] + radius
        return self.create_oval(*top_left, *bottom_right, **kwargs)
