from redlooper.gui.loop_progress_widget import LoopProgressWidget
from redlooper.gui.main_window import MainWindow
from tkinter import *
import time
import threading

print('hallo')
window = MainWindow(fullscreen=True)
lpw = LoopProgressWidget(master=window)


def update():
    loop_len = 200
    lpw.set_mode(lpw.Mode.PULSING)
    lpw.set_loop_length(loop_len)
    while True:
        for i in range(0, loop_len*100):
            lpw.set_loop_position(i/100.0)
            time.sleep(0.01)


th = threading.Thread(target=update)
print('starting')
th.start()
window.mainloop()
print('done')