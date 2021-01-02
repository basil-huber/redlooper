from redlooper import Looper, PyPedal
from threading import Event
import time

# def button_callback(looper, pedal, button_id, button_state):
#     looper_state = looper.get_state()
#     if button_id == 0:
#         if button_state == BluePedal.RELEASED:
#             if looper_state in [Looper.State.MUTED_OFF, Looper.State.OFF, Looper.State.UNKNOWN, Looper.State.RECORDING]:
#                 looper.record()
#             else:
#                 looper.multiply()
#         elif button_state == BluePedal.RELEASED_LONG:
#             looper.undo()
#     elif button_id == 1:
#         if button_state == BluePedal.RELEASED:
#             looper.mute()
#         elif button_state == BluePedal.RELEASED_LONG:
#             looper.reset()


def set_event(event):
    """Callback for looper connected: set event"""
    event.set()


def main():
    looper_connected_event = Event()

    def looper_connected():
        looper_connected_event.set()
        print('Looper connected!!!!!!!!!!!!!!')

    pedal = PyPedal()

    try:
        ###########################
        # Set up looper and pedal #
        ###########################
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

            pedal.button_left.set_callback_released(button_left_released)
            pedal.button_left.set_callback_released_long(button_left_released_long)
            pedal.button_right.set_callback_released(button_right_released)
            pedal.button_right.set_callback_released_long(button_right_released_long)

            ###########################
            #       Main loop         #
            ###########################
            while looper.sooperlooper.is_alive():
                time.sleep(1)
    finally:
        pass


if __name__ == '__main__':
    main()

