import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
class OrderOrganizer(tk.Tk):
    def __init__(self):
            super().__init__()

            self.title("Customer Order Organizer")
            self.geometry("800x400")

            shops = ["PB-KIDS", "PB-ADULT", "IFC", "LT", "FW", "DB", "RB", "TS", 'WE']

            # Create and position widgets
            self.shop_var = tk.StringVar()
            self.shop_menu = tk.OptionMenu(self, self.shop_var, *shops)
            self.shop_menu.grid(row=0, column=0)

            self.book_title_label = tk.Label(self, text="Book Title:")
            self.book_title_label.grid(row=1, column=0)
            self.book_title_entry = tk.Entry(self)
            self.book_title_entry.grid(row=1, column=1)

            self.price_label = tk.Label(self, text="Price:")
            self.price_label.grid(row=2, column=0)
            self.price_entry = tk.Entry(self)
            self.price_entry.grid(row=2, column=1)

            self.remarks_label = tk.Label(self, text="Remarks:")
            self.remarks_label.grid(row=3, column=0)
            self.remarks_entry = tk.Entry(self)
            self.remarks_entry.grid(row=3, column=1)

            self.save_button = tk.Button(self, text="Save Order", command=self.save_order)
            self.save_button.grid(row=4, column=0)

            self.reset_button = tk.Button(self, text="Reset", command=self.reset)
            self.reset_button.grid(row=4, column=1)

            self.orders_frame = tk.Frame(self)
            self.orders_frame.grid(row=5, column=0, columnspan=2)

            self.orders_list = tk.Listbox(self.orders_frame, width=80)
            self.orders_list.pack()
            self.sort_button = tk.Button(self, text="Sort By Shop", command=self.sort_orders_by_shop)
            self.sort_button.grid(row=4, column=2)

            self.export_button = tk.Button(self, text="Export to Excel", command=self.export_to_excel)
            self.export_button.grid(row=4, column=3)

            self.orders_list.bind("<Button-3>", self.display_delete_menu)

    def save_order(self):
            shop = self.shop_var.get()
            book_title = self.book_title_entry.get()
            price = self.price_entry.get()
            remarks = self.remarks_entry.get()


            order = f"{shop}, {book_title}, {price}, {remarks}"
            self.orders_list.insert(tk.END, order)

            # Reset the input fields
            self.shop_var.set('')
            self.book_title_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.remarks_entry.delete(0, tk.END)

    def reset(self):
            self.orders_list.delete(0, tk.END)
            self.book_title_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.remarks_entry.delete(0, tk.END)

    def sort_orders_by_shop(self):
            orders = list(self.orders_list.get(0, tk.END))
            sorted_orders = sorted(orders, key=lambda x: x.split(',')[0].strip())
            self.orders_list.delete(0, tk.END)
            for order in sorted_orders:
                self.orders_list.insert(tk.END, order)

    def delete_order(self):
            selected = self.orders_list.curselection()
            if selected:
                    self.orders_list.delete(selected)

    def display_delete_menu(self, event):
            popup_menu = tk.Menu(self, tearoff=0)
            popup_menu.add_command(label="Delete Order", command=self.delete_order)
            popup_menu.post(event.x_root, event.y_root)

    def export_to_excel(self):
            orders = list(self.orders_list.get(0, tk.END))
            if not orders:
                    messagebox.showerror("Error", "No orders to export.")
                    return

            data = [order.split(", ") for order in orders]
            df = pd.DataFrame(data, columns=["Shop", "Book Title", "Price", "Remarks"])

            file_name = "orders.xlsx"
            if os.path.exists(file_name):
                    os.remove(file_name)

            try:
                    df.to_excel(file_name, index=False)
                    messagebox.showinfo("Success", f"Orders exported to {file_name}.")
            except Exception as e:
                    messagebox.showerror("Error", f"Failed to export orders: {str(e)}")

if __name__ == "__main__":
    app = OrderOrganizer()
    app.mainloop()

