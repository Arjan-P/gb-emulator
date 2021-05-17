import argparse
import cpu
import registers
import bus
import ppu

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
    while True:#b.cpu.running:
        b.Clock()
    print(b.read(0xff40))

if __name__ == '__main__':
    main()