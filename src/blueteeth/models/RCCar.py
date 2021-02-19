from src.blueteeth.models.ESP32BluetoothTool import ESP32BluetoothTool, retry


class RCCar(ESP32BluetoothTool):

    def __init__(self, mac_addr: str, port: int = 1):
        super().__init__(mac_addr, port)

    @retry
    def forward(self, duration):
        self.socket.send("F%s\n" % duration)

    @retry
    def backward(self, duration):
        self.socket.send("B%s\n" % duration)

    @retry
    def left(self, duration):
        self.socket.send("L%s\n" % duration)

    @retry
    def right(self, duration):
        self.socket.send("R%s\n" % duration)

    @retry
    def light_on(self):
        self.socket.send("D1")

    @retry
    def light_off(self):
        self.socket.send("D-1")





