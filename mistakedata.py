import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATABASE_FILE = "database.json"

# Load data
def load_data():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    return []

# Save data
def save_data(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Add record
def add_record():
    question = question_entry.get()
    q_type = type_var.get()
    reason = reason_entry.get()
    tags = tags_entry.get()

    if question == "" or q_type == "":
        messagebox.showerror("Error", "Please enter question and type")
        return

    record = {
        "question": question,
        "type": q_type,
        "reason": reason,
        "tags": [t.strip() for t in tags.split(",")],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data = load_data()
    data.append(record)
    save_data(data)

    messagebox.showinfo("Success", "Record added!")
    question_entry.delete(0, tk.END)
    reason_entry.delete(0, tk.END)
    tags_entry.delete(0, tk.END)

# View all records
def view_records():
    data = load_data()
    display.delete(1.0, tk.END)

    if not data:
        display.insert(tk.END, "No records found.\n")
        return

    for i, r in enumerate(data, 1):
        display.insert(tk.END, f"--- Record {i} ---\n")
        display.insert(tk.END, f"Question: {r['question']}\n")
        display.insert(tk.END, f"Type: {r['type']}\n")
        display.insert(tk.END, f"Reason: {r['reason']}\n")
        display.insert(tk.END, f"Tags: {', '.join(r['tags'])}\n")
        display.insert(tk.END, f"Date: {r['date']}\n\n")

# GUI Window
root = tk.Tk()
root.title("Question Mistake Database")
root.geometry("600x600")

tk.Label(root, text="Question:").pack()
question_entry = tk.Entry(root, width=60)
question_entry.pack()

tk.Label(root, text="Type (wrong/timeout):").pack()
type_var = tk.StringVar()
type_box = ttk.Combobox(root, textvariable=type_var, values=["wrong", "timeout"])
type_box.pack()

tk.Label(root, text="Reason:").pack()
reason_entry = tk.Entry(root, width=60)
reason_entry.pack()

tk.Label(root, text="Tags (comma separated):").pack()
tags_entry = tk.Entry(root, width=60)
tags_entry.pack()

tk.Button(root, text="Add Record", command=add_record).pack(pady=10)
tk.Button(root, text="View Records", command=view_records).pack(pady=5)

display = tk.Text(root, height=18, width=70)
display.pack(pady=10)

root.mainloop()

