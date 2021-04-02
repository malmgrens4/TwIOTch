from src.blueteeth.models.ESP32BluetoothTool import ESP32BluetoothTool, retry


class BalloonBox(ESP32BluetoothTool):

    def __init__(self, mac_addr: str, port: int = 1):
        super().__init__(mac_addr, port)

    @retry
    def left_pump(self, duration):
        self.socket.send(f"L{duration}\n")

    @retry
    def right_pump(self, duration):
        self.socket.send(f"R{duration}\n")

    @retry
    def all_pumps(self, duration):
        self.socket.send(f"L{duration}R{duration}\n")
