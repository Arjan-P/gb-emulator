import numpy as np
import fetcher
# Add ppu states
# add vram oam ram to ppu
# no vram access to cpu during pixel transfer
# no oam access to cpu during oam search/pixel transfer
class PPU:
    def __init__(self):
        self.cycles=0
        self.s = States()
        self.state=0
        self.states=[
                        self.s.OAMSearch,
                        self.s.PixelTransfer,
                        self.s.HBlank,
                        self.s.VBlank
                    ]
#        self.Fetcher=fetcher.Fetcher(self.bus)
        self.x=0
        super().__init__()
    
    # Registers
    ly: int   = 0
    stat: int = 0x84
    lyc: int  = 0
    scx: int  = 0
    scy: int  = 0
    bgp: int  = 0
    wx: int   = 0
    wy: int   = 0
    lcdc: int = 0
    obp0: int = 0
    obp1: int = 0
    vbk: int  = 0

    def read(self, address: int) -> int:
        if address == 0xff44:
            return self.ly
        if address == 0xff41:
            return self.stat
        if address == 0xff45:
            return self.lyc
        if address == 0xff43:
            return self.scx
        if address == 0xff42:
            return self.scy
        if address == 0xff47:
            return self.bgp
        if address == 0xff4b:
            return self.wx
        if address == 0xff4a:
            return self.wy
        if address == 0xff40:
            return self.lcdc
        if address == 0xff48:
            return self.obp0
        if address == 0xff49:
            return self.obp1

    def write(self, address: int, value: int):
        if address == 0xff44:
            self.ly = value
        elif address == 0xff41:
            self.stat = value
        elif address == 0xff45:
            self.lyc = value
        elif address == 0xff43:
            self.scx = value
        elif address == 0xff42:
            self.scy = value
        elif address == 0xff47:
            self.bgp = value
        elif address == 0xff4b:
            self.wx = value
        elif address == 0xff4a:
            self.wy = value
        elif address == 0xff40:
            self.lcdc = value
        elif address ==0xff48:
            self.obp0 = value
        elif address == 0xff49:
            self.obp1 = value

    def Clock(self):
        if self.lcdc >> 7==1:   # LCD Display on
            self.states[self.state](self)
            self.cycles+=1
        pass  

    def connectBus(self,bus):
        self.bus = bus
    
class States:
    def __init__(self):
        super().__init__()
    
    def OAMSearch(self,ppu):    #0
        print('\t\t\tOAM')
        if ppu.cycles==40:
            ppu.state=1
    
    def PixelTransfer(self,ppu):    #1
        print('\t\t\tPT')
        ppu.x+=1
        if ppu.x==160:
            ppu.state=2



    def HBlank(self,ppu):   #2
        print('HB')
        if ppu.cycles==456:
            ppu.cycles=0
            ppu.x=0
            ppu.ly+=1
            if ppu.ly==144:
                ppu.state=3
            else:
                ppu.state=0

    def VBlank(self,ppu):   #3
        print('\t\t\tVB')
        if ppu.cycles==456:
            ppu.cycles=0
            ppu.ly+=1
            if ppu.ly == 153:
                ppu.ly=0
                ppu.state=0