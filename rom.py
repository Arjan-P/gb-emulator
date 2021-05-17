class ROM:
    START=0x0000
    END = 0x3FFF
    rom=[]
    def __init__(self, *args, **kwargs):
        with open('./ROMS/DMG_ROM.bin','rb') as f:
            self.rom.append(f.read())
        return super().__init__(*args, **kwargs)

    def load(self,r:bytes):
        self.rom[0]+=r

    def read(self,addr,byte):
        return int.from_bytes(self.rom[0][addr-self.START:addr-self.START+byte],'little')