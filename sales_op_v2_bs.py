import pandas as pd
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from openpyxl import load_workbook
pd.set_option('display.max_columns', None)

class SalesReportOptimizer(Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Sales Report OP")
        self.include_suppliers = []
        self.exclude_keywords = []

        Button(self, text='Open', command=self.open_file).pack()

        # Include supplier entry
        self.include_supplier_label = ttk.Label(self, text="Include Supplier:")
        self.include_supplier_label.pack()
        self.include_supplier_entry = ttk.Entry(self)
        self.include_supplier_entry.pack()

        Button(self, text='Add Supplier', command=self.add_supplier).pack()

        # Exclude keyword entry
        self.exclude_keyword_label = ttk.Label(self, text="Exclude Keyword:")
        self.exclude_keyword_label.pack()
        self.exclude_keyword_entry = ttk.Entry(self)
        self.exclude_keyword_entry.pack()

        Button(self, text='Add Exclude Keyword', command=self.add_exclude_keyword).pack()

        # Filters display frame
        self.filters_frame = ttk.Frame(self)
        self.filters_frame.pack()

        Button(self, text="Remove All Filters", command=self.remove_all_filters).pack()

        Button(self, text="Optimize", command=self.optimize).pack()

        button_frame = Frame(self, width=300, height=300, bg='lightsteelblue2', relief='raised')
        button_frame.pack()

        save_as_button_excel = Button(button_frame, text='Export Excel', command=self.export_excel, bg='green', fg='white',
                                      font=('helvetica', 12, 'bold'))
        save_as_button_excel.pack(pady=75)

        self.var = IntVar()
        c = Checkbutton(self, text="Add Bestsellers", variable=self.var)
        c.pack()
        self.no_non_books = BooleanVar(value=False)
        no_non_books_checkbox = Checkbutton(
            self,
            text="No non-book",
            variable=self.no_non_books
        )
        no_non_books_checkbox.pack()

    def add_supplier(self):
        supplier = self.include_supplier_entry.get().lower()
        if supplier == "all":
            self.include_suppliers = ["all"]
        elif supplier not in self.include_suppliers:
            self.include_suppliers.append(supplier)
        self.update_filters_display()

    def add_exclude_keyword(self):
        keyword = self.exclude_keyword_entry.get()
        if keyword not in self.exclude_keywords:
            self.exclude_keywords.append(keyword)
            self.update_filters_display()

    def update_filters_display(self):
        for widget in self.filters_frame.winfo_children():
            widget.destroy()

        for supplier in self.include_suppliers:
            tag = ttk.Label(self.filters_frame, text=supplier, background="lightblue", relief="solid")
            tag.pack(side="left", padx=2, pady=2)

            remove_button = ttk.Button(self.filters_frame, text="x", command=lambda s=supplier: self.remove_supplier(s))
            remove_button.pack(side="left", padx=2, pady=2)

        for keyword in self.exclude_keywords:
            tag = ttk.Label(self.filters_frame, text=keyword, background="orange", relief="solid")
            tag.pack(side="left", padx=2, pady=2)

            remove_button = ttk.Button(self.filters_frame, text="x", command=lambda k=keyword: self.remove_exclude_keyword(k))
            remove_button.pack(side="left", padx=2, pady=2)

    def remove_supplier(self, supplier):
        if supplier in self.include_suppliers:
            self.include_suppliers.remove(supplier)
            self.update_filters_display()

    def remove_exclude_keyword(self, keyword):
        if keyword in self.exclude_keywords:
            self.exclude_keywords.remove(keyword)
            self.update_filters_display()

    def remove_all_filters(self):
        self.include_suppliers = []
        self.exclude_keywords = []
        self.update_filters_display()

    def open_file(self):

        file = filedialog.askopenfile(parent=self, mode='rb', title='Choose a file')
        if file is not None:
            self.data = pd.read_excel(file, header=0)
            messagebox.showinfo("File Load", "File load complete.")

    def optimize(self):

        if self.data is None:
            messagebox.showerror("Error", "No data loaded.")
            return

        data = self.data.copy()

        include_suppliers = [s.upper() for s in self.include_suppliers]
        exclude_keywords = [k.upper() for k in self.exclude_keywords]

        data.columns = data.columns.str.replace(' ', '_')
        data['Item_main_supplier'] = data['Item_main_supplier'].str.upper()

        if self.include_suppliers and self.include_suppliers[0].lower() == "all":
            pass

        else:
            if include_suppliers:
                include_suppliers.append('FEML')
                data = data[data['Item_main_supplier'].isin(include_suppliers)]
            else:
              data = data[data['Item_main_supplier'] == 'FEML']

        data = data[~data['Item_code'].isin(['BB'])]
        data = data.drop(columns=['Sub-Category', 'Imprint', 'Item_type'])
        data.columns = data.columns.str.replace('Inventory_warehouse', 'Shop')
        data.columns = data.columns.str.replace('Sum_of_sold_quantities', 'Sold')
        data.columns = data.columns.str.replace('Inventory_total:_Physical', 'Stock')
        if self.no_non_books.get():
            data = data[data['Item_code'].str.startswith("97")]
        for keyword in exclude_keywords:
            data = data[~data.apply(lambda x: x.astype(str).str.upper().str.contains(keyword).any(), axis=1)]

        data = data[
            ~data.apply(lambda x: x.astype(str).str.upper().str.contains(r'GOODS?[-\s]*VALUE|VALUE[-\s]*GOODS?').any(),
                        axis=1)]

        self.optimized_df = data
        messagebox.showinfo("Optimization", "File optimized!")

    def add_bestsellers(self, file_path):

        # Check for duplicates
        self.optimized_df.drop_duplicates(inplace=True)

        # Group by code and description
        bestsellers = self.optimized_df.groupby(['Item_description', 'Item_code'])['Sold'].sum().sort_values(
            ascending=False).head(150)

        # Reset index and merge
        bestsellers = bestsellers.reset_index()

        # Left merge to ensure one row per item
        bestsellers = pd.merge(bestsellers, self.optimized_df[['Item_description', 'Item_code', 'Item_main_supplier']],
                               how='left', on=['Item_description', 'Item_code'])

        # Drop duplicates
        bestsellers.drop_duplicates(subset=['Item_description', 'Item_code'], inplace=True)

        # Sort by total sold
        bestsellers = bestsellers.sort_values('Sold', ascending=False)

        # Split by supplier
        feml = bestsellers[bestsellers['Item_main_supplier'] == 'FEML']
        non_feml = bestsellers[bestsellers['Item_main_supplier'] != 'FEML']

        # Write sheets
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
            bestsellers.to_excel(writer, sheet_name='All Bestsellers')
            feml.to_excel(writer, sheet_name='FEML Bestsellers')
            non_feml.to_excel(writer, sheet_name='Non-FEML Bestsellers')

        # Add supplier column
        for df in [bestsellers, feml, non_feml]:
            df['Supplier'] = df['Item_main_supplier']
    def export_excel(self):
        # Default to .xlsx file format
        self.export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')

        # Export filtered data
        self.optimized_df.to_excel(self.export_file_path, index=False)

        # Check if adding bestsellers
        if self.var.get() == 1:
            self.add_bestsellers(self.export_file_path)

        messagebox.showinfo("Export", "File exported.")
