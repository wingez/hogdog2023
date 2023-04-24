from datetime import datetime

from automation.sequencer.graph import Guard

import threading
import sys


class KeyPressedGuard(Guard):

    def __init__(self, char: str):
        super(KeyPressedGuard, self).__init__()
        self.char = char
        self.start_listen_timestamp = datetime.now()

    def initialize(self):
        self.start_listen_timestamp = datetime.now()

    def evaluate(self) -> bool:

        for key, timestamp in key_buffer:
            if key == self.char and timestamp > self.start_listen_timestamp:
                return True
        return False


key_buffer = []


def run_thread():
    while True:
        char = sys.stdin.read(1)
        key_buffer.append((char, datetime.now()))


def start():
    thread = threading.Thread(target=run_thread, daemon=True)
    thread.start()
