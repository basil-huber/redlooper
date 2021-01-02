from .gpio_button import GPIOButton


class PyPedal:
    GPIO_BUTTON_LEFT = 17
    GPIO_BUTTON_RIGHT = 27

    def __init__(self):
        self.button_left = GPIOButton(self.GPIO_BUTTON_LEFT)
        self.button_right = GPIOButton(self.GPIO_BUTTON_RIGHT)
