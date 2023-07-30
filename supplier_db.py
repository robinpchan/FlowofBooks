import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd


# Database setup
conn = sqlite3.connect("supplier_list.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS suppliers (
             supplier_name TEXT,
             supplier_code TEXT,
             email TEXT,
             contact_person TEXT
             )""")
conn.commit()
def main():
    SupplierDB()
class SupplierDB(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Supplier Management")

        self.supplier_name = tk.StringVar()
        self.supplier_code = tk.StringVar()
        self.email = tk.StringVar()
        self.contact_person = tk.StringVar()
        self.search_field = tk.StringVar()

        tk.Label(self, text="Supplier Name").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.supplier_name).grid(row=0, column=1)

        tk.Label(self, text="Supplier Code").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.supplier_code).grid(row=1, column=1)

        tk.Label(self, text="Email").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.email).grid(row=2, column=1)

        tk.Label(self, text="Contact Person").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.contact_person).grid(row=3, column=1)

        tk.Button(self, text="Add Supplier", command=self.add_supplier).grid(row=4, column=0, columnspan=2)

        self.display = tk.Text(self, width=60, height=10, wrap=tk.WORD)
        self.display.grid(row=5, column=0, columnspan=2)

        tk.Button(self, text="Clear Display", command=self.clear_display).grid(row=6, column=0, columnspan=2)

        tk.Label(self, text="Search").grid(row=7, column=0)
        tk.Entry(self, textvariable=self.search_field).grid(row=7, column=1)

        tk.Button(self, text="Search", command=self.search).grid(row=8, column=0, columnspan=2)

        tk.Button(self, text="Export Display to File", command=self.export_display_to_file).grid(row=9, column=0, columnspan=2)

        tk.Button(self, text="Export Database to File", command=self.export_database_to_file).grid(row=10, column=0, columnspan=2)
        tk.Button(self, text="Modify Supplier List", command=self.modify_supplier_list).grid(row=11, column=0,
                                                                                             columnspan=2)

        self.display_suppliers()

        self.protocol("WM_DELETE_WINDOW", self.close_and_cleanup)

    def add_supplier(self):
        c.execute("INSERT INTO suppliers VALUES (:supplier_name, :supplier_code, :email, :contact_person)",
                  {
                      'supplier_name': self.supplier_name.get(),
                      'supplier_code': self.supplier_code.get(),
                      'email': self.email.get(),
                      'contact_person': self.contact_person.get()
                  })

        conn.commit()
        self.display_suppliers()


    def display_suppliers(self):
        records = c.execute("SELECT * FROM suppliers").fetchall()
        self.display.delete(1.0, tk.END)
        for record in records:
            self.display.insert(tk.END, f"{record[0]} {record[1]} {record[2]} {record[3]}\n")


    def clear_display(self):
        self.display.delete(1.0, tk.END)

    def reset_input(self):
        self.supplier_name.set("")
        self.supplier_code.set("")
        self.email.set("")
        self.contact_person.set("")
        self.search_field.set("")

    def search(self):
        search_query = self.search_field.get()
        results = c.execute("SELECT * FROM suppliers WHERE supplier_name LIKE ? "
                            "OR supplier_code LIKE ? "
                            "OR email LIKE ? "
                            "OR contact_person LIKE ?",
                            (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%")).fetchall()

        self.display.delete(1.0, tk.END)
        for result in results:
            self.display.insert(tk.END, f"{result[0]} {result[1]} {result[2]} {result[3]}\n")

    def export_display_to_file(self):
        content = self.display.get(1.0, tk.END)
        data = [line.split() for line in content.split('\n') if line]

        # Ensure each row has the same number of columns by adding empty strings for missing values
        max_columns = 4
        for row in data:
            if len(row) < max_columns:
                row.extend([""] * (max_columns - len(row)))

        df = pd.DataFrame(data, columns=['Supplier_Name', 'Supplier_Code', 'Email', 'Contact_Person'])
        df.to_excel("current_display.xlsx", index=False)

    def export_database_to_file(self):
        records = c.execute("SELECT * FROM suppliers").fetchall()
        columns = ['Supplier_Name', 'Supplier_Code', 'Email', 'Contact_Person']
        df = pd.DataFrame.from_records(records, columns=columns)

        # Replace NaN values with empty strings
        df.fillna("", inplace=True)

        df.to_excel("supplier_list.xlsx", index=False)

    def modify_supplier_list(self):
        ModifySupplierList(self)

    def close_and_cleanup(self):
        conn.close()
        self.destroy()

class ModifySupplierList(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.title("Modify Supplier List")

        self.tree = ttk.Treeview(self, columns=("Supplier Name", "Supplier Code", "Email", "Contact Person"), show="headings")
        self.tree.heading("Supplier Name", text="Supplier Name")
        self.tree.heading("Supplier Code", text="Supplier Code")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Contact Person", text="Contact Person")
        self.tree.grid(row=0, column=0, columnspan=2)

        self.populate_treeview()

        self.tree.bind("<Button-3>", self.show_context_menu)

        self.protocol("WM_DELETE_WINDOW", self.close_and_return)

    def populate_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        records = c.execute("SELECT * FROM suppliers").fetchall()

        for record in records:
            self.tree.insert("", tk.END, values=record)

    def show_context_menu(self, event):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_supplier)
        self.context_menu.add_command(label="Delete", command=self.delete_supplier)

        self.context_menu.tk_popup(event.x_root, event.y_root)

    def edit_supplier(self):
        selected_item = self.tree.selection()[0]
        supplier_data = self.tree.item(selected_item, "values")

        EditSupplier(self, supplier_data)

    def delete_supplier(self):
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning("No selection", "Please select a supplier from the list.")
            return

        item = selected_items[0]
        supplier_data = self.tree.item(item)["values"]

        if messagebox.askyesno("Delete supplier", f"Are you sure you want to delete {supplier_data[0]}?"):
            c.execute("DELETE FROM suppliers WHERE supplier_name = ? AND supplier_code = ?",
                      (supplier_data[0], supplier_data[1]))
            conn.commit()
            self.populate_treeview()

    def close_and_return(self):
        self.parent.focus_set()
        self.destroy()
class EditSupplier(tk.Toplevel):
    def __init__(self, parent, supplier_data):
        super().__init__()

        self.parent = parent
        self.title("Edit Supplier")

        self.supplier_name = tk.StringVar(value=supplier_data[0])
        self.supplier_code = tk.StringVar(value=supplier_data[1])
        self.email = tk.StringVar(value=supplier_data[2])
        self.contact_person = tk.StringVar(value=supplier_data[3])

        tk.Label(self, text="Supplier Name").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.supplier_name).grid(row=0, column=1)

        tk.Label(self, text="Supplier Code").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.supplier_code).grid(row=1, column=1)

        tk.Label(self, text="Email").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.email).grid(row=2, column=1)

        tk.Label(self, text="Contact Person").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.contact_person).grid(row=3, column=1)

        tk.Button(self, text="Save Edit", command=self.save_edit).grid(row=4, column=0)
        tk.Button(self, text="Cancel", command=self.destroy).grid(row=4, column=1)

    def save_edit(self):
        c.execute("""UPDATE suppliers SET
                     supplier_name = :supplier_name,
                     supplier_code = :supplier_code,
                     email = :email,
                     contact_person = :contact_person
                     WHERE supplier_code = :old_supplier_code""",
                  {
                      'supplier_name': self.supplier_name.get(),
                      'supplier_code': self.supplier_code.get(),
                      'email': self.email.get(),
                      'contact_person': self.contact_person.get(),
                      'old_supplier_code': self.supplier_code.get()
                  })

        conn.commit()
        self.parent.populate_treeview()
        self.destroy()

#if __name__ == "__main__":
 #   main()



