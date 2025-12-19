import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime

DB_FILE = "mistake_data.json"


# ---------------- DATABASE HELPERS ----------------
def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- ADD BATCH WINDOW ----------------
def open_add_window():
    add_win = tk.Toplevel(root)
    add_win.title("Add New Batch")
    add_win.geometry("400x400")

    tk.Label(add_win, text="Batch Title:").pack()
    title_entry = tk.Entry(add_win, width=40)
    title_entry.pack(pady=5)

    tk.Label(add_win, text="Enter Question:").pack()
    q_entry = tk.Entry(add_win, width=40)
    q_entry.pack()

    tk.Label(add_win, text="Reason:").pack()
    r_entry = tk.Entry(add_win, width=40)
    r_entry.pack()

    tk.Label(add_win, text="Tag:").pack()
    t_entry = tk.Entry(add_win, width=40)
    t_entry.pack()

    records = []

    def add_record():
        q = q_entry.get().strip()
        r = r_entry.get().strip()
        t = t_entry.get().strip()

        if q == "" or r == "" or t == "":
            messagebox.showerror("Error", "All fields required.")
            return

        records.append({"question": q, "reason": r, "tag": t})
        messagebox.showinfo("Added", "Record added!")
        q_entry.delete(0, tk.END)
        r_entry.delete(0, tk.END)
        t_entry.delete(0, tk.END)

    def save_batch():
        title = title_entry.get().strip()
        if title == "":
            messagebox.showerror("Error", "Title required.")
            return
        if len(records) == 0:
            messagebox.showerror("Error", "No records added.")
            return

        db = load_db()
        db.append({
            "title": title,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "records": records
        })
        save_db(db)
        messagebox.showinfo("Saved", "Batch saved successfully!")
        add_win.destroy()

    tk.Button(add_win, text="Add Record", command=add_record).pack(pady=5)
    tk.Button(add_win, text="Save Batch", command=save_batch).pack(pady=10)


# ---------------- VIEW BATCHES WINDOW ----------------
def open_view_window():
    view_win = tk.Toplevel(root)
    view_win.title("View Batches")
    view_win.geometry("500x400")

    db = load_db()

    tree = ttk.Treeview(view_win, columns=("title", "date", "count"), show="headings")
    tree.heading("title", text="Title")
    tree.heading("date", text="Date")
    tree.heading("count", text="Records")

    tree.pack(fill="both", expand=True)

    for batch in db:
        tree.insert("", tk.END, values=(batch["title"], batch["date"], len(batch["records"])))

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a batch to delete.")
            return

        index = tree.index(selected[0])

        confirm = messagebox.askyesno("Confirm", "Delete this batch?")
        if confirm:
            del db[index]
            save_db(db)
            tree.delete(selected[0])
            messagebox.showinfo("Deleted", "Batch deleted.")

    tk.Button(view_win, text="Delete Selected Batch", command=delete_selected).pack(pady=10)


# ---------------- MAIN GUI ----------------
root = tk.Tk()
root.title("Mistake App")
root.geometry("300x250")

tk.Label(root, text="Mistake Tracking App", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Add New Batch", width=20, command=open_add_window).pack(pady=10)
tk.Button(root, text="View / Delete Batches", width=20, command=open_view_window).pack(pady=10)
tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=10)

root.mainloop()
