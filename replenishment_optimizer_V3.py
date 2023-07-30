import pandas as pd
from tkinter import *
from tkinter import messagebox, filedialog

class ReplenishmentOptimizer(Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Replenishment Optimizer")
        self.filters = []
        self.data = None

        Button(self, text='Open', command=self.open_file).pack()

        self.keyword_entry = Entry(self)
        self.keyword_entry.pack()
        self.keyword_entry.insert(0, "Enter keyword to exclude")
        self.keyword_entry.bind("<FocusIn>", self.clear_entry_field)
        self.keyword_entry.bind("<FocusOut>", self.reset_entry_field)

        Button(self, text="Add exclude keyword", command=self.add_exclude_keyword).pack()
        Button(self, text="Remove all filters", command=self.remove_all_filters).pack()
        Button(self, text="Optimize", command=self.optimize).pack()

        self.hq_stock_var = IntVar()
        Checkbutton(self, text="HQ stock", variable=self.hq_stock_var).pack()

        self.filter_display_frame = Frame(self)
        self.filter_display_frame.pack()

        button_frame = Frame(self, width=300, height=300, bg='lightsteelblue2', relief='raised')
        button_frame.pack()

        save_as_button_excel = Button(button_frame, text='Export Excel', command=self.export_excel, bg='green', fg='white',
                                      font=('helvetica', 12, 'bold'))
        save_as_button_excel.pack(pady=75)

    def clear_entry_field(self, event):
        self.keyword_entry.delete(0, END)

    def reset_entry_field(self, event):
        if not self.keyword_entry.get():
            self.keyword_entry.insert(0, "Enter keyword to exclude")

    def open_file(self):
        file = filedialog.askopenfile(parent=self, mode='rb', title='Choose a file')
        if file is not None:
            self.data = pd.read_excel(file, header=1)
            messagebox.showinfo("File Load", "File load complete.")

    def add_exclude_keyword(self):
        keyword = self.keyword_entry.get()
        if keyword and keyword not in self.filters:
            self.filters.append(keyword)
            self.update_filter_display()
            self.keyword_entry.delete(0, END)

    def remove_filter(self, keyword):
        self.filters.remove(keyword)
        self.update_filter_display()

    def remove_all_filters(self):
        self.filters.clear()
        self.update_filter_display()

    def update_filter_display(self):
        for widget in self.filter_display_frame.winfo_children():
            widget.destroy()

        for keyword in self.filters:
            tag = Label(self.filter_display_frame, text=keyword, bg='lightsteelblue2', bd=1, relief='solid')
            tag.pack(side=LEFT)
            remove_button = Button(self.filter_display_frame, text='x', command=lambda k=keyword: self.remove_filter(k))
            remove_button.pack(side=LEFT)

    def optimize(self):
        if self.data is not None:

            if self.hq_stock_var.get() == 1:

               self.data = self.data.drop(columns=['TYPE', 'SALES TERM'])
               self.data.columns = self.data.columns.str.replace('LIST PRICE', 'PRICE')
               self.data.columns = self.data.columns.str.replace('SOLD LAST', '')
               # Add new filter logic here
               self.data['BARCODE'] = self.data['BARCODE'].astype(str)
               self.data = self.data[self.data['BARCODE'].str.startswith(("97", "48"))]
            else:

                self.data = self.data.drop(columns=['SUPPLIER', 'TYPE', 'HQ SOH', 'PENDING TN (QTY)', 'SALES TERM'])

                self.data.columns = self.data.columns.str.replace('SOH', '')
                self.data.columns = self.data.columns.str.replace('LIST PRICE', 'PRICE')
                self.data.columns = self.data.columns.str.replace('SOLD LAST', '')
                # Add new filter logic here
                self.data['BARCODE'] = self.data['BARCODE'].astype(str)
                self.data = self.data[self.data['BARCODE'].str.startswith(("97", "48"))]
            for keyword in self.filters:
                keyword_lower = keyword.lower()
                self.data = self.data[
                    ~self.data.apply(lambda x: x.astype(str).str.lower().str.contains(keyword_lower).any(), axis=1)]

            messagebox.showinfo("Optimization", "File optimized!")
        else:
            messagebox.showerror("Error", "Please load a file first.")

    def export_excel(self):
        if self.data is not None:
            export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
            self.data.to_excel(export_file_path, index=None, header=True)
            messagebox.showinfo("Export", "File exported.")
        else:
            messagebox.showerror("Error", "Please load and optimize a file first.")



