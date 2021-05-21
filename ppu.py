import numpy as np
import sdl2
import os
# Add ppu states
# add vram oam ram to ppu
# no vram access to cpu during pixel transfer
# no oam access to cpu during oam search/pixel transfer
class PPU:
    def __init__(self):
        self.fetcher=None
        self.display=Display()
        self.tileData = [0x8800,0x8000]
        self.tileMap = [0x9800,0x9c00]
        self.state=0
        self.cycles=0
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
            #print(self.scx,self.scy,self.ly)
            #print(self.scy)
            if self.state==0:
                if self.cycles==20:
                    self.x=0
                    tileLine = (self.ly+self.scy)%8
                    mapRow = (int((self.ly+self.scy)/8))*32
                    tileIndexAddr=self.tileMap[(self.lcdc>>3)&1]+mapRow
                    tileDataOffset=self.tileData[(self.lcdc>>4)&1]

                    self.fetcher.Start(tileIndexAddr,tileDataOffset,tileLine)
                    self.state=1

            elif self.state==1:
                self.fetcher.Clock()
                #print((self.fetcher.FIFO))
             
     
                if len(self.fetcher.FIFO) >= 8:
           
                        
                    self.display.write(self.fetcher.FIFO[0],self.lcdc)
                    del(self.fetcher.FIFO[0])

                self.x+=1
                if self.x==160:
                    self.display.HBlank()
                    self.state=2

            elif self.state==2:
                if self.cycles==456:
                    self.cycles=0
                    self.x=0
                    self.ly+=1
                    if self.ly==144:
                        self.display.VBlank()
                        self.state=3
                    else:
                        self.state=0 
            else:
                if self.cycles==456:
                    self.cycles=0
                    self.ly+=1
                    if self.ly == 153:
                        self.ly=0
                        self.state=0
            self.cycles+=1
        pass  

    def connectBus(self,bus):
        self.bus = bus
        self.fetcher = Fetcher(bus)

class Fetcher:
    def __init__(self,bus):
        self.bus=bus
        self.cycles=0
        self.state=0
        self.indexAddr=0
        self.tileLine=0
        self.tileDataOffset=0
        self.pixelData=[[0]*8,[0]*8]
        self.FIFO=[]
    
        super().__init__()

    def Start(self,tileIndexAddr,tileDataOffset,tileLine):
        self.tileIndex=0
        self.indexAddr=tileIndexAddr
        self.tileDataOffset=tileDataOffset
        self.tileLine=tileLine

    def Clock(self):
        self.cycles+=1
        if self.cycles<2:
            return 
        self.cycles=0
        if self.state==0:
            # Read Tile Index number from bg map
            self.tileId=self.bus.read(int(self.indexAddr)+self.tileIndex)
            self.tileIndex+=1
            self.state=1

        elif self.state==1:
            # Read First byte of Pixel Data
            t=self.tileDataOffset+(self.tileId*16)
            
            b1=self.bus.read(t+self.tileLine*2)
            
            for bit in range(8):
                self.pixelData[1][bit]=(b1>>(7-bit))&1
      
        
            self.state=2
        
        elif self.state==2:
            # Read Second Byte of Pixel Data
            t=self.tileDataOffset+(self.tileId*16)
            b1=self.bus.read(t+self.tileLine*2+1)
            
            for bit in range(8):
                self.pixelData[0][bit]=(b1>>(7-bit))&1

            self.state=3
        
            
        
        elif self.state==3:
            # Push to FIFO
            if len(self.FIFO)==0:
                for x in range(8):
                    self.FIFO.append((self.pixelData[1][x],self.pixelData[0][x]))  
                self.state=0
            if len(self.FIFO)<=8:
                for x in range(8):
                    self.FIFO.append((self.pixelData[1][x],self.pixelData[0][x]))                
                self.state=0
class Display:
    def __init__(self):
        
        self.palette=[
            [0xe0, 0xf0, 0xe7, 0xff],
            [0x8b, 0xa3, 0x94, 0xff],
            [0x55, 0x64, 0x5a, 0xff],
            [0x34, 0x3d, 0x37, 0xff]
        ]
        self.offset=0
        self.window=sdl2.SDL_CreateWindow(b'',sdl2.SDL_WINDOWPOS_UNDEFINED,sdl2.SDL_WINDOWPOS_UNDEFINED,160*2,144*2,sdl2.SDL_WINDOW_SHOWN)
        self.renderer=sdl2.SDL_CreateRenderer(self.window,-1,sdl2.SDL_RENDERER_ACCELERATED)
        self.texture=sdl2.SDL_CreateTexture(self.renderer,np.uint32(sdl2.SDL_PIXELFORMAT_RGBA32),sdl2.SDL_TEXTUREACCESS_STREAMING,160,144)
        self.buffer=bytearray(160*144*4)
        super().__init__()
    
    def write(self,color,lcdc):
        colorIndex={((lcdc>>1)&1,(lcdc>>0)&1):0,((lcdc>>3)&1,(lcdc>>2)&1):1,((lcdc>>5)&1,(lcdc>>4)&1):2,((lcdc>>7)&1,(lcdc>>6)&1):3}
        self.buffer[self.offset+0]=self.palette[colorIndex[color]][0] # R
        self.buffer[self.offset+1]=self.palette[colorIndex[color]][1] # G
        self.buffer[self.offset+2]=self.palette[colorIndex[color]][2] # B
        self.buffer[self.offset+3]=self.palette[colorIndex[color]][3] # A
        self.offset+=4

    def HBlank(self):
        pass

    def VBlank(self):
        self.offset=0
        #print(self.buffer)
        sdl2.SDL_UpdateTexture(self.texture,None,bytes(self.buffer),int(160*4))
        sdl2.SDL_RenderCopy(self.renderer,self.texture,None,None)
        sdl2.SDL_RenderPresent(self.renderer)