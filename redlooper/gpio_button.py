from RPi import GPIO
import time


class GPIOButton:
    BOUNCE_TIME = 70   # [ms]
    LONG_PRESS_TIME = 3  # [s]

    def __init__(self, gpio_bcm, callback_pressed=None, callback_released=None, callback_released_long=None):
        self.is_pressed = False
        self.trigger_time = 0
        self.callback_pressed = callback_pressed
        self.callback_released = callback_released
        self.callback_released_long = callback_released_long
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_bcm, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(gpio_bcm, GPIO.BOTH, callback=self.gpio_callback_, bouncetime=self.BOUNCE_TIME)

    def set_callback_pressed(self, callback_pressed):
        self.callback_pressed = callback_pressed

    def set_callback_released(self, callback_released):
        self.callback_released = callback_released

    def set_callback_released_long(self, callback_released_long):
        self.callback_released_long = callback_released_long

    def gpio_callback_(self, channel):
        self.is_pressed = GPIO.input(channel) == GPIO.HIGH
        if not self.is_pressed:
            if self.is_long_press_():
                func = self.callback_released_long
            else:
                func = self.callback_released
        else:
            func = self.callback_pressed
        self.trigger_time = time.time()
        if func:
            func()

    def is_long_press_(self):
        dt = time.time() - self.trigger_time
        print(dt)
        return dt >= self.LONG_PRESS_TIME
