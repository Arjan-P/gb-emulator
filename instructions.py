import numpy as np

class Instructions:
    def __init__(self):
        super().__init__()

    def log(self,msg,logging=False):
        if logging:
            print(msg)

    def x04(self,cpu):
        '''
        Increment the contents of register B by 1.
        '''
        cpu.registers.b_reg=np.uint8(1+cpu.registers.b_reg)
        if cpu.registers.b_reg == 0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        if (((cpu.registers.b_reg & 0xf) + (1 & 0xf)) & 0x10) == 0x10:
            cpu.registers.Set('h')
        else:
            cpu.registers.Clear('h')
        cpu.registers.Clear('n')
        self.log('INC B')
        cpu.cycles = 1
        cpu.registers.pc_reg+=1

    def x05(self,cpu):
        # TODO set half carry
        '''
        Decrement the contents of register B by 1
        '''
        cpu.registers.b_reg=np.uint8(cpu.registers.b_reg-1)
        if cpu.registers.b_reg == 0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        cpu.registers.Set('n')
        self.log('DEC B')
        cpu.cycles=1
        cpu.registers.pc_reg+=1

    def x06(self,cpu):
        '''
        Load the 8-bit immediate operand d8 into register B.
        '''
        data = cpu.bus.read(cpu.registers.pc_reg+1)
        cpu.registers.b_reg=data
        self.log(f'LD B {hex(data)}')
        cpu.cycles=2
        cpu.registers.pc_reg+=2

    def x0C(self,cpu):
        '''
        Increment the contents of register C by 1.
        '''
        cpu.registers.c_reg=np.uint8(1+cpu.registers.c_reg)
        if cpu.registers.c_reg == 0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        if (((cpu.registers.c_reg & 0xf) + (1 & 0xf)) & 0x10) == 0x10:
            cpu.registers.Set('h')
        else:
            cpu.registers.Clear('h')
        cpu.registers.Clear('n')
        self.log('INC C')
        cpu.cycles=1
        cpu.registers.pc_reg+=1

    def x0D(self,cpu):
        '''
        Decrement the contents of register C by 1.
        '''
        cpu.registers.c_reg=np.uint8(cpu.registers.c_reg-1)
        if cpu.registers.c_reg == 0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        cpu.registers.Set('n')
        self.log('DEC C')
        cpu.cycles=1
        cpu.registers.pc_reg+=1

    def x0E(self,cpu):
        '''
        Load the 8-bit immediate operand d8 into register C.
        '''
        data = cpu.bus.read(cpu.registers.pc_reg+1)
        cpu.registers.c_reg = data
        self.log(f'LD C {hex(data)}')
        cpu.cycles=2
        cpu.registers.pc_reg+=2

    def x11(self,cpu):
        '''
        Load the 2 bytes of immediate data into register pair DE.

        The first byte of immediate data is the lower byte (i.e., bits 0-7), and the second byte
        of immediate data is the higher byte (i.e., bits 8-15).
        '''
        data = cpu.bus.read(cpu.registers.pc_reg+1,2)
        cpu.registers.d_reg = cpu.bus.read(cpu.registers.pc_reg+2)
        cpu.registers.e_reg = cpu.bus.read(cpu.registers.pc_reg+1)
        self.log(f'LD DE {hex(data)}')
        cpu.cycles=3
        cpu.registers.pc_reg+=3
    
    def x13(self,cpu):
        '''
        Increment the contents of register pair DE by 1.
        '''
        cpu.registers.d_reg=cpu.registers.inc([cpu.registers.d_reg,cpu.registers.e_reg],1)[0]
        cpu.registers.e_reg=cpu.registers.inc([cpu.registers.d_reg,cpu.registers.e_reg],1)[1]
        self.log('INC DE')
        cpu.cycles=2
        cpu.registers.pc_reg+=1  

    def x15(self,cpu):
        '''
        Decrement the contents of register D by 1.
        '''
        cpu.registers.d_reg=np.uint8(cpu.registers.d_reg-1)
        if cpu.registers.d_reg == 0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        cpu.registers.Set('n')
        self.log('DEC D')
        cpu.cycles=1
        cpu.registers.pc_reg+=1
        cpu.running=False
        

    def x17(self,cpu):
        '''
        Rotate the contents of register C to the left. That is, the contents of bit 0 are copied
        to bit 1, and the previous contents of bit 1 (before the copy operation) are copied to bit 2.
        The same operation is repeated in sequence for the rest of the register. The previous contents
        of the carry (CY) flag are copied to bit 0 of register C.
        '''
        INT_BITS=32
        a7=cpu.registers.a_reg>>7
        cpu.registers.a_reg=np.uint8((cpu.registers.a_reg << 1)|(cpu.registers.a_reg >> (INT_BITS - 1)))
        if cpu.registers.isSet('c'):
            cpu.registers.a_reg|=1
        else:
            cpu.registers.a_reg&=~(1)
        if bool(a7):
            cpu.registers.Set('c')
        else:
            cpu.registers.Clear('c')
        if cpu.registers.a_reg==0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        cpu.registers.Clear('n')
        cpu.registers.Clear('h')
        self.log('RL A')
        cpu.cycles=1
        cpu.registers.pc_reg+=1

    def x18(self,cpu):
        '''
        Jump s8 steps from the current address in the program counter (PC). (Jump relative.)
        '''
        val = cpu.bus.read(cpu.registers.pc_reg+1)
        self.log(f'JR {hex(val)}')
        j=np.uint8(val+cpu.registers.pc_reg+2)
        cpu.cycles=3
        cpu.registers.pc_reg=j

    def x1A(self,cpu):
        '''
        Load the 8-bit contents of memory specified by register pair DE into register A.
        '''
        addr = (cpu.registers.d_reg<<8)+cpu.registers.e_reg
        data = cpu.bus.read(addr)
        cpu.registers.a_reg=data
        self.log(f'LD A ({hex(data)})')
        cpu.cycles=2
        cpu.registers.pc_reg+=1
    
    def x1D(self,cpu):
        # TODO set half carry
        '''
        Decrement the contents of register E by 1.
        '''
        cpu.registers.e_reg=np.uint8(cpu.registers.e_reg-1)
        if cpu.registers.e_reg == 0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        cpu.registers.Set('n')
        self.log('DEC E')
        cpu.cycles=1
        cpu.registers.pc_reg+=1

    def x1E(self,cpu):
        '''
        Load the 8-bit immediate operand d8 into register E.
        '''
        data = cpu.bus.read(cpu.registers.pc_reg+1)
        cpu.registers.e_reg = data
        self.log(f'LD E {hex(data)}')
        cpu.cycles=2
        cpu.registers.pc_reg+=2

    def x20(self,cpu):
        '''
        If the Z flag is 0, jump s8 steps from the current address stored in the program
        counter (PC). If not, the instruction following the current JP instruction is executed (as usual).
        '''
        if cpu.registers.isSet('z'):
            self.log('JR NZ s8')
            cpu.registers.pc_reg+=2
            cpu.cycles=2
            
        else: 
            val = cpu.bus.read(cpu.registers.pc_reg+1)
            cpu.registers.pc_reg+=2
            
            j=np.uint8(val+cpu.registers.pc_reg)
            self.log(f'JR NZ {hex(j)}')
            cpu.registers.pc_reg=j
            cpu.cycles=3
            
    def x21(self,cpu):
        '''
        Load the 2 bytes of immediate data into register pair HL.

        The first byte of immediate data is the lower byte (i.e., bits 0-7), and the second byte 
        of immediate data is the higher byte (i.e., bits 8-15).    
        '''
        data = cpu.bus.read(cpu.registers.pc_reg+1,2)
        cpu.registers.h_reg = cpu.registers.byte_to_bytes(data)[0]
        cpu.registers.l_reg = cpu.registers.byte_to_bytes(data)[1]
        self.log(f'LD HL {hex(data)}')
        cpu.cycles=3
        cpu.registers.pc_reg+=3

    def x22(self,cpu):
        '''
        Store the contents of register A into the memory location specified by register pair HL,
        and simultaneously increment the contents of HL.
        '''
        addr = (cpu.registers.h_reg<<8)+cpu.registers.l_reg
        cpu.bus.write(addr,cpu.registers.a_reg)
        cpu.registers.h_reg=cpu.registers.inc([cpu.registers.h_reg,cpu.registers.l_reg],1)[0]
        cpu.registers.l_reg=cpu.registers.inc([cpu.registers.h_reg,cpu.registers.l_reg],1)[1]
        self.log('LD (HL+) A')
        cpu.registers.pc_reg+=1
        cpu.cycles=2

    def x23(self,cpu):
        '''
        Increment the contents of register pair HL by 1.
        '''
        cpu.registers.h_reg=cpu.registers.inc([cpu.registers.h_reg,cpu.registers.l_reg],1)[0]
        cpu.registers.l_reg=cpu.registers.inc([cpu.registers.h_reg,cpu.registers.l_reg],1)[1]
        self.log('INC HL')
        cpu.registers.pc_reg+=1
        cpu.cycles=2

    def x24(self,cpu):
        '''
        Increment the contents of register H by 1.
        '''
        cpu.registers.h_reg=np.uint8(1+cpu.registers.h_reg)
        if cpu.registers.h_reg == 0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        if (((cpu.registers.h_reg & 0xf) + (1 & 0xf)) & 0x10) == 0x10:
            cpu.registers.Set('h')
        else:
            cpu.registers.Clear('h')
        cpu.registers.Clear('n')
        self.log('INC H')
        cpu.cycles=1
        cpu.registers.pc_reg+=1

    def x28(self,cpu):
        '''
        If the Z flag is 1, jump s8 steps from the current address stored in the program
        counter (PC). If not, the instruction following the current JP instruction is executed (as
        usual).
        '''
        if cpu.registers.isSet('z'):

            val = cpu.bus.read(cpu.registers.pc_reg+1)
            cpu.registers.pc_reg+=2
            cpu.cycles=3
            j=np.uint8(val+cpu.registers.pc_reg)
            self.log(f'JR Z {hex(j)}')
           
            cpu.registers.pc_reg=j             
        else: 
            self.log('JR Z s8')
            cpu.registers.pc_reg+=2
            cpu.cycles=2

    def x2E(self,cpu):
        '''
        Load the 8-bit immediate operand d8 into register L.
        '''
        data = cpu.bus.read(cpu.registers.pc_reg+1)
        cpu.registers.l_reg=data
        self.log(f'LD L {hex(data)}')
        cpu.cycles=2
        cpu.registers.pc_reg+=2

    def x31(self,cpu):
        '''
        Load the 2 bytes of immediate data into register pair SP.

        The first byte of immediate data is the lower byte (i.e., bits 0-7), and the second byte 
        of immediate data is the higher byte (i.e., bits 8-15).
        '''
        data = cpu.bus.read(cpu.registers.pc_reg+1,2)
        cpu.registers.sp_reg = data
        self.log(f'LD SP {hex(data)}')
        cpu.cycles = 3
        cpu.registers.pc_reg+=3

    def x32(self,cpu):
        '''
        Store the contents of register A into the memory location specified by register pair HL, 
        and simultaneously decrement the contents of HL.
        '''
        addr = (cpu.registers.h_reg<<8)+cpu.registers.l_reg
        cpu.bus.write(addr,cpu.registers.a_reg)
        cpu.registers.h_reg=cpu.registers.dec([cpu.registers.h_reg,cpu.registers.l_reg],1)[0]
        cpu.registers.l_reg=cpu.registers.dec([cpu.registers.h_reg,cpu.registers.l_reg],1)[1]
        self.log('LD (HL-) A')
        cpu.registers.pc_reg+=1
        cpu.cycles=2
        
    
    def x3C(self,cpu):
        '''
        Increment the contents of register A by 1.
        '''
        cpu.registers.a_reg=np.uint8(1+cpu.registers.a_reg)
        if cpu.registers.a_reg == 0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        if (((cpu.registers.a_reg & 0xf) + (1 & 0xf)) & 0x10) == 0x10:
            cpu.registers.Set('h')
        else:
            cpu.registers.Clear('h')
        cpu.registers.Clear('n')
        self.log('INC A')
        cpu.registers.pc_reg+=1
        cpu.cycles=1
    
    def x3D(self,cpu):
        '''
        Decrement the contents of register A by 1.
        '''
        cpu.registers.a_reg=np.uint8(cpu.registers.a_reg-1)
        if cpu.registers.a_reg == 0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        cpu.registers.Set('n')
        self.log('DEC A')
        cpu.registers.pc_reg+=1
        cpu.cycles=1

    def x3E(self,cpu):
        '''
        Load the 8-bit immediate operand d8 into register A.
        '''
        data = cpu.bus.read(cpu.registers.pc_reg+1)
        cpu.registers.a_reg = data
        self.log(f'LD A {hex(data)}')
        cpu.registers.pc_reg+=2
        cpu.cycles=2

    def x4F(self,cpu):
        '''
        Load the contents of register A into register C.
        '''
        cpu.registers.c_reg=cpu.registers.a_reg
        self.log('LD C A')
        cpu.registers.pc_reg+=1
        cpu.cycles=1

    def x57(self,cpu):
        '''
        Load the contents of register A into register D.
        '''
        cpu.registers.d_reg=cpu.registers.a_reg
        self.log('LD D A')
        cpu.registers.pc_reg+=1
        cpu.cycles=1

    def x67(self,cpu):
        '''
        Load the contents of register A into register H.
        '''
        cpu.registers.h_reg=cpu.registers.a_reg
        self.log('LD H A')
        cpu.registers.pc_reg+=1
        cpu.cycles=1

    def x77(self,cpu):
        '''
        Store the contents of register A in the memory location specified by register pair HL.
        '''
        addr = (cpu.registers.h_reg<<8)+cpu.registers.l_reg
        cpu.bus.write(addr,cpu.registers.a_reg)
        self.log('LD (HL) A')
        cpu.registers.pc_reg+=1
        cpu.cycles=2

    def x7B(self,cpu):
        '''
        Load the contents of register E into register A.
        '''
        cpu.registers.a_reg=cpu.registers.e_reg
        self.log('LD A E')
        cpu.registers.pc_reg+=1
        cpu.cycles=1

    def x7C(self,cpu):
        '''
        Load the contents of register H into register A.
        '''
        cpu.registers.a_reg=cpu.registers.h_reg
        self.log('LD A H')
        cpu.registers.pc_reg+=1
        cpu.cycles=1        

    def x90(self,cpu):
        '''
        Subtract the contents of register B from the contents of register A, and store the results in register A.
        '''
        cpu.registers.a_reg=np.uint8(cpu.registers.a_reg-cpu.registers.b_reg)
        if cpu.registers.a_reg==0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        if int(cpu.registers.a_reg)-int(cpu.registers.b_reg)<0:
            cpu.registers.Set('c')
        else:
            cpu.registers.Clear('c')
        cpu.registers.Set('n')
        cpu.registers.pc_reg+=1
        cpu.cycles=1


    def xAF(self,cpu):
        '''
        Take the logical exclusive-OR for each bit of the contents of register A and the 
        contents of register A, and store the results in register A.
        '''
        cpu.registers.a_reg ^= cpu.registers.a_reg
        if cpu.registers.a_reg == 0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        for x in ['n','h','c']:
            cpu.registers.Clear(x)
        self.log('XOR A')
        cpu.registers.pc_reg+=1
        cpu.cycles=1

    def xC1(self,cpu):
        '''
        Pop the contents from the memory stack into register pair into register pair BC by
        doing the following:

        ->    Load the contents of memory specified by stack pointer SP into the lower portion of BC.
        ->    Add 1 to SP and load the contents from the new memory location into the upper portion of BC.
        ->    By the end, SP should be 2 more than its initial value.
        '''
        cpu.registers.b_reg=cpu.bus.read(cpu.registers.sp_reg)
        cpu.registers.sp_reg+=1
        cpu.registers.c_reg=cpu.bus.read(cpu.registers.sp_reg)
        cpu.registers.sp_reg+=1  
        self.log('POP BC')
        cpu.registers.pc_reg+=1
        cpu.cycles=3

    def xC5(self,cpu):
        '''
        Push register pair nn onto stack.
        Decrement Stack Pointer (SP) twice.
        '''
        cpu.registers.sp_reg-=1  
        cpu.bus.write(cpu.registers.sp_reg,cpu.registers.c_reg)
        cpu.registers.sp_reg-=1
        cpu.bus.write(cpu.registers.sp_reg,cpu.registers.b_reg)

        self.log('PUSH BC')
        cpu.registers.pc_reg+=1
        cpu.cycles=4

    def xC9(self,cpu):
        '''
        Pop from the memory stack the program counter PC value pushed when the
        subroutine was called, returning contorl to the source program.

        The contents of the address specified by the stack pointer SP are loaded in the lower-
        order byte of PC, and the contents of SP are incremented by 1. The contents of the
        address specified by the new SP value are then loaded in the higher-order byte of
        PC, and the contents of SP are incremented by 1 again. (THe value of SP is 2 larger
        than before instruction execution.) The next instruction is fetched from the address
        specified by the content of PC (as usual).
        '''
        
        b1=cpu.bus.read(cpu.registers.sp_reg)
        cpu.registers.sp_reg+=1
        b2=cpu.bus.read(cpu.registers.sp_reg)
        cpu.registers.sp_reg+=1
        self.log(f'RET {hex(cpu.registers.bytes_to_byte([b1,b2]))}')
        cpu.registers.pc_reg = cpu.registers.bytes_to_byte([b1,b2])
        cpu.cycles=4

    def xCD(self,cpu):
        '''
        In memory, push the program counter PC value corresponding to the address
        following the CALL instruction to the 2 bytes following the byte specified by the
        current stack pointer SP. Then load the 16-bit immediate operand a16 into PC.

        The subroutine is placed after the location specified by the new PC value. When the
        subroutine finishes, control is returned to the source program using a return
        instruction and by popping the starting address of the next instruction (which was just
        pushed) and moving it to the PC.

        With the push, the current value of SP is decremented by 1, and the higher-order
        byte of PC is loaded in the memory address specified by the new SP value. The value of
        SP is then decremented by 1 again, and the lower-order byte of PC is loaded in the
        memory address specified by that value of SP.

        The lower-order byte of a16 is placed in byte 2 of the object code, and the higher-order
        byte is placed in byte 3.
        '''
        j = cpu.bus.read(cpu.registers.pc_reg+1,2)
        cpu.registers.sp_reg-=1        
        cpu.bus.write(cpu.registers.sp_reg,cpu.registers.byte_to_bytes(cpu.registers.pc_reg+3)[1])
        cpu.registers.sp_reg-=1
        cpu.bus.write(cpu.registers.sp_reg,cpu.registers.byte_to_bytes(cpu.registers.pc_reg+3)[0])

        cpu.registers.pc_reg=j
        self.log(f'CALL {hex(j)}')
        cpu.cycles=6

    def xE0(self,cpu):
        '''
        Store the contents of register A in the internal RAM, port register, or mode register at
        the address in the range 0xFF00-0xFFFF specified by the 8-bit immediate operand a8.

        Note: Should specify a 16-bit address in the mnemonic portion for a8, although the
        immediate operand only has the lower-order 8 bits.

        ->    0xFF00-0xFF7F: Port/Mode registers, control register, sound register
        ->    0xFF80-0xFFFE: Working & Stack RAM (127 bytes)
        ->    0xFFFF: Interrupt Enable Register
        '''
        data = cpu.bus.read(cpu.registers.pc_reg+1)
        addr=np.uint16(0xff00+data)
        cpu.bus.write(addr,cpu.registers.a_reg)
        self.log(f'LD (0xff00 + {hex(data)}) A')
        cpu.registers.pc_reg+=2
        cpu.cycles=3

    def xE2(self,cpu):
        '''
        Store the contents of register A in the internal RAM, port register, or mode register at
        the address in the range 0xFF00-0xFFFF specified by register C.

        ->    0xFF00-0xFF7F: Port/Mode registers, control register, sound register
        ->    0xFF80-0xFFFE: Working & Stack RAM (127 bytes)
        ->    0xFFFF: Interrupt Enable Register
        '''
        addr=np.uint16(0xff00+cpu.registers.c_reg)
        cpu.bus.write(addr,cpu.registers.a_reg)
        self.log(f'LD (0xff00 + {hex(cpu.registers.c_reg)}) A')
        cpu.registers.pc_reg+=1
        cpu.cycles=2

    def xEA(self,cpu):
        '''
        Store the contents of register A in the internal RAM or register specified by the 16-bit
        immediate operand a16.
        '''
        addr = cpu.bus.read(cpu.registers.pc_reg+1,2)
        cpu.bus.write(addr,cpu.registers.a_reg)
        self.log(f'LD ({hex(addr)}) A')
        cpu.registers.pc_reg+=3
        cpu.cycles=4

    def xF0(self,cpu):
        '''
        Load into register A the contents of the internal RAM, port register, or mode register at the
        address in the range 0xFF00-0xFFFF specified by the 8-bit immediate operand a8.

        Note: Should specify a 16-bit address in the mnemonic portion for a8, although the
        immediate operand only has the lower-order 8 bits.

        ->    0xFF00-0xFF7F: Port/Mode registers, control register, sound register
        ->    0xFF80-0xFFFE: Working & Stack RAM (127 bytes)
        ->    0xFFFF: Interrupt Enable Register
        '''
        val = cpu.bus.read(cpu.registers.pc_reg+1)
        addr = np.uint16(0xff00+val)
        cpu.registers.a_reg = cpu.bus.read(addr)
        self.log(f'LD A ({hex(addr)})')
        
        cpu.registers.pc_reg+=2
        cpu.cycles=3

    def xFE(self,cpu):
        # TODO set half carry flag
        '''
        Compare the contents of register A and the contents of the 8-bit immediate operand
        d8 by calculating A - d8, and set the Z flag if they are equal.

        The execution of this instruction does not affect the contents of register A.
        '''
        data = cpu.bus.read(cpu.registers.pc_reg+1)
        if cpu.registers.a_reg-data==0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')

        if cpu.registers.a_reg-data<0:
            cpu.registers.Set('c')
        else:
            cpu.registers.Clear('c')

        cpu.registers.Set('n')
        self.log(f'CP {hex(data)}')
        cpu.registers.pc_reg+=2
        cpu.cycles=2

