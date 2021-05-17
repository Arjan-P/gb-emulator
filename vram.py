class VRAM:
    START = 0x8000
    END = 0x9FFF
    def __init__(self):
        self.vram = bytearray([0]*8*1024)
        super().__init__()

    def read(self,addr,byte):
        return int.from_bytes(self.vram[addr-self.START:addr-self.START+byte],'little')

    def write(self,addr,data):
        self.vram[addr-self.START] = data