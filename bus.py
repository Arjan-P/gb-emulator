import ram
import vram
import ports
import rom
import hram
import ppu
import cpu

class Bus:
    def __init__(self):
        self.ppu=ppu.PPU()
        self.cpu=cpu.CPU()
        self.ppu.connectBus(self)
        self.cpu.connectBus(self)
        self.ram = ram.RAM()
        self.vram = vram.VRAM()
        self.io = ports.IO()
        self.hram = hram.HRAM()
        super().__init__()

    def read(self,addr,byte=1):
        '''
        0000-3FFF   16KB ROM Bank 00     (in cartridge, fixed at bank 00)
        4000-7FFF   16KB ROM Bank 01..NN (in cartridge, switchable bank number)
        8000-9FFF   8KB Video RAM (VRAM) (switchable bank 0-1 in CGB Mode)
        A000-BFFF   8KB External RAM     (in cartridge, switchable bank, if any)
        C000-CFFF   4KB Work RAM Bank 0 (WRAM)
        D000-DFFF   4KB Work RAM Bank 1 (WRAM)  (switchable bank 1-7 in CGB Mode)
        E000-FDFF   Same as C000-DDFF (ECHO)    (typically not used)
        FE00-FE9F   Sprite Attribute Table (OAM)
        FEA0-FEFF   Not Usable
        FF00-FF7F   I/O Ports
        FF80-FFFE   High RAM (HRAM)
        FFFF        Interrupt Enable Register
        '''
        
        if addr >= 0x0000 and addr<= 0x3fff:
            return self.rom.read(addr,byte)
        
        elif addr >= 0x8000 and addr <= 0x9fff:
            return self.vram.read(addr,byte)
        
        elif addr >= 0xc000 and addr <= 0xdfff:
            return self.ram.read(addr,byte)
        # OAM Ram
        elif addr >= 0xff00 and addr <= 0xff7f:
            if addr >= 0xff40 and addr <= 0xff49:
                return self.ppu.read(addr)
            return self.io.read(addr,byte)
        
        elif addr >= 0xff80 and addr <= 0xfffe:
            return self.hram.read(addr,byte)
        
        else:
            pass

    def write(self,addr,data):
        '''
        0000-3FFF   16KB ROM Bank 00     (in cartridge, fixed at bank 00)
        4000-7FFF   16KB ROM Bank 01..NN (in cartridge, switchable bank number)
        8000-9FFF   8KB Video RAM (VRAM) (switchable bank 0-1 in CGB Mode)
        A000-BFFF   8KB External RAM     (in cartridge, switchable bank, if any)
        C000-CFFF   4KB Work RAM Bank 0 (WRAM)
        D000-DFFF   4KB Work RAM Bank 1 (WRAM)  (switchable bank 1-7 in CGB Mode)
        E000-FDFF   Same as C000-DDFF (ECHO)    (typically not used)
        FE00-FE9F   Sprite Attribute Table (OAM)
        FEA0-FEFF   Not Usable
        FF00-FF7F   I/O Ports
        FF80-FFFE   High RAM (HRAM)
        FFFF        Interrupt Enable Register
        '''

        if addr >= 0x8000 and addr <= 0x9fff:
            self.vram.write(addr,data)
            
        elif addr >= 0xc000 and addr <= 0xdfff:
            self.ram.write(addr,data)
        
        elif addr >= 0xff00 and addr <= 0xff7f:
            if addr >= 0xff40 and addr <= 0xff49:
                self.ppu.write(addr,data)
            self.io.write(addr,data)
        
        elif addr >= 0xff80 and addr <= 0xfffe:
            self.hram.write(addr,data)
        
        else:
            pass

    def loadRom(self,r):
        self.rom = rom.ROM()
        self.rom.load(r)

    def Clock(self):
        self.cpu.Clock()
        self.ppu.Clock()