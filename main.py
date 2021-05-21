import argparse
import cpu
import registers
import bus
import ppu
from timeit import default_timer as timer
from datetime import timedelta

def main():

    # set up command line argument parser
    parser = argparse.ArgumentParser(description='NES Emulator.')
    parser.add_argument('rom_path',
                        metavar='R',
                        type=str,
                        help='path to nes rom')
    parser.add_argument('--test')
    args = parser.parse_args()

    r=registers.Registers()
    b=bus.Bus()
    # load rom
    with open(args.rom_path, 'rb') as file:
        # TODO load full file
        b.loadRom(file.read()[0x100:])

    start=timer()
    while True:
        b.Clock()
    end=timer()
    print(timedelta(seconds=end-start))

    b.cpu.log(True)
    addr=0x8000
    with open('./VRAM/bgTiles.txt','w') as f:
        for x in range(25):
            f.write(f'{hex(addr)}:  ')
            for y in range(16):
                f.write(b.read(addr+y).to_bytes(1,'little').hex())
            addr+=0x010
            f.write('\n')

if __name__ == '__main__':
    main()