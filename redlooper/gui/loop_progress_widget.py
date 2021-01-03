import tkinter
from tkinter.font import Font


class DialWidget(tkinter.Canvas):
    RADIUS_RATIO = 0.7

    def __init__(self, master=None, font=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.arc_id = None
        self.center_circle_id = None
        self.text_id = None

        if font:
            self.font = font
        else:
            self.font = Font(size=50)

        self.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)
        self.update()
        self.draw_()

    def set_extent(self, extent_fraction):
        extent_degrees = extent_fraction * 360.0
        self.itemconfigure(self.arc_id, extent=-extent_degrees)

    def set_center_text(self, text):
        self.itemconfigure(self.text_id, text=text)

    def draw_(self):
        center = self.winfo_width() / 2.0, self.winfo_height() / 2.0
        radius_outer = min(center)
        radius_inner = radius_outer * self.RADIUS_RATIO

        self.arc_id = self.draw_arc_(center, radius_outer, start=90, extent=0, fill='blue')
        self.center_circle_id = self.draw_oval_(center, radius_inner, fill=self['background'])
        self.text_id = self.draw_text_(center, text='')

    def draw_arc_(self, center, radius, **kwargs):
        top_left = center[0] - radius, center[1] - radius
        bottom_right = center[0] + radius, center[1] + radius
        return self.create_arc(*top_left, *bottom_right, **kwargs)

    def draw_oval_(self, center, radius, **kwargs):
        top_left = center[0] - radius, center[1] - radius
        bottom_right = center[0] + radius, center[1] + radius
        return self.create_oval(*top_left, *bottom_right, **kwargs)

    def draw_text_(self, center, text):
        return self.create_text(*center, anchor='center', text=text, font=self.font)


class TimerWidget(DialWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout_s = 0
        self.time_elapsed_s = 0

    def set_timeout(self, timeout_s):
        self.timeout_s = timeout_s
        self.update_graphics_()

    def set_time_elapsed(self, time_s):
        self.time_elapsed_s = time_s
        self.update_graphics_()

    def update_graphics_(self):
        self.set_center_text(self.get_time_elapsed_string_())
        self.set_extent(self.get_elapsed_time_fraction_())

    def get_elapsed_time_fraction_(self):
        if self.timeout_s:
            return self.time_elapsed_s / self.timeout_s
        else:
            return 0

    def get_time_elapsed_string_(self):
        return self.format_time_(self.time_elapsed_s)

    @staticmethod
    def format_time_(seconds):
        minutes = int(seconds / 60)
        seconds = int(seconds % 60)
        return '%.2d:%.2d' % (minutes, seconds)


class LoopProgressWidget(TimerWidget):
    def set_loop_position(self, loop_position_s):
        self.set_time_elapsed(loop_position_s)

    def set_loop_length(self, loop_length_s):
        self.set_timeout(loop_length_s)
