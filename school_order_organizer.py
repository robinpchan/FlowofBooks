import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
import openpyxl

class SchoolOrderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("School Order Organizer")
        self.master.geometry("600x400")

        self.orders = []
        # Keep school name checkbox
        self.keep_school_name = tk.BooleanVar()
        self.keep_school_name_check = ttk.Checkbutton(self.master, text="Keep School Name",
                                                      variable=self.keep_school_name)
        self.keep_school_name_check.grid(column=2, row=0)
        # School name entry
        self.school_name_label = ttk.Label(self.master, text="School Name:")
        self.school_name_label.grid(column=0, row=0, padx=10, pady=10)
        self.school_name_entry = ttk.Entry(self.master)
        self.school_name_entry.grid(column=1, row=0)

        # Book title entry
        self.book_title_label = ttk.Label(self.master, text="Book Title:")
        self.book_title_label.grid(column=0, row=1, padx=10, pady=10)
        self.book_title_entry = ttk.Entry(self.master)
        self.book_title_entry.grid(column=1, row=1)

        # ISBN entry
        self.isbn_label = ttk.Label(self.master, text="ISBN:")
        self.isbn_label.grid(column=0, row=2, padx=10, pady=10)
        self.isbn_entry = ttk.Entry(self.master)
        self.isbn_entry.grid(column=1, row=2)

        # Quantity entry
        self.qty_label = ttk.Label(self.master, text="Quantity:")
        self.qty_label.grid(column=0, row=3, padx=10, pady=10)
        self.qty_entry = ttk.Entry(self.master)
        self.qty_entry.grid(column=1, row=3)

        # Save Order button
        self.save_order_button = ttk.Button(self.master, text="Save Order", command=self.save_order)
        self.save_order_button.grid(column=0, row=4, padx=10, pady=10)

        # Reset button
        self.reset_button = ttk.Button(self.master, text="Reset", command=self.reset)
        self.reset_button.grid(column=1, row=4, padx=10, pady=10)

        # Sort by School Name button
        self.sort_school_button = ttk.Button(self.master, text="Sort by School Name", command=self.sort_school)
        self.sort_school_button.grid(column=2, row=4, padx=10, pady=10)

        # Export to Excel button
        self.export_excel_button = ttk.Button(self.master, text="Export to Excel", command=self.export_to_excel)
        self.export_excel_button.grid(column=3, row=4, padx=10, pady=10)

        # Display frame
        self.display_frame = ttk.LabelFrame(self.master, text="Saved Orders")
        self.display_frame.grid(column=0, row=5, columnspan=4, padx=10, pady=10)
        self.display = ttk.Label(self.display_frame, text="")
        self.display.pack(padx=10, pady=10)

    def save_order(self):
        school_name = self.school_name_entry.get()
        book_title = self.book_title_entry.get()
        isbn = self.isbn_entry.get()
        qty = self.qty_entry.get()
        self.orders.append((school_name, book_title, isbn, qty))

        # Clear entry fields
        if not self.keep_school_name.get():
            self.school_name_entry.delete(0, 'end')
        self.book_title_entry.delete(0, 'end')
        self.isbn_entry.delete(0, 'end')
        self.qty_entry.delete(0, 'end')

        self.update_display()

    def update_display(self):
        order_str = ""
        for order in self.orders:
            order_str = ""
            for order in self.orders:
                order_str += f"{order[0]}, {order[1]}, {order[2]}, {order[3]}\n"
            self.display.config(text=order_str)

    def reset(self):
        self.orders.clear()
        self.update_display()

    def sort_school(self):
        self.orders.sort(key=lambda order: order[0].lower())
        self.update_display()

    def export_to_excel(self):
        if not self.orders:
            return

        df = pd.DataFrame(self.orders, columns=["School Name", "Book Title", "ISBN", "Quantity"])
        file_path = "school_orders.xlsx"
        writer = pd.ExcelWriter(file_path, engine='openpyxl')
        df.to_excel(writer, index=False)
        writer.save()

        print(f"Orders exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    SchoolOrderGUI(root)
    root.mainloop()

