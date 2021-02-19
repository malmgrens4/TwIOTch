import bluetooth

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
