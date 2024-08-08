# examples/run_emulator.py

import tkinter as tk
from nova import SimpleEmulator, EmulatorApp

if __name__ == '__main__':
    emulator = SimpleEmulator()

    bios_content = bytes([
        0xB4, 0x0E,  # mov ah, 0x0E (Teletype Output)
        0xB0, 0x4E,  # mov al, 'N'
        0xCD, 0x10,  # int 0x10 (call interrupt)
        0xB0, 0x6F,  # mov al, 'o'
        0xCD, 0x10,  # int 0x10 (call interrupt)
        0xB0, 0x76,  # mov al, 'v'
        0xCD, 0x10,  # int 0x10 (call interrupt)
        0xB0, 0x61,  # mov al, 'a'
        0xCD, 0x10,  # int 0x10 (call interrupt)

        # Newline
        0xB4, 0x0E,  # mov ah, 0x0E (Teletype Output)
        0xB0, 0x0D,  # mov al, '\r' (carriage return)
        0xCD, 0x10,  # int 0x10 (call interrupt)
        0xB0, 0x0A,  # mov al, '\n' (line feed)
        0xCD, 0x10,  # int 0x10 (call interrupt)

        # Halt
        0xF4         # halt (stop execution)
    ])

    with open('bios.bin', 'wb') as f:
        f.write(bios_content)

    # Set up the GUI
    root = tk.Tk()
    app = EmulatorApp(root, emulator)
    root.mainloop()
