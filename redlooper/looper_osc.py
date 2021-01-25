import liblo
from threading import Event
from enum import Enum
import subprocess
import jack
from time import sleep
import threading
import logging


class Looper:
    class State(Enum):
        UNKNOWN = -1
        OFF = 0
        WAIT_START = 1
        RECORDING = 2
        WAIT_STOP = 3
        PLAYING = 4
        OVERDUBBING = 5
        MULTIPLYING = 6
        INSERTING = 7
        REPLACING = 8
        DELAY = 9
        MUTED = 10
        SCRATCHING = 11
        ONESHOT = 12
        SUBSTITUTE = 13
        PAUSED = 14
        MUTED_OFF = 20  # undocumented

    def __init__(self, target_ip="localhost", home_ip="localhost", home_port="9952", on_exit=None, on_connected=None):
        self.state = Looper.State.UNKNOWN
        self.ping_event = Event()
        self.state_event = Event()

        # callbacks
        self.state_callback = None
        self.loop_position_update_callback = None
        self.loop_length_update_callback = None
        self.on_connected = on_connected

        # OSC client and server
        self.home_server = liblo.ServerThread(home_port)
        self.target = liblo.Address(target_ip, "9951")
        self.home_url = home_ip + ":" + home_port
        self.home_server.add_method("/state", "isf", self.receive_state, self)
        self.home_server.add_method("/ping", None, self.receive_ping, self)
        self.home_server.add_method("/loop_len", None, self.receive_loop_len, self)
        self.home_server.add_method("/loop_pos", None, self.receive_loop_pos, self)
        self.loop_count = 1

        self.loop_len = 0
        self.loop_pos = 0

        # Sooperlooper process
        self.sooperlooper = SooperLooper(gui=False, on_exit=on_exit)

        # jackd
        self.jack = None

    def __enter__(self):
        self.start_jack()
        self.sooperlooper.start()
        self.connect_jack()
        self.connect()
        self.register_state_update()
        self.register_loop_progress_update()
        return self

    def __exit__(self, *exc):
        # terminate slgui
        self.sooperlooper.terminate()
        # try to shutdown sooperlooper politely
        self.quit()
        self.stop_jack()

    def start_jack(self):
        self.jack = jack.Client("BlueLooper")
        self.jack.activate()

    def stop_jack(self):
        self.jack.deactivate()
        self.jack.close()

    def connect_jack(self):
        # wait for all jack ports to be there
        port_list = ['system:capture_1', 'system:capture_2',
                     'system:playback_1', 'system:playback_2',
                     'sooperlooper:loop0_in_1', 'sooperlooper:loop0_in_2',
                     'sooperlooper:loop0_out_1', 'sooperlooper:loop0_out_2']
        for port_name in port_list:
            while not self.jack.get_ports(port_name):
                sleep(0.1)

        # connect ports
        self.jack.connect('system:capture_1', 'sooperlooper:loop0_in_1')
        self.jack.connect('system:capture_2', 'sooperlooper:loop0_in_2')
        self.jack.connect('sooperlooper:loop0_out_1', 'system:playback_1')
        self.jack.connect('sooperlooper:loop0_out_2', 'system:playback_2')

    def connect(self, timeout=None):
        logging.info('sooperlooper starting')
        self.home_server.start()
        logging.info('pinignig')
        while True:
            if self.ping(timeout):
                break

        if self.on_connected:
            self.on_connected()

        self.request_state()

    def register_state_update(self):
        liblo.send(self.target, "/sl/-1/register_auto_update", "state", 100, self.home_url, "/state")

    def register_loop_progress_update(self):
        liblo.send(self.target, "/sl/-1/register_auto_update", "loop_len", 100, self.home_url, "/loop_len")
        liblo.send(self.target, "/sl/-1/register_auto_update", "loop_pos", 100, self.home_url, "/loop_pos")

    def set_state_callback(self, callback):
        self.state_callback = callback

    def set_loop_position_update_callback(self, callback):
        self.loop_position_update_callback = callback

    def set_loop_length_update_callback(self, callback):
        self.loop_length_update_callback = callback

    def send_sldown(self, command):
        liblo.send(self.target, "/sl/-1/down", command)

    def record(self):
        self.send_sldown("record")

    def pause(self):
        self.send_sldown("pause")

    def overdub(self):
        self.send_sldown("overdub")

    def multiply(self):
        self.send_sldown("multiply")

    def undo(self):
        self.send_sldown("undo")

    def mute(self):
        self.send_sldown("mute")

    def reset(self):
        liblo.send(self.target, "/loop_del", -1)
        self.add_loop()
        self.loop_count = 1

    def set_threshold(self, threshold):
        liblo.send(self.target, "/sl/-1/set", "rec_thresh", threshold)

    def ping(self, timeout=20):
        self.ping_event.clear()
        liblo.send(self.target, "/ping", self.home_url, "/ping")
        return self.ping_event.wait(timeout)

    def quit(self):
        liblo.send(self.target, "/quit")

    def add_loop(self):
        liblo.send(self.target, "/loop_add", 2, 50)
        self.loop_count = self.loop_count + 1

    def get_state(self):
        return self.state

    def request_state(self, timeout=1):
        self.state_event.clear()
        liblo.send(self.target, "/sl/-1/get", "state", self.home_url, "/state")
        self.state_event.wait(timeout)
        return self.state

    def receive_state(self, path, answer):
        try:
            self.state = Looper.State(answer[2])
        except ValueError:
            self.state = Looper.State.UNKNOWN
        self.state_event.set()
        if self.state_callback:
            self.state_callback(self.state)

    def receive_loop_len(self, path, answer):
        self.loop_len = answer[2]
        if self.loop_length_update_callback:
            self.loop_length_update_callback(self.loop_len)

    def receive_loop_pos(self, path, answer):
        self.loop_pos = answer[2]
        if self.loop_position_update_callback:
            self.loop_position_update_callback(self.loop_pos)

    def receive_ping(self, path, answer):
        self.ping_event.set()


class SooperLooper(threading.Thread):

    def __init__(self, gui=True, on_exit=None):
        super().__init__()
        self.gui = gui
        self.on_exit = on_exit
        self.process = None

    def run(self):
        if self.gui:
            self.process = subprocess.Popen("slgui")
        else:
            self.process = subprocess.Popen("sooperlooper")
        self.process.communicate()
        if self.on_exit:
            self.on_exit()

    def terminate(self):
        self.process.terminate()
