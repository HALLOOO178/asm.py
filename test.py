from simple_emulator.simple_emulator import SimpleEmulator
import sys

def main():
    emulator = SimpleEmulator()

    # BIOS content for the emulator
    bios_content = bytes([
    0xB4, 0x0E,  # mov ah, 0x0E (Teletype Output)
    0xB0, 0x74,  # mov al, 't'
    0xCD, 0x10,  # int 0x10 (call interrupt)
    0xB0, 0x65,  # mov al, 'e'
    0xCD, 0x10,  # int 0x10 (call interrupt)
    0xB0, 0x73,  # mov al, 's'
    0xCD, 0x10,  # int 0x10 (call interrupt)
    0xB0, 0x74,  # mov al, 't'
    0xCD, 0x10,  # int 0x10 (call interrupt)
    0xB0, 0x0A,  # mov al, '\n'
    0xCD, 0x10,  # int 0x10 (call interrupt)
    0xF4         # halt (stop execution)
  ])


    # Write the BIOS content to a file
    with open('bios.bin', 'wb') as f:
        f.write(bios_content)

    # Load and run the BIOS
    emulator.set_output_callback(sys.stdout.write)
    emulator.run('bios.bin')

if __name__ == "__main__":
    main()