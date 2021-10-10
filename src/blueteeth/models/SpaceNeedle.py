from src.blueteeth.models.ESP32BluetoothTool import ESP32BluetoothTool, retry


class SpaceNeedle(ESP32BluetoothTool):

    def __init__(self, mac_addr: str, port: int = 1):
        super().__init__(mac_addr, port)

    @retry
    def single_color(self, color):
        self.socket.send("%s\n" % ((color + ",") * 40))

    @retry
    def two_split(self, color1, color2):
        self.socket.send("%s%s\n" % ((color1 + ",") * 20), (color2 + ",") * 20)

    @retry
    def brightness(self, brightness):
        self.socket.send("B%s\n" % brightness)

    @retry
    def off(self):
        self.socket.send("000000," * 40)