class PrefixedInstructions:
    def __init__(self):
        super().__init__()

    def log(self,msg,logging=False):
        if logging:
            print(msg)

    def x11(self,cpu):
        '''
        Rotate the contents of register C to the left. That is, the contents of bit 0 are copied
        to bit 1, and the previous contents of bit 1 (before the copy operation) are copied to bit 2.
        The same operation is repeated in sequence for the rest of the register. The previous contents
        of the carry (CY) flag are copied to bit 0 of register C.
        '''
        INT_BITS=32

        c7=cpu.registers.c_reg>>7
        cpu.registers.c_reg=np.uint8((cpu.registers.c_reg << 1)|(cpu.registers.c_reg >> (INT_BITS - 1)))
        if cpu.registers.isSet('c'):
            cpu.registers.c_reg|=1
        else:
            cpu.registers.c_reg&=~(1)
        if bool(c7):
            cpu.registers.Set('c')
        else:
            cpu.registers.Clear('c')
        if cpu.registers.c_reg==0:
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        cpu.registers.Clear('n')
        cpu.registers.Clear('h')
        self.log('RL C')
        cpu.registers.pc_reg+=1
        cpu.cycles=2


    def x7C(self,cpu):
        '''
        Copy the complement of the contents of bit 7 in register H to the Z flag of the program status word (PSW).
        '''
        if bool(abs((cpu.registers.h_reg>>7)-1)):
            cpu.registers.Set('z')
        else:
            cpu.registers.Clear('z')
        cpu.registers.Clear('n')
        cpu.registers.Set('h')
        self.log('BIT 7 H')
        cpu.registers.pc_reg+=1
        cpu.cycles=2