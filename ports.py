class IO:
    START = 0xFF00
    END = 0xFF7F
    def __init__(self):
        self.ports = bytearray([0]*128)
        super().__init__()

    def read(self,addr,byte):
        return int.from_bytes(self.ports[addr-self.START:addr-self.START+byte],'little')

    def write(self,addr,data):
        self.ports[addr-self.START] = data