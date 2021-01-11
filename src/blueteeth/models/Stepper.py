from src.blueteeth.models.ESP32BluetoothTool import ESP32BluetoothTool


class Stepper(ESP32BluetoothTool):
    # TODO Move this to a config file
    speed = 700

    def __init__(self, mac_addr, port=1):
        super().__init__(mac_addr, port)

    def rotate(self, direction, degrees, speed=speed):
        # TODO think about error handling that allows retry when disconnected
        self.socket.send("%s,d%s,s%s\n" % (direction.name, degrees, speed))

    def set_speed(self, speed):
        self.speed = speed

