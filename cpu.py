import opcodes
import registers

class CPU:
    def __init__(self):
        self.registers = registers.Registers()
        self.cycles=0
        self.pre=False
        self.running=True
        super().__init__()

    def connectBus(self,bus):
        self.bus=bus

    def log(self,logging=False):
        if logging:
            print(f'AF:\t{hex(self.registers.bytes_to_byte([self.registers.a_reg,self.registers.f_reg])).upper()}')
            print(f'BC:\t{hex(self.registers.bytes_to_byte([self.registers.b_reg,self.registers.c_reg])).upper()}')
            print(f'DE:\t{hex(self.registers.bytes_to_byte([self.registers.d_reg,self.registers.e_reg])).upper()}')
            print(f'HL:\t{hex(self.registers.bytes_to_byte([self.registers.h_reg,self.registers.l_reg])).upper()}')
            print(f'PC:\t{hex(self.registers.pc_reg).upper()}')
            print(f'SP:\t{hex(self.registers.sp_reg).upper()}')

    def Clock(self):
        op = opcodes.Opcodes()
        self.log(True)
        if self.cycles == 0:
            code = hex(self.bus.read(self.registers.pc_reg))
            if self.pre:
                print(f'{code}',end='\t')
                op.extended_opcodes[code](self)
                self.pre=False
            else:
                if code == '0xcb':
                    self.registers.pc_reg+=1
                    print(f'{code}')
                    self.pre=True
                    self.cycles+=1
                else:
                    print(f'{code}',end='\t')
                    op.opcodes[code](self)
        self.cycles-=1
