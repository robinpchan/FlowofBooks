import tkinter as tk
from tkinter import ttk
import sqlite3
import os

import supplier_db
from text_processor import TextProcessor
from school_order_organizer import SchoolOrderGUI
from replenishment_optimizer_V3 import ReplenishmentOptimizer
from sales_op_v2_bs import SalesReportOptimizer
import test_keep_v0
import buy_cal

class FlowOfBooks(tk.Tk):
    def __init__(self):
        super().__init__()
        # Create connection to the database
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.db")
        self.conn = sqlite3.connect(db_path)
        self.orders_conn = sqlite3.connect('orders.db')

        print(f"FlowOfBooks orders_db connection: {self.orders_conn}")

        # Window settings
        self.title("Flow of Books")
        self.geometry("400x400")

        # Create main frame
        main_frame = tk.Frame(self, width=560, height=420)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create buttons for parent directories
        btn_style = ttk.Style()
        btn_style.configure('big.TButton', font=('Arial', 20))

        upstream_btn = ttk.Button(main_frame, text="Upstream", style='big.TButton', command=self.show_upstream_menu)
        upstream_btn.pack(fill="both", expand=True)
        midstream_btn = ttk.Button(main_frame, text="Mid-Stream", style='big.TButton', command=self.show_midstream_menu)
        midstream_btn.pack(fill="both", expand=True)
        downstream_btn = ttk.Button(main_frame, text="Downstream", style='big.TButton', command=self.show_downstream_menu)
        downstream_btn.pack(fill="both", expand=True)

    def show_upstream_menu(self):
        # Create Upstream menu
        upstream_menu = tk.Menu(self, tearoff=0)

        # Add Supplier submenu
        supplier_submenu = tk.Menu(upstream_menu, tearoff=0)
        supplier_submenu.add_command(label="Missing Shipment Tracker")
        supplier_submenu.add_command(label="Supplier Contact DB", command=supplier_db.main)
        upstream_menu.add_cascade(label="Supplier", menu=supplier_submenu)

        # Add Product submenu
        product_submenu = tk.Menu(upstream_menu, tearoff=0)
        product_submenu.add_command(label="Text Processor", command=self.open_text_processor)
        product_submenu.add_command(label="Buying Calculator", command=buy_cal.main)
        upstream_menu.add_cascade(label="Product", menu=product_submenu)

        # Show menu
        self.show_menu(upstream_menu)

    def show_midstream_menu(self):
        # Create Mid-Stream menu
        midstream_menu = tk.Menu(self, tearoff=0)
        midstream_menu.add_command(label="Project Manager", command=test_keep_v0.main)
        midstream_menu.add_command(label="Book Catalog")

        # Show menu
        self.show_menu(midstream_menu)

    def show_downstream_menu(self):
        # Create Downstream menu
        downstream_menu = tk.Menu(self, tearoff=0)

        # Add Customer submenu
        customer_submenu = tk.Menu(downstream_menu, tearoff=0)
        customer_submenu.add_command(label="Customer Order Organizer", command=self.open_customer_order_app)
        downstream_menu.add_cascade(label="Customer", menu=customer_submenu)

        # Add Shops submenu
        shop_submenu = tk.Menu(downstream_menu, tearoff=0)
        shop_submenu.add_command(label="Replenishment Optimizer", command=self.open_replenishment_optimizer)
        shop_submenu.add_command(label="Sales Report Optimizer",
                                 command=self.open_sales_report_optimizer)  # Add this line
        downstream_menu.add_cascade(label="Shops", menu=shop_submenu)

        # Add School Order Organizer
        downstream_menu.add_command(label="School Order Organizer", command=self.open_school_order_organizer)

        # Show menu
        self.show_menu(downstream_menu)

    def show_menu(self, menu):
        x, y = self.winfo_pointerxy()
        menu.post(x, y)

    def open_text_processor(self):
        TextProcessor()

    def open_school_order_organizer(self):
        SchoolOrderGUI(tk.Toplevel())

    def open_replenishment_optimizer(self):
        ReplenishmentOptimizer()

    def open_sales_report_optimizer(self):
        SalesReportOptimizer()

    def open_customer_order_app(self):
        customer_order_window = tk.Toplevel(self)
        customer_order_app = CustomerOrderApp(customer_order_window, self.orders_conn)



if __name__ == "__main__":
    app = FlowOfBooks()
    app.mainloop()


