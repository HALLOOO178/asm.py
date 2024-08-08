# simple_emulator/os_builder.py

import argparse
import os

def create_boot_image(file_name, text):
    boot_image_content = []

    for char in text:
        boot_image_content.extend([
            0xB4, 0x0E,  # mov ah, 0x0E (Teletype Output)
            0xB0, ord(char),  # mov al, char
            0xCD, 0x10,  # int 0x10 (call interrupt)
        ])

    # Add a newline at the end
    boot_image_content.extend([
        0xB4, 0x0E,  # mov ah, 0x0E (Teletype Output)
        0xB0, 0x0D,  # mov al, '\r' (carriage return)
        0xCD, 0x10,  # int 0x10 (call interrupt)
        0xB0, 0x0A,  # mov al, '\n' (line feed)
        0xCD, 0x10,  # int 0x10 (call interrupt)
        0xF4         # halt (stop execution)
    ])

    with open(file_name, 'wb') as f:
        f.write(bytes(boot_image_content))

def main():
    parser = argparse.ArgumentParser(description='Simple OS Builder for the Simple Emulator.')
    parser.add_argument('output', help='Output file name for the boot image')
    parser.add_argument('--text', help='Text to display on boot', default='Hello, Nova!')

    args = parser.parse_args()

    create_boot_image(args.output, args.text)
    print(f"Boot image created: {args.output}")

if __name__ == '__main__':
    main()
