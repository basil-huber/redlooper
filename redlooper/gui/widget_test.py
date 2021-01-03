from redlooper.gui.loop_progress_widget import LoopProgressWidget
from redlooper.gui.main_window import MainWindow
from tkinter import *
import time
import threading

print('hallo')
window = MainWindow()
lpw = LoopProgressWidget(master=window, width=200, height=300)


def update():
    loop_len = 200
    lpw.set_loop_length(loop_len)
    while True:
        for i in range(0, loop_len):
            print('loopi')
            lpw.set_loop_position(i)
            time.sleep(0.1)


th = threading.Thread(target=update)
print('starting')
th.start()
window.mainloop()
print('done')