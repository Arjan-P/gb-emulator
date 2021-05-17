import numpy as np

class Fetcher:
    def __init__(self,bus):
        self.states=['ReadTileId','ReadTileData0','ReadTileData1','PushToFIFO']
        self.state=None
        self.FIFO=[0]*16
        self.cycles=None
        self.bus=bus
        self.pixelData=[0]*8
        self.tileData=[0]*8
        super().__init__()
    
    def Clock(self):
        self.cycles+=1
        if self.cycles<2:
            return
        self.cycles=0
        if self.states[self.state] == 'ReadTileId':
            self.tileId = self.bus.read(self.mapAddr+np.uint16(self.tileIndex))
            self.state=1
        elif self.states[self.state] == 'ReadTileData0':
            offset=0x8000+(np.uint16(self.tileId)*16)
            addr = offset + (np.uint16(tileLine) * 2)
            data=self.bus.read(addr)
            for bitPos in range(8):
                self.pixelData[bitPos]=(data>>bitPos)&1
            self.state=2
        elif self.states[self.state] == 'ReadTileData1':
            offset=0x8000+(np.uint16(self.tileId)*16)
            addr = offset + (np.uint16(tileLine) * 2)
            data=self.bus.read(addr+1)
            for bitPos in range(8):
                self.pixelData[bitPos]=(data>>bitPos)&1
            self.state=3
        elif self.states[self.state] == 'PushToFIFO':
            if FIFO[8:]==[0]*8:
                i=7
                while i>=0:
                    self.tileData[i]=self.FIFO[i]
                self.tileIndex+=1
                self.state=0

    def start(self,tileMapRowAddr,tileLine):
        self.tileIndex=0
        self.mapAddr = tileMapRowAddr
        self.tileLine = tileLine
        self.state=0
        self.FIFO=[0]*16