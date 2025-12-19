import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

DB_FILE = "mistake_db.json"


# ------------------ Helpers ------------------
def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ------------------ Main GUI ------------------
class MistakeApp:
    def __init__(self, root):
        self.root = root
        root.title("Mistake Tracker - Tkinter")
        root.geometry("850x520")
        root.configure(bg="#f1f1f1")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Mistake Tracker", bg="#f1f1f1",
                         font=("Helvetica", 20, "bold"))
        title.pack(pady=10)

        # ---------- Input Frame ----------
        input_frame = tk.Frame(self.root, bg="#f1f1f1")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Question:", bg="#f1f1f1").grid(row=0, column=0)
        tk.Label(input_frame, text="Reason:", bg="#f1f1f1").grid(row=0, column=2)
        tk.Label(input_frame, text="Tag:", bg="#f1f1f1").grid(row=0, column=4)

        self.q_entry = tk.Entry(input_frame, width=30)
        self.q_entry.grid(row=0, column=1, padx=5)

        self.reason_entry = tk.Entry(input_frame, width=20)
        self.reason_entry.grid(row=0, column=3, padx=5)

        self.tag_entry = tk.Entry(input_frame, width=20)
        self.tag_entry.grid(row=0, column=5, padx=5)

        # ---------- Buttons ----------
        btn_frame = tk.Frame(self.root, bg="#f1f1f1")
        btn_frame.pack(pady=5)

        add_button = tk.Button(btn_frame, text="Add Record", width=15, command=self.add_record)
        del_button = tk.Button(btn_frame, text="Delete Selected", width=15, command=self.delete_record)
        clear_button = tk.Button(btn_frame, text="Clear All", width=15, command=self.clear_table)

        add_button.grid(row=0, column=0, padx=10)
        del_button.grid(row=0, column=1, padx=10)
        clear_button.grid(row=0, column=2, padx=10)

        # ---------- Table ----------
        columns = ("question", "reason", "tag")
        self.table = ttk.Treeview(self.root, columns=columns, show="headings", height=15)

        for col in columns:
            self.table.heading(col, text=col.title(), anchor="center")
            self.table.column(col, anchor="center", width=200)

        self.table.pack(pady=10)

        # ---------- Bottom Buttons ----------
        bottom_frame = tk.Frame(self.root, bg="#f1f1f1")
        bottom_frame.pack(pady=5)

        save_btn = tk.Button(bottom_frame, text="Save Batch", width=20, command=self.save_batch)
        view_btn = tk.Button(bottom_frame, text="View Saved Batches", width=20, command=self.view_batches)
        exit_btn = tk.Button(bottom_frame, text="Exit", width=20, command=self.root.quit)

        save_btn.grid(row=0, column=0, padx=10)
        view_btn.grid(row=0, column=1, padx=10)
        exit_btn.grid(row=0, column=2, padx=10)

    # ---------- Add record ----------
    def add_record(self):
        q = self.q_entry.get().strip()
        reason = self.reason_entry.get().strip()
        tag = self.tag_entry.get().strip()

        if not q:
            messagebox.showwarning("Input Required", "Question cannot be empty.")
            return

        self.table.insert("", "end", values=(q, reason, tag))

        self.q_entry.delete(0, tk.END)
        self.reason_entry.delete(0, tk.END)
        self.tag_entry.delete(0, tk.END)
        self.q_entry.focus()

    # ---------- Delete selected row ----------
    def delete_record(self):
        sel = self.table.selection()
        if not sel:
            messagebox.showinfo("Select Row", "Please select a row to delete.")
            return
        for row in sel:
            self.table.delete(row)

    # ---------- Clear entire table ----------
    def clear_table(self):
        if messagebox.askyesno("Confirm", "Clear all records?"):
            for row in self.table.get_children():
                self.table.delete(row)

    # ---------- Save batch ----------
    def save_batch(self):
        rows = self.table.get_children()
        if not rows:
            messagebox.showinfo("Empty", "No records to save.")
            return

        title = simpledialog.askstring("Batch Title", "Enter title for this batch:")
        if not title:
            messagebox.showwarning("Required", "Batch title cannot be empty.")
            return

        batch = {
            "title": title,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "records": []
        }

        for row in rows:
            batch["records"].append({
                "question": self.table.item(row, "values")[0],
                "reason": self.table.item(row, "values")[1],
                "tag": self.table.item(row, "values")[2]
            })

        db = load_db()
        db.append(batch)
        save_db(db)

        messagebox.showinfo("Saved", f"Batch '{title}' saved successfully.")
        self.clear_table()

    # ---------- View saved batches ----------
    def view_batches(self):
        BatchViewer()


# ------------------ Batch Viewer Window ------------------
class BatchViewer:
    def __init__(self):
        self.db = load_db()

        self.win = tk.Toplevel()
        self.win.title("Saved Batches")
        self.win.geometry("650x450")

        left_frame = tk.Frame(self.win)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        right_frame = tk.Frame(self.win)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.listbox = tk.Listbox(left_frame, width=35)
        self.listbox.pack(fill="y")

        for b in self.db:
            self.listbox.insert("end", f"{b['title']} ({b['date']})")

        self.listbox.bind("<<ListboxSelect>>", self.show_details)

        del_btn = tk.Button(left_frame, text="Delete Batch", command=self.delete_batch)
        del_btn.pack(pady=5)

        self.text = tk.Text(right_frame, wrap="word")
        self.text.pack(fill="both", expand=True)

    def show_details(self, event):
        index = self.listbox.curselection()
        if not index:
            return
        b = self.db[index[0]]
        txt = f"Title: {b['title']}\nDate: {b['date']}\nRecords: {len(b['records'])}\n\n"
        for i, r in enumerate(b["records"], start=1):
            txt += f"{i}. Question: {r['question']}\n   Reason: {r['reason']}\n   Tag: {r['tag']}\n\n"

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", txt)

    def delete_batch(self):
        index = self.listbox.curselection()
        if not index:
            return
        if messagebox.askyesno("Confirm", "Delete this batch?"):
            del self.db[index[0]]
            save_db(self.db)
            self.listbox.delete(index)
            self.text.delete("1.0", tk.END)


# ------------------ Main ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MistakeApp(root)
    root.mainloop()
