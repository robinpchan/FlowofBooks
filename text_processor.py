import tkinter as tk
from tkinter import ttk
import re

class TextProcessor(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title('Text Processor')
        self.geometry('400x200')

        self.input_label = ttk.Label(self, text='Input:')
        self.input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.input_entry = ttk.Entry(self, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.cleanse_copy_button = ttk.Button(self, text='Cleanse & Copy', command=self.cleanse_and_copy)
        self.cleanse_copy_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.reverse_capitalize_button = ttk.Button(self, text='Reverse & Capitalize', command=self.reverse_and_capitalize)
        self.reverse_capitalize_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.output_label = ttk.Label(self, text='Output:')
        self.output_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.output_entry = ttk.Entry(self, width=50, state='readonly')
        self.output_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    def cleanse_and_copy(self):
        input_text = self.input_entry.get()
        cleansed_text = ''.join(re.findall(r'\d', input_text))

        self.output_entry.config(state='normal')
        self.output_entry.delete(0, 'end')
        self.output_entry.insert(0, cleansed_text)
        self.output_entry.config(state='readonly')

        self.clipboard_clear()
        self.clipboard_append(cleansed_text)

    def reverse_and_capitalize(self):
        input_text = self.input_entry.get()
        words = input_text.split()
        if words:
            words[0], words[-1] = words[-1], words[0]
            reversed_capitalized_text = ' '.join(word.upper() for word in words)
        else:
            reversed_capitalized_text = ""

        self.output_entry.config(state='normal')
        self.output_entry.delete(0, 'end')
        self.output_entry.insert(0, reversed_capitalized_text)
        self.output_entry.config(state='readonly')

        self.clipboard_clear()
        self.clipboard_append(reversed_capitalized_text)





