# simple_emulator/emulator.py

import os

class SimpleEmulator:
    def __init__(self):
        self.memory = [0] * 0xA00000  # 64KB memory
        self.registers = {
            'ax': 0, 'bx': 0, 'cx': 0, 'dx': 0,
            'si': 0, 'di': 0, 'sp': 0xFFFF, 'bp': 0,
            'al': 0, 'ah': 0, 'bl': 0, 'bh': 0,
            'cl': 0, 'ch': 0, 'dl': 0, 'dh': 0
        }
        self.flags = {'carry': 0, 'zero': 0, 'sign': 0, 'overflow': 0}
        self.ip = 0x7C00  # Instruction pointer (start of BIOS)
        self.running = False
        self.output_callback = None
        self.keypress_callback = None
        self.wait_for_keypress = False

    def set_output_callback(self, callback):
        self.output_callback = callback

    def set_keypress_callback(self, callback):
        self.keypress_callback = callback

    def load_file(self, file_path, address):
        with open(file_path, 'rb') as f:
            data = f.read()
            for i, byte in enumerate(data):
                self.memory[address + i] = byte

    def execute(self):
        ip = self.ip
        self.running = True
        while self.running:
            if ip >= len(self.memory):
                break

            opcode = self.memory[ip]

            if opcode == 0xB4:  # mov ah, imm8 (setup for output)
                self.registers['ah'] = self.memory[ip + 1]
                ip += 2
            elif opcode == 0xB0:  # mov al, imm8 (character to output)
                self.registers['al'] = self.memory[ip + 1]
                ip += 2
            elif opcode == 0xCD:  # interrupt
                int_no = self.memory[ip + 1]
                self.handle_interrupt(int_no)
                ip += 2
            elif opcode == 0xF4:  # halt
                self.running = False
            elif opcode == 0x00 or opcode == 0x30:  # nop
                ip += 1
            else:
                if self.output_callback:
                    self.output_callback(f"Unhandled opcode {opcode:02X} at IP {ip:04X}\n", is_error=True)
                ip += 1

    def handle_interrupt(self, int_no):
        if int_no == 0x10:  # Video services
            self.handle_interrupt_10()
        elif int_no == 0x16:  # Keyboard services
            self.handle_interrupt_16()
        else:
            if self.output_callback:
                self.output_callback(f"Interrupt {int_no:02X} called\n", is_error=True)

    def handle_interrupt_10(self):
        ah = self.registers['ah']
        al = self.registers['al']
        if ah == 0x0E:  # Teletype Output
            if self.output_callback:
                self.output_callback(chr(al))
        else:
            if self.output_callback:
                self.output_callback(f"Interrupt 10 with AH = {ah:02X} and AL = {al:02X} not handled\n", is_error=True)

    def handle_interrupt_16(self):
        # Simulate waiting for a keypress
        if self.wait_for_keypress and self.keypress_callback:
            self.keypress_callback()
        else:
            if self.output_callback:
                self.output_callback(f"Interrupt 16 not handled\n", is_error=True)

    def run(self, bios_file, bootloader_file=None):
        self.load_file(bios_file, 0x7C00)
        self.execute()

        if bootloader_file:
            if not os.path.exists(bootloader_file):
                print(f"Creating {bootloader_file}...")
                self.create_boot_image(bootloader_file)
            self.load_file(bootloader_file, 0x7C00)
            self.execute()

    def create_boot_image(self, file_name):
        boot_image_content = bytes([
            # Print "Nova"
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
        with open(file_name, 'wb') as f:
            f.write(boot_image_content)
