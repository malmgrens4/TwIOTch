import bluetooth
from bluetooth import BluetoothError
import logging


def retry(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BluetoothError as err:
            logging.error("Error when calling bluetooth command.", err)
            args[0].connect_socket()
            return func(*args, **kwargs)
    return wrapper


class ESP32BluetoothTool:
    mac_addr = ''
    socket = ''
    port = 1

    def __init__(self, mac_addr: str, port: int = 1):
        self.mac_addr = mac_addr
        self.port = port
        self.connect_socket()

    def connect_socket(self):
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.connect((self.mac_addr, self.port))

    def close_socket(self):
        self.socket.close()
