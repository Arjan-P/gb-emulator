import numpy as np

class Registers:
    def __init__(self, *args, **kwargs):
        '''
        F register bits
        0   0   0   0   0   0   0   0
        ^   ^   ^   ^
        Z   N   H   C  
        '''
        self.a_reg = 0
        self.f_reg = 0
        self.b_reg = 0
        self.c_reg = 0
        self.d_reg = 0
        self.e_reg = 0
        self.h_reg = 0
        self.l_reg = 0
        self.sp_reg = 0
        self.pc_reg = 0
        return super().__init__(*args, **kwargs)
    
    def Set(self,flag):
        if flag == 'z':
            self.f_reg|=1<<7
        elif flag == 'n':
            self.f_reg|=1<<6
        elif flag == 'h':
            self.f_reg|=1<<5
        elif flag == 'c':
            self.f_reg|=1<<4
        else:
            pass
    
    def Clear(self,flag):
        if flag == 'z':
            self.f_reg&=~(1<<7)
        elif flag == 'n':
            self.f_reg&=~(1<<6)
        elif flag == 'h':
            self.f_reg&=~(1<<5)
        elif flag == 'c':
            self.f_reg&=~(1<<4)
        else:
            pass

    def isSet(self,flag):
        if flag == 'z':
            return bool((self.f_reg>>7)&1)
        elif flag == 'n':
            return bool((self.f_reg>>6)&1)
        elif flag == 'h':
            return bool((self.f_reg>>5)&1)
        elif flag == 'c':
            return bool((self.f_reg>>4)&1)
        else:
            pass   
        
    def inc(self,regPair,val):
        res=np.uint16((regPair[0]<<8)+regPair[1]+val)
        return [(res>>8)&0xff,res&0xff]

    def dec(self,regPair,val):
        res=np.uint16((regPair[0]<<8)+regPair[1]-val)
        return [(res>>8)&0xff,res&0xff]

    def bytes_to_byte(self,Bytes):
        return (Bytes[0]<<8)+Bytes[1]

    def byte_to_bytes(self,Byte):
        return [(Byte>>8)&0xff,Byte&0xff]
        