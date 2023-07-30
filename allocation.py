import pandas as pd
from tkinter import filedialog, messagebox, Tk, Button, Label, StringVar
from openpyxl import load_workbook


class PreviewOptimizer:
    def __init__(self, root):
        self.root = root
        self.file_path = StringVar()
        self.df = None

        # Create buttons and labels
        self.open_file_button = Button(root, text="Open File", command=self.open_file)
        self.open_file_button.pack()

        self.optimize_button = Button(root, text="Optimize", command=self.optimize)
        self.optimize_button.pack()

        self.export_button = Button(root, text="Export File", command=self.export_file)
        self.export_button.pack()

        self.file_label = Label(root, textvariable=self.file_path)
        self.file_label.pack()

    def open_file(self):
        self.file_path.set(filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")]))
        self.df = pd.read_excel(self.file_path.get())
        messagebox.showinfo("Success", "File opened successfully!")

    def optimize(self):
        if self.df is None:
            messagebox.showerror("Error", "No file opened yet!")
            return

        # Group by 'Group' and 'Item' and sum 'Qty'
        self.df = self.df.groupby(['Group', 'Item'])['Qty'].sum().reset_index()

        # Sorting by 'Group' in descending order
        self.df = self.df.sort_values(by='Group', ascending=False)

        # Selecting only required columns
        self.df = self.df[['Group', 'Item', 'Qty']]
        messagebox.showinfo("Success", "Optimization done!")

    def export_file(self):
        if self.df is None:
            messagebox.showerror("Error", "No file opened yet!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            self.df.to_excel(writer, index=False)

        messagebox.showinfo("Success", "File exported successfully!")

if __name__ == "__main__":
    root = Tk()
    app = PreviewOptimizer(root)
    root.mainloop()