# simple_emulator/gui.py

import tkinter as tk
from tkinter import messagebox
import threading
import sys

class EmulatorApp:
    def __init__(self, root, emulator):
        self.root = root
        self.emulator = emulator
        self.root.title("Nova")

        self.text = tk.Text(root, wrap='word', bg='black', fg='white', insertbackground='white')
        self.text.pack(expand=1, fill='both')

        # Start the emulator automatically
        self.start_emulator()

        self.start_button = tk.Button(root, text="Start Emulator", command=self.start_emulator)
        self.start_button.pack(side='left', padx=20, pady=20)

        self.stop_button = tk.Button(root, text="Stop Emulator", command=self.stop_emulator)
        self.stop_button.pack(side='right', padx=20, pady=20)

        self.emulator_thread = None

        # Bind keypress event
        self.text.bind("<KeyPress>", self.on_keypress)

    def start_emulator(self):
        self.text.delete(1.0, tk.END)
        bios_file = 'bios.bin'
        bootloader_file = 'boot.img'
        self.emulator.set_output_callback(self.update_terminal)
        self.emulator.set_keypress_callback(self.handle_keypress)
        self.emulator.wait_for_keypress = True
        self.emulator_thread = threading.Thread(target=self.emulator.run, args=(bios_file, bootloader_file))
        self.emulator_thread.start()

    def stop_emulator(self):
        if self.emulator.running:
            self.emulator.running = False
        if self.emulator_thread and self.emulator_thread.is_alive():
            self.emulator_thread.join()
        messagebox.showinfo("Info", "Emulator stopped")

    def update_terminal(self, text, is_error=False):
        if is_error:
            # Print errors to console
            sys.stderr.write(text)
        else:
            # Print regular output to the text widget
            self.text.insert(tk.END, text)
            self.text.see(tk.END)
        self.root.update_idletasks()  # Ensure the UI updates immediately

    def handle_keypress(self, event):
        self.emulator.wait_for_keypress = False
        self.emulator.set_output_callback(self.update_terminal)

        key = event.char

        if not key:
            return

        # Print the key that was pressed
        self.emulator.memory[self.emulator.ip] = 0xB4  # mov ah, 0x0E
        self.emulator.memory[self.emulator.ip + 1] = 0x0E  # Teletype Output
        self.emulator.memory[self.emulator.ip + 2] = ord(key)  # key pressed
        self.emulator.memory[self.emulator.ip + 3] = 0xCD  # int 0x10
        self.emulator.memory[self.emulator.ip + 4] = 0x10
        self.emulator.memory[self.emulator.ip + 5] = 0xF4  # Halt
        self.emulator.ip += 6
        self.emulator.execute()

    def on_keypress(self, event):
        self.handle_keypress(event)
