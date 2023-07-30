import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime

def main():
    # Database setup
    conn = sqlite3.connect("project_manager.db")
    c = conn.cursor()

    # Check if the table exists and has a 'status' column
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='tasks' AND sql LIKE '%status%' AND sql LIKE '%date_created%'")
    table_exists = c.fetchone()[0]

    if not table_exists:
        c.execute("DROP TABLE IF EXISTS tasks")
        c.execute("""CREATE TABLE tasks (
                id INTEGER PRIMARY KEY,
                task TEXT,
                status TEXT,
                date_created TEXT
            )""")
        conn.commit()

    # Helper functions
    def add_task(task):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        c.execute("INSERT INTO tasks (task, status, date_created) VALUES (?, 'active', ?)", (task, current_date))
        conn.commit()
        refresh_active_tasks()

    def finish_task(task_id):
        c.execute("UPDATE tasks SET status = 'finished' WHERE id = ?", (task_id,))
        conn.commit()
        refresh_active_tasks()
        refresh_finished_tasks()

    def delete_task(task_id):
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        refresh_active_tasks()
        refresh_finished_tasks()

    def modify_task(task_id, new_task):
        c.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
        conn.commit()
        refresh_active_tasks()
        refresh_finished_tasks()

    def archive_finished_tasks():
        c.execute("UPDATE tasks SET status = 'archived' WHERE status = 'finished'")
        conn.commit()
        refresh_finished_tasks()

    def load_archived_tasks():
        archive_window = tk.Toplevel(root)
        archive_window.title("Archived Tasks")
        refresh_archived_tasks(archive_window)

    def sort_tasks_by_date():
        refresh_active_tasks(sorted_by_date=True)
    # Helper functions for context menu
    def on_task_right_click(event, task_id):
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label="Modify Task", command=lambda: modify_task_popup(task_id))
        menu.add_command(label="Delete Task", command=lambda: delete_task(task_id))
        menu.post(event.x_root, event.y_root)

    def modify_task_popup(task_id):
        modify_window = tk.Toplevel(root)
        modify_window.title("Modify Task")

        c.execute("SELECT task FROM tasks WHERE id = ?", (task_id,))
        task = c.fetchone()[0]

        entry = ttk.Entry(modify_window)
        entry.insert(0, task)
        entry.pack()

        save_button = ttk.Button(modify_window, text="Save", command=lambda: modify_task(task_id, entry.get()))
        save_button.pack()

    def configure_canvas(canvas, frame, scrollbar):
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)
        canvas.yview_moveto(0)
        frame.update_idletasks()
        frame.configure(width=canvas.winfo_width())

    def update_active_tasks(sorted_by_date=False):
        for widget in active_tasks_frame.winfo_children():
            widget.destroy()

        if sorted_by_date:
            c.execute("SELECT * FROM tasks WHERE status = 'active' ORDER BY date_created DESC")
        else:
            c.execute("SELECT * FROM tasks WHERE status = 'active'")

        tasks = c.fetchall()
        tasks.reverse()  # Reverse the list so the newest tasks come first

        for i, (task_id, task, status, date_created) in enumerate(tasks):
            # Check if the date_created is missing, and assign the current date as a default value
            if date_created is None:
                date_created = datetime.datetime.now().strftime('%Y-%m-%d')
                c.execute("UPDATE tasks SET date_created = ? WHERE id = ?", (date_created, task_id))
                conn.commit()

            chk_var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(active_tasks_frame, text=task, variable=chk_var,
                                  command=lambda task_id=task_id: finish_task(task_id))
            chk.pack(anchor='w', side='top')  # Using pack with side='top' option
            chk.bind("<Button-3>", lambda event, task_id=task_id: on_task_right_click(event, task_id))

        configure_canvas(active_tasks_canvas, active_tasks_frame, active_tasks_scrollbar)

    def refresh_active_tasks(sorted_by_date=False):
        for widget in active_frame.winfo_children():
            widget.destroy()

        ttk.Label(active_frame, text="Active Tasks").pack()

        # Starting entry widget
        starting_entry = ttk.Entry(active_frame)
        starting_entry.bind('<Return>', lambda e: add_task(starting_entry.get()))
        starting_entry.pack()

        global active_tasks_canvas, active_tasks_frame, active_tasks_scrollbar

        active_tasks_canvas = tk.Canvas(active_frame)
        active_tasks_canvas.pack(side='left', fill='both', expand=True)

        active_tasks_scrollbar = ttk.Scrollbar(active_frame, orient='vertical', command=active_tasks_canvas.yview)
        active_tasks_scrollbar.pack(side='right', fill='y')

        active_tasks_frame = ttk.Frame(active_tasks_canvas)
        active_tasks_canvas.create_window((0, 0), window=active_tasks_frame, anchor='nw')

        update_active_tasks(sorted_by_date)

    def sort_tasks_by_date():
        update_active_tasks(sorted_by_date=True)

    def update_finished_tasks():
        for widget in finished_tasks_frame.winfo_children():
            widget.destroy()

        c.execute("SELECT * FROM tasks WHERE status = 'finished'")
        for task_id, task, status, date_created in c.fetchall():
            lbl = ttk.Label(finished_tasks_frame, text=f"{task} ({date_created})")
            lbl.pack()
            lbl.bind("<Button-3>", lambda event, task_id=task_id: on_task_right_click(event, task_id))

        configure_canvas(finished_tasks_canvas, finished_tasks_frame, finished_tasks_scrollbar)

    def refresh_finished_tasks():
        for widget in finished_frame.winfo_children():
            widget.destroy()

        ttk.Label(finished_frame, text="Finished Tasks").pack()

        global finished_tasks_canvas, finished_tasks_frame, finished_tasks_scrollbar

        finished_tasks_canvas = tk.Canvas(finished_frame)
        finished_tasks_canvas.pack(side='left', fill='both', expand=True)

        finished_tasks_scrollbar = ttk.Scrollbar(finished_frame, orient='vertical', command=finished_tasks_canvas.yview)
        finished_tasks_scrollbar.pack(side='right', fill='y')

        finished_tasks_frame = ttk.Frame(finished_tasks_canvas)
        finished_tasks_canvas.create_window((0, 0), window=finished_tasks_frame, anchor='nw')

        update_finished_tasks()

    def refresh_archived_tasks(archive_window):
        for widget in archive_window.winfo_children():
            widget.destroy()

        c.execute("SELECT DISTINCT date_created FROM tasks WHERE status = 'archived' ORDER BY date_created DESC")
        dates = c.fetchall()

        for date_created, in dates:
            date_btn = ttk.Button(archive_window, text=date_created,
                                  command=lambda d=date_created: show_tasks_by_date(archive_window, d))
            date_btn.pack()

    def show_tasks_by_date(archive_window, date_created):
        for widget in archive_window.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.destroy()

        c.execute("SELECT * FROM tasks WHERE status = 'archived' AND date_created = ?", (date_created,))
        for task_id, task, status, date_created in c.fetchall():
            ttk.Label(archive_window, text=f"{task} ({date_created})").pack()

    # Create and configure the main window
    root = tk.Tk()
    root.title("Project Manager")

    # Active tasks frame
    active_frame = ttk.Frame(root)
    active_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    # Finished tasks frame
    finished_frame = ttk.Frame(root)
    finished_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

    # Sort tasks by date button
    sort_by_date_btn = ttk.Button(root, text="Sort Tasks by Date", command=sort_tasks_by_date)
    sort_by_date_btn.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

    # Archive buttons
    archive_btn = ttk.Button(root, text="Archive Finished Tasks", command=archive_finished_tasks)
    archive_btn.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

    load_archive_btn = ttk.Button(root, text="Load Archived Tasks", command=load_archived_tasks)
    load_archive_btn.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

    # Implement refresh functions
    refresh_active_tasks()
    refresh_finished_tasks()

    root.mainloop()

    if __name__ == "__main__":
        main()



