import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import pyperclip
import json
import os

def main():
    BuyingCalculator()
class BuyingCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Price Calculator")
        self.geometry("800x600")

        self.create_widgets()
        self.load_conversion_settings()

        self.data = {}

    def create_widgets(self):
        # Publisher A input fields
        ttk.Label(self, text="Publisher A").grid(column=0, row=0, padx=10, pady=10)
        ttk.Label(self, text="Cover Price").grid(column=0, row=1, padx=10, pady=10)
        self.cover_price_A = ttk.Entry(self)
        self.cover_price_A.grid(column=1, row=1)

        ttk.Label(self, text="Currency").grid(column=0, row=2, padx=10, pady=10)
        self.currency_A = ttk.Combobox(self, values=["USD", "GBP"], state="readonly")
        self.currency_A.current(0)
        self.currency_A.grid(column=1, row=2)

        ttk.Label(self, text="Publisher Name").grid(column=0, row=3, padx=10, pady=10)
        self.publisher_name_A = ttk.Entry(self)
        self.publisher_name_A.grid(column=1, row=3)

        ttk.Label(self, text="Supplier Discount").grid(column=0, row=4, padx=10, pady=10)
        self.supplier_discount_A = ttk.Entry(self)
        self.supplier_discount_A.grid(column=1, row=4)

        # Special Price A
        self.special_price_label_A = tk.Label(self, text="Special Price A")
        self.special_price_label_A.grid(row=5, column=0)
        self.special_price_A = tk.Entry(self)
        self.special_price_A.grid(row=5, column=1)

        # Publisher B input fields
        ttk.Label(self, text="Publisher B").grid(column=2, row=0, padx=10, pady=10)
        ttk.Label(self, text="Cover Price").grid(column=2, row=1, padx=10, pady=10)
        self.cover_price_B = ttk.Entry(self)
        self.cover_price_B.grid(column=3, row=1)

        ttk.Label(self, text="Currency").grid(column=2, row=2, padx=10, pady=10)
        self.currency_B = ttk.Combobox(self, values=["USD", "GBP"], state="readonly")
        self.currency_B.current(0)
        self.currency_B.grid(column=3, row=2)

        ttk.Label(self, text="Publisher Name").grid(column=2, row=3, padx=10, pady=10)
        self.publisher_name_B = ttk.Entry(self)
        self.publisher_name_B.grid(column=3, row=3)

        ttk.Label(self, text="Supplier Discount").grid(column=2, row=4, padx=10, pady=10)
        self.supplier_discount_B = ttk.Entry(self)
        self.supplier_discount_B.grid(column=3, row=4)

        # Special Price B
        self.special_price_label_B = tk.Label(self, text="Special Price B")
        self.special_price_label_B.grid(row=5, column=2)
        self.special_price_B = tk.Entry(self)
        self.special_price_B.grid(row=5, column=3)

        # Use Special Price for Retail Checkboxes
        self.use_special_price_A = tk.BooleanVar()
        self.use_special_price_B = tk.BooleanVar()

        self.use_special_price_check_A = tk.Checkbutton(self, text="Use Special Price for Retail A",
                                                        variable=self.use_special_price_A)
        self.use_special_price_check_A.grid(row=6, column=0)

        self.use_special_price_check_B = tk.Checkbutton(self, text="Use Special Price for Retail B",
                                                        variable=self.use_special_price_B)
        self.use_special_price_check_B.grid(row=6, column=2)

        # Conversion settings
        self.conversion_settings_button = ttk.Button(self, text="Conversion Settings",
                                                     command=self.show_conversion_settings)
        self.conversion_settings_button.grid(column=0, row=7, padx=10, pady=10)

        # Compute button
        self.compute_button = ttk.Button(self, text="Compute", command=self.compute)
        self.compute_button.grid(column=1, row=7, padx=10, pady=10)

        # Reset input button
        self.reset_input_button = ttk.Button(self, text="Reset Input", command=self.reset_input_fields)
        self.reset_input_button.grid(column=2, row=7, padx=10, pady=10)

        self.copy_comparison_button = ttk.Button(self, text="Copy Comparison", command=self.copy_comparison)
        self.copy_comparison_button.grid(column=3, row=7, padx=10, pady=10)

        # Export to file button
        self.export_to_file_button = ttk.Button(self, text="Export to File", command=self.export_to_file)
        self.export_to_file_button.grid(column=4, row=7, padx=10, pady=10)

        # Results display frame
        self.results_frame = ttk.Frame(self)
        self.results_frame.grid(column=0, row=8, columnspan=5)

    def load_conversion_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)

            self.usd_to_hkd_cost_value = settings.get("usd_to_hkd_cost", 1)
            self.gbp_to_hkd_cost_value = settings.get("gbp_to_hkd_cost", 1)
            self.usd_to_hkd_retail_value = settings.get("usd_to_hkd_retail", 1)
            self.gbp_to_hkd_retail_value = settings.get("gbp_to_hkd_retail", 1)
        else:
            self.usd_to_hkd_cost_value = 1
            self.gbp_to_hkd_cost_value = 1
            self.usd_to_hkd_retail_value = 1
            self.gbp_to_hkd_retail_value = 1
    def show_conversion_settings(self):
            self.settings_window = tk.Toplevel(self)
            self.settings_window.title("Conversion Settings")

            # Default USD to HKD cost conversion
            ttk.Label(self.settings_window, text="Default USD to HKD cost conversion").grid(column=0, row=0, padx=10,
                                                                                            pady=10)
            self.usd_to_hkd_cost = ttk.Entry(self.settings_window)
            self.usd_to_hkd_cost.grid(column=1, row=0)

            # Default GBP to HKD cost conversion
            ttk.Label(self.settings_window, text="Default GBP to HKD cost conversion").grid(column=0, row=1, padx=10,
                                                                                            pady=10)
            self.gbp_to_hkd_cost = ttk.Entry(self.settings_window)
            self.gbp_to_hkd_cost.grid(column=1, row=1)

            # Default USD to HKD retail price
            ttk.Label(self.settings_window, text="Default USD to HKD retail price").grid(column=0, row=2, padx=10,
                                                                                         pady=10)
            self.usd_to_hkd_retail = ttk.Entry(self.settings_window)
            self.usd_to_hkd_retail.grid(column=1, row=2)

            # Default GBP to HKD retail price
            ttk.Label(self.settings_window, text="Default GBP to HKD retail price").grid(column=0, row=3, padx=10,
                                                                                         pady=10)
            self.gbp_to_hkd_retail = ttk.Entry(self.settings_window)
            self.gbp_to_hkd_retail.grid(column=1, row=3)

            # Save button
            self.save_button = ttk.Button(self.settings_window, text="Save", command=self.save_conversion_settings)
            self.save_button.grid(column=1, row=4, padx=10, pady=10)
            # Cancel button
            self.cancel_button = ttk.Button(self.settings_window, text="Cancel",
                       command=self.settings_window.destroy)
            self.cancel_button.grid(column=2, row=4, padx=10, pady=10)
            # Insert values
            self.usd_to_hkd_cost.insert(0, self.usd_to_hkd_cost_value)
            self.gbp_to_hkd_cost.insert(0, self.gbp_to_hkd_cost_value)
            self.usd_to_hkd_retail.insert(0, self.usd_to_hkd_retail_value)
            self.gbp_to_hkd_retail.insert(0, self.gbp_to_hkd_retail_value)
    def save_conversion_settings(self):
            try:
                self.usd_to_hkd_cost_value = float(self.usd_to_hkd_cost.get())
                self.gbp_to_hkd_cost_value = float(self.gbp_to_hkd_cost.get())
                self.usd_to_hkd_retail_value = float(self.usd_to_hkd_retail.get())
                self.gbp_to_hkd_retail_value = float(self.gbp_to_hkd_retail.get())
                self.settings_window.destroy()
                self.save_settings_to_file()
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter valid numbers for all conversion rates.")
    def save_settings_to_file(self):
        settings = {
            "usd_to_hkd_cost": self.usd_to_hkd_cost_value,
            "gbp_to_hkd_cost": self.gbp_to_hkd_cost_value,
            "usd_to_hkd_retail": self.usd_to_hkd_retail_value,
            "gbp_to_hkd_retail": self.gbp_to_hkd_retail_value,
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def calculate_retail_cost_margin(self, currency, cover_price, supplier_discount, special_price=None,
                                     use_special_price=False):
        # Determine the appropriate conversion rates based on the currency
        retail_conversion_rate = self.usd_to_hkd_retail_value if currency == "USD" else self.gbp_to_hkd_retail_value
        cost_conversion_rate = self.usd_to_hkd_cost_value if currency == "USD" else self.gbp_to_hkd_cost_value

        # If special_price is provided and use_special_price is True, use it for calculations, otherwise use the cover_price
        price_to_use = special_price if use_special_price and special_price is not None else cover_price

        # Calculate retail price and cost using the respective conversion rates
        retail_price = price_to_use * retail_conversion_rate
        cost = price_to_use * cost_conversion_rate * (1 - supplier_discount / 100)

        # Calculate margin
        margin = retail_price - cost

        return retail_price, cost, margin

    def compute(self):
        # Get input values
        self.data["publisher_A"] = self.publisher_name_A.get()
        self.data["publisher_B"] = self.publisher_name_B.get()
        self.data["cover_price_A"] = float(self.cover_price_A.get())
        self.data["cover_price_B"] = float(self.cover_price_B.get())
        self.data["currency_A"] = self.currency_A.get()
        self.data["currency_B"] = self.currency_B.get()
        self.data["supplier_discount_A"] = float(self.supplier_discount_A.get())
        self.data["supplier_discount_B"] = float(self.supplier_discount_B.get())

        # Get special prices and "use special price" options
        self.data["special_price_A"] = float(self.special_price_A.get()) if self.special_price_A.get() else None
        self.data["special_price_B"] = float(self.special_price_B.get()) if self.special_price_B.get() else None
        self.data["use_special_price_A"] = self.use_special_price_A.get()
        self.data["use_special_price_B"] = self.use_special_price_B.get()

        # Calculate retail prices, cost, and margin
        self.data["retail_price_A"], self.data["cost_A"], self.data["margin_A"] = self.calculate_retail_cost_margin(
            self.data["currency_A"], self.data["cover_price_A"], self.data["supplier_discount_A"],
            self.data["special_price_A"], self.data["use_special_price_A"])

        self.data["retail_price_B"], self.data["cost_B"], self.data["margin_B"] = self.calculate_retail_cost_margin(
            self.data["currency_B"], self.data["cover_price_B"], self.data["supplier_discount_B"],
            self.data["special_price_B"], self.data["use_special_price_B"])

        # Display results
        self.display_results()

    def display_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        results = [
            ("Publisher", self.data["publisher_A"], self.data["publisher_B"]),
            ("Currency", self.data["currency_A"], self.data["currency_B"]),
            ("Cover Price", f"{self.data['cover_price_A']} {self.data['currency_A']}",
             f"{self.data['cover_price_B']} {self.data['currency_B']}"),
            ("Retail Price", f"{int(self.data['retail_price_A'])} HKD", f"{int(self.data['retail_price_B'])} HKD"),
            ("Cost", f"{int(self.data['cost_A'])} HKD", f"{int(self.data['cost_B'])} HKD"),
            ("Margin", f"{round(self.data['margin_A'], 1)}HKD", f"{round(self.data['margin_B'], 1)}HKD")
        ]

        for i, (label, value_A, value_B) in enumerate(results):
            ttk.Label(self.results_frame, text=label).grid(column=0, row=i, padx=10, pady=10)
            ttk.Label(self.results_frame, text=value_A).grid(column=1, row=i, padx=10, pady=10)
            ttk.Label(self.results_frame, text=value_B).grid(column=2, row=i, padx=10, pady=10)


    def reset_input_fields(self):
                self.cover_price_A.delete(0, 'end')
                self.currency_A.set("USD")
                self.publisher_name_A.delete(0, 'end')
                self.supplier_discount_A.delete(0, 'end')

                self.cover_price_B.delete(0, 'end')
                self.currency_B.set("USD")
                self.publisher_name_B.delete(0, 'end')
                self.supplier_discount_B.delete(0, 'end')


    def copy_comparison(self):
            publisher_name_A = self.publisher_name_A.get()
            publisher_name_B = self.publisher_name_B.get()

            cover_price_A = int(float(self.cover_price_A.get()))
            cover_price_B = int(float(self.cover_price_B.get()))

            currency_A = self.currency_A.get()
            currency_B = self.currency_B.get()

            retail_price_A = int(self.retail_price_A)
            retail_price_B = int(self.retail_price_B)

            cost_A = int(self.cost_A)
            cost_B = int(self.cost_B)

            margin_A = int(self.margin_A)
            margin_B = int(self.margin_B)

            comparison_text = f"{publisher_name_A}, {publisher_name_B}\n"
            comparison_text += f"{cover_price_A} {currency_A}, {cover_price_B} {currency_B}\n"
            comparison_text += f"{retail_price_A} HKD, {retail_price_B} HKD\n"
            comparison_text += f"{cost_A}, {cost_B}\n"
            comparison_text += f"{margin_A}HKD, {margin_B}HKD"

            pyperclip.copy(comparison_text)

    def export_to_file(self):
            publisher_name_A = self.publisher_name_A.get()
            publisher_name_B = self.publisher_name_B.get()

            cover_price_A = int(float(self.cover_price_A.get()))
            cover_price_B = int(float(self.cover_price_B.get()))

            currency_A = self.currency_A.get()
            currency_B = self.currency_B.get()

            retail_price_A = int(self.retail_price_A)
            retail_price_B = int(self.retail_price_B)

            cost_A = int(self.cost_A)
            cost_B = int(self.cost_B)

            margin_A = int(self.margin_A)
            margin_B = int(self.margin_B)

            data = {
                'Publisher': [publisher_name_A, publisher_name_B],
                'Cover Price': [f"{cover_price_A} {currency_A}", f"{cover_price_B} {currency_B}"],
                'Retail Price (HKD)': [retail_price_A, retail_price_B],
                'Cost': [cost_A, cost_B],
                'Margin': [f"{margin_A}HKD", f"{margin_B}HKD"],
            }

            df = pd.DataFrame(data)
            df.to_excel("comparison_results.xlsx", index=False, engine='openpyxl')

            tk.messagebox.showinfo("Exported", "Comparison results have been exported to 'comparison_results.xlsx'.")

#if __name__ == "__main__":
    #app = PriceCalculator()
    #app.mainloop()



