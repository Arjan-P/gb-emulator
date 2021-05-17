class HRAM:
    START = 0xFF80
    END = 0xFFFE
    def __init__(self):
        self.hram = bytearray([0]*127)
        super().__init__()

    def read(self,addr,byte):
        return int.from_bytes(self.hram[addr-self.START:addr-self.START+byte],'little')

    def write(self,addr,data):
        self.hram[addr-self.START] = data
