from src.blueteeth.models.ESP32BluetoothTool import ESP32BluetoothTool


class RCCar(ESP32BluetoothTool):

    def __init__(self, mac_addr: str, port: int = 1):
        super().__init__(mac_addr, port)

    def forward(self, duration):
        self.socket.send("F%s\n" % duration)

    def backward(self, duration):
        self.socket.send("B%s\n" % duration)

    def left(self, duration):
        self.socket.send("L%s\n" % duration)

    def right(self, duration):
        self.socket.send("R%s\n" % duration)

    def light_on(self):
        self.socket.send("D1")

    def light_off(self):
        self.socket.send("D-1")

