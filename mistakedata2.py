import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

DB_FILE = "mistake_data.json"


# ---------------- DATABASE ----------------
def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ---------------- Add Batch Window ----------------
class AddBatchWindow:
    def __init__(self, master):
        self.win = tk.Toplevel(master)
        self.win.title("Add New Batch")
        self.win.resizable(False, False)

        tk.Label(self.win, text="Batch Title:").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 2))
        self.title_entry = tk.Entry(self.win, width=60)
        self.title_entry.grid(row=0, column=1, pady=(8, 2), padx=8)

        # tree-like rows to add multiple records quickly
        tk.Label(self.win, text="Enter records (leave empty question to skip row)").grid(
            row=1, column=0, columnspan=2, sticky="w", padx=8
        )

        self.records_frame = tk.Frame(self.win)
        self.records_frame.grid(row=2, column=0, columnspan=2, padx=8, pady=6)

        header = ("Question", "Reason", "Tag")
        for c, h in enumerate(header):
            tk.Label(self.records_frame, text=h, font=("Arial", 9, "bold")).grid(row=0, column=c, padx=4, pady=2)

        self.row_entries = []
        # start with 3 rows
        for _ in range(3):
            self.add_row()

        btn_frame = tk.Frame(self.win)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text="Add Row", command=self.add_row).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Save Batch", command=self.save_batch).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Cancel", command=self.win.destroy).grid(row=0, column=2, padx=6)

    def add_row(self):
        r = len(self.row_entries) + 1
        q = tk.Entry(self.records_frame, width=50)
        q.grid(row=r, column=0, padx=4, pady=3)
        reason = tk.Entry(self.records_frame, width=30)
        reason.grid(row=r, column=1, padx=4, pady=3)
        tag = tk.Entry(self.records_frame, width=20)
        tag.grid(row=r, column=2, padx=4, pady=3)
        self.row_entries.append((q, reason, tag))

    def save_batch(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Batch title cannot be empty.")
            return

        records = []
        for q, r, t in self.row_entries:
            qv = q.get().strip()
            rv = r.get().strip()
            tv = t.get().strip()
            if qv:  # only save rows with question filled
                records.append({"question": qv, "reason": rv, "tag": tv})

        if not records:
            messagebox.showerror("Error", "Add at least one record (enter a question).")
            return

        batch = {
            "title": title,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "records": records
        }

        db = load_db()
        db.append(batch)
        save_db(db)
        messagebox.showinfo("Saved", f"Batch '{title}' saved with {len(records)} records.")
        self.win.destroy()


# ---------------- Edit Record Popup ----------------
class EditRecordPopup:
    def __init__(self, master, record, on_save):
        self.on_save = on_save
        self.win = tk.Toplevel(master)
        self.win.title("Edit Record")
        self.win.resizable(False, False)

        tk.Label(self.win, text="Question:").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 2))
        self.q_ent = tk.Entry(self.win, width=80)
        self.q_ent.grid(row=0, column=1, padx=8, pady=(8, 2))
        self.q_ent.insert(0, record.get("question", ""))

        tk.Label(self.win, text="Reason:").grid(row=1, column=0, sticky="w", padx=8, pady=2)
        self.r_ent = tk.Entry(self.win, width=80)
        self.r_ent.grid(row=1, column=1, padx=8, pady=2)
        self.r_ent.insert(0, record.get("reason", ""))

        tk.Label(self.win, text="Tag:").grid(row=2, column=0, sticky="w", padx=8, pady=2)
        self.t_ent = tk.Entry(self.win, width=80)
        self.t_ent.grid(row=2, column=1, padx=8, pady=2)
        self.t_ent.insert(0, record.get("tag", ""))

        btn_frame = tk.Frame(self.win)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Save", command=self.save).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Cancel", command=self.win.destroy).grid(row=0, column=1, padx=6)

    def save(self):
        q = self.q_ent.get().strip()
        r = self.r_ent.get().strip()
        t = self.t_ent.get().strip()
        if not q:
            messagebox.showerror("Error", "Question cannot be empty.")
            return
        self.on_save({"question": q, "reason": r, "tag": t})
        self.win.destroy()


# ---------------- Edit Batch Window (Treeview) ----------------
class EditBatchWindow:
    def __init__(self, master, batch_index):
        self.master = master
        self.batch_index = batch_index
        self.db = load_db()
        if batch_index < 0 or batch_index >= len(self.db):
            messagebox.showerror("Error", "Batch not found.")
            return
        self.batch = self.db[batch_index]

        self.win = tk.Toplevel(master)
        self.win.title(f"Edit Batch — {self.batch['title']}")
        self.win.geometry("900x550")

        # Top: editable title and date
        top_frame = tk.Frame(self.win)
        top_frame.pack(fill="x", padx=8, pady=6)
        tk.Label(top_frame, text="Title:").pack(side="left")
        self.title_var = tk.StringVar(value=self.batch["title"])
        self.title_entry = tk.Entry(top_frame, textvariable=self.title_var, width=60)
        self.title_entry.pack(side="left", padx=6)

        tk.Label(top_frame, text=f"Saved: {self.batch.get('date', '')}").pack(side="left", padx=6)
