from redlooper import Looper, PyPedal
from redlooper.gui import MainWindow, LoopProgressWidget
from threading import Event
import time

def main():
    window = MainWindow()
    lpw = LoopProgressWidget(window)

    looper_connected_event = Event()
    def looper_connected():
        looper_connected_event.set()
        print('Looper connected!!!!!!!!!!!!!!')

    pedal = PyPedal()

    try:
        with Looper(on_connected=looper_connected) as looper:
            #######################################
            # wait for looper and pedal connected #
            #######################################
            looper_connected_event.wait()

            ###########################
            # Connect buttons to looper #
            ###########################
            def button_left_released():
                print('left released')
                # looper_state = looper.get_state()
                # if looper_state in [Looper.State.MUTED_OFF, Looper.State.OFF, Looper.State.UNKNOWN,
                #                     Looper.State.RECORDING]:
                looper.record()
                # else:
                #     looper.multiply()

            def button_left_released_long():
                print('left released LONG')
                looper.undo()

            def button_right_released():
                print('right released')
                looper.mute()

            def button_right_released_long():
                print('right released LONG')
                looper.reset()

            def state_changed_callback(state):
                if state == Looper.State.RECORDING:
                    lpw.set_mode(lpw.Mode.PULSING)
                else:
                    window.set_mode(lpw.Mode.FILLING)

            pedal.button_left.set_callback_released(button_left_released)
            pedal.button_left.set_callback_released_long(button_left_released_long)
            pedal.button_right.set_callback_released(button_right_released)
            pedal.button_right.set_callback_released_long(button_right_released_long)

            looper.set_loop_position_update_callback(lpw.set_loop_position)
            looper.set_loop_length_update_callback(lpw.set_loop_length)
            looper.set_state_callback(state_changed_callback)

            ###########################
            #       Main loop         #
            ###########################
            window.mainloop()
    finally:
        pass


if __name__ == '__main__':
    main()

