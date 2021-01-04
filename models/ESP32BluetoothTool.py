import bluetooth


class ESP32BluetoothTool:
    mac_addr = ''
    socket = ''
    port = 1

    def __init__(self, mac_addr, port=1):
        self.mac_addr = mac_addr
        self.port = port
        self._connect_socket()

    def _connect_socket(self):
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.connect((self.mac_addr, self.port))

    def close_socket(self):
        self.socket.close()
