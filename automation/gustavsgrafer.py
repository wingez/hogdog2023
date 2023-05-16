from datetime import datetime, timedelta
from typing import List

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import queue
from dataclasses import dataclass
import time
import threading
import operator
import itertools as it
import serial
from pathlib import Path
import platform

# >>> $ pip install matplotlib pyserial


DATA_KEEP_SECONDS = 200

ROWS = 3
COLS = 3

BAUDRATE = 115200

device = ''  # set to specific com-port, '/dev/ttyACM0' 'COM3' etc...

if not device:
    for i in range(0, 3):
        device = f'/dev/ttyACM{i}'
        if Path(device).exists():
            break
    else:
        raise RuntimeError("serial-port not set")

print("Selected serial port:", device)


@dataclass
class Event:
    channel: str
    time: float
    value: float


event_queue = queue.Queue()


def func():
    arduino = serial.Serial(port=device, baudrate=BAUDRATE)

    while True:
        try:
            data = b''
            while b'\n' not in data:
                data += arduino.readline()
            data = data.decode('ascii')

            def valid(c):
                if c.isalnum():
                    return True
                if c in ['.', ':', '-']:
                    return True
                return False

            data = ''.join(filter(valid, data))

            if not all([valid(c) for c in data]):
                raise AssertionError("fghjk")

            # print("receved: ", data)
            if ":" in data:
                now = datetime.now().timestamp()

                datas = data.strip().split(" ")

                for data in datas:
                    channel, data_str = data.split(':')
                    event = Event(channel, now, float(data_str))

                    # print("putting data")
                    event_queue.put(event)
        except Exception as e:
            print(e)
            continue


class DataCollector:
    def __init__(self):
        self.fig, axis = plt.subplots(3, 3)
        self.unused_axis = list(it.chain.from_iterable(axis.tolist()))
        print(self.unused_axis)
        self.ax_map = {}
        plt.title("Grupp 1s")

        self.data: List[Event] = []

    def fetch_data(self):
        print("fetching")
        while not event_queue.empty():
            # print("found data")
            item = event_queue.get_nowait()
            channel = item.channel
            if channel not in self.ax_map:
                if not self.unused_axis:
                    raise AssertionError("channel", repr(channel))
                newchannel = self.unused_axis.pop()
                print("new channel:", newchannel, repr(channel))
                self.ax_map[channel] = newchannel

            self.data.append(item)

    def discard_old_data(self):

        discard = (datetime.now() - timedelta(seconds=DATA_KEEP_SECONDS)).timestamp()
        self.data = list(filter(lambda i: i.time > discard, self.data))

    def update(self, i):
        print("tick")
        # Add x and y to lists

        self.fetch_data()
        self.discard_old_data()

        for channel, ax in self.ax_map.items():
            time = [data.time for data in self.data if data.channel == channel]
            values = [data.value for data in self.data if data.channel == channel]
            # Draw x and y lists
            ax.clear()
            ax.plot(time, values)
            ax.set(title=channel)

        # Format plot
        # plt.xticks(rotation=45, ha='right')
        # plt.subplots_adjust(bottom=0.30)
        # plt.title('TMP102 Temperature over Time')
        # plt.ylabel('Temperature (deg C)')

    def plot(self):
        ani = animation.FuncAnimation(self.fig, self.update, interval=500)
        plt.show()


t = threading.Thread(target=func, daemon=True)
t.start()
s = DataCollector()
s.plot()
