from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog,
    QDialog, QListWidget, QTextEdit
)
import sys
import json
import os
from datetime import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

DB_FILE = "mistake_db.json"
GSHEET_CREDENTIALS = "credentials.json"  # service account JSON
GSHEET_NAME = "Mistake Tracker"          # Google Sheet name

# ----------------- helpers -----------------
def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ----------------- Google Sheets -----------------
def upload_batches_to_sheet():
    db = load_db()
    try:
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GSHEET_CREDENTIALS, scope)
        client = gspread.authorize(creds)
        sheet = client.open(GSHEET_NAME).sheet1
        sheet.clear()
        sheet.append_row(["Batch Title", "Date", "Question", "Reason", "Tag"])
        for batch in db:
            for rec in batch["records"]:
                sheet.append_row([batch["title"], batch["date"], rec["question"], rec["reason"], rec["tag"]])
        QMessageBox.information(None, "Success", "All batches uploaded to Google Sheets!")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to upload: {e}")

# ----------------- Excel export -----------------
def export_batch_to_excel(table):
    if table.rowCount() == 0:
        QMessageBox.information(None, "No records", "No records to export.")
        return

    title, ok = QInputDialog.getText(None, "Batch Title", "Enter title for this batch:")
    if not ok or not title.strip():
        QMessageBox.warning(None, "Title required", "Batch title cannot be empty.")
        return
    title = title.strip()

    data = []
    for r in range(table.rowCount()):
        question = table.item(r, 0).text() if table.item(r,0) else ""
        reason = table.item(r, 1).text() if table.item(r,1) else ""
        tag = table.item(r, 2).text() if table.item(r,2) else ""
        data.append({"Question": question, "Reason": reason, "Tag": tag})

    df = pd.DataFrame(data)
    filename = f"{title}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    QMessageBox.information(None, "Exported", f"Batch exported to '{filename}' successfully.")

# ----------------- Main Window -----------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mistake Tracker (PyQt)")
        self.resize(800, 520)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Input row
        form_layout = QHBoxLayout()
        self.q_input = QLineEdit(); self.q_input.setPlaceholderText("Question / Short description")
        self.reason_input = QLineEdit(); self.reason_input.setPlaceholderText("Reason")
        self.tag_input = QLineEdit(); self.tag_input.setPlaceholderText("Tag (e.g., physics,math)")
        form_layout.addWidget(QLabel("Question:"))
        form_layout.addWidget(self.q_input)
        form_layout.addWidget(QLabel("Reason:"))
        form_layout.addWidget(self.reason_input)
        form_layout.addWidget(QLabel("Tag:"))
        form_layout.addWidget(self.tag_input)
        main_layout.addLayout(form_layout)

        # Buttons under inputs
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Record")
        add_btn.clicked.connect(self.add_record)
        del_btn = QPushButton("Delete Selected Record")
        del_btn.clicked.connect(self.delete_selected_record)
        clear_btn = QPushButton("Clear Table")
        clear_btn.clicked.connect(self.clear_table)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(clear_btn)
        main_layout.addLayout(btn_layout)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Question", "Reason", "Tag"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        main_layout.addWidget(self.table)

        # Bottom buttons: Save, View, Export, Sync, Exit
        bottom_layout = QHBoxLayout()
        save_batch_btn = QPushButton("Save Batch")
        save_batch_btn.clicked.connect(self.save_batch)
        view_batches_btn = QPushButton("View Batches")
        view_batches_btn.clicked.connect(self.open_view_batches)
        export_btn = QPushButton("Export to Excel")
        export_btn.clicked.connect(lambda: export_batch_to_excel(self.table))
        sync_btn = QPushButton("Sync to Google Sheets")
        sync_btn.clicked.connect(upload_batches_to_sheet)
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        bottom_layout.addWidget(save_batch_btn)
        bottom_layout.addWidget(view_batches_btn)
        bottom_layout.addWidget(export_btn)
        bottom_layout.addWidget(sync_btn)
        bottom_layout.addWidget(exit_btn)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    # ----------------- Table operations -----------------
    def add_record(self):
        q = self.q_input.text().strip()
        reason = self.reason_input.text().strip()
        tag = self.tag_input.text().strip()
        if not q:
            QMessageBox.warning(self, "Input required", "Please enter a question/description.")
            return
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(q))
        self.table.setItem(row, 1, QTableWidgetItem(reason))
        self.table.setItem(row, 2, QTableWidgetItem(tag))
        self.q_input.clear()
        self.reason_input.clear()
        self.tag_input.clear()

    def delete_selected_record(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.information(self, "No selection", "Select a row to delete.")
            return
        for idx in sorted([r.row() for r in selected], reverse=True):
            self.table.removeRow(idx)

    def clear_table(self):
        cnt = self.table.rowCount()
        if cnt == 0:
            return
        if QMessageBox.question(self, "Confirm", f"Clear all {cnt} records?") == QMessageBox.Yes:
            self.table.setRowCount(0)

    # ----------------- Save Batch -----------------
    def save_batch(self):
        if self.table.rowCount() == 0:
            QMessageBox.information(self, "No records", "No records to save.")
            return

        # Batch title
        title, ok = QInputDialog.getText(self, "Batch Title", "Enter title for this batch:")
        if not ok or not title.strip():
            QMessageBox.warning(self, "Title required", "Batch title cannot be empty.")
            return
        title = title.strip()

        # Batch date (manual)
        date_str, ok = QInputDialog.getText(self, "Batch Date", 
                                            "Enter batch date (YYYY-MM-DD) or leave blank for today:")
        if not ok:
            return
        date_str = date_str.strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                date_str += " 00:00:00"
            except ValueError:
                QMessageBox.warning(self, "Invalid date", "Date format must be YYYY-MM-DD. Using today instead.")
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create batch
        batch = {"title": title, "date": date_str, "records": []}
        for r in range(self.table.rowCount()):
            q = self.table.item(r, 0).text() if self.table.item(r,0) else ""
            reason = self.table.item(r, 1).text() if self.table.item(r,1) else ""
            tag = self.table.item(r, 2).text() if self.table.item(r,2) else ""
            batch["records"].append({"question": q, "reason": reason, "tag": tag})

        db = load_db()
        db.append(batch)
        save_db(db)
        QMessageBox.information(self, "Saved", f"Saved batch '{title}' with {len(batch['records'])} records.")
        self.table.setRowCount(0)

    def open_view_batches(self):
        dialog = ViewBatchesDialog(self)
        dialog.exec_()

# ----------------- Batches Viewer Dialog -----------------
class ViewBatchesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("View Saved Batches")
        self.resize(700, 420)
        self.db = load_db()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        self.list_widget = QListWidget()
        for b in self.db:
            self.list_widget.addItem(f"{b['title']}  ({b['date']})  [{len(b['records'])} recs]")
        self.list_widget.currentRowChanged.connect(self.display_selected_batch)
        left_layout.addWidget(QLabel("Saved Batches:"))
        left_layout.addWidget(self.list_widget)
        btn_del = QPushButton("Delete Selected Batch")
        btn_del.clicked.connect(self.delete_selected_batch)
        left_layout.addWidget(btn_del)
        layout.addLayout(left_layout, 2)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Batch Details:"))
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        right_layout.addWidget(self.detail_text)
        layout.addLayout(right_layout, 3)

        self.setLayout(layout)
        if self.db:
            self.list_widget.setCurrentRow(0)

    def display_selected_batch(self, index):
        if index < 0 or index >= len(self.db):
            self.detail_text.clear()
            return
        b = self.db[index]
        lines = [f"Title: {b['title']}", f"Date: {b['date']}", f"Records: {len(b['records'])}", "-"*40]
        for i, r in enumerate(b['records'], start=1):
            lines.append(f"{i}. Q: {r.get('question','')}")
            lines.append(f"    Reason: {r.get('reason','')}")
            lines.append(f"    Tag: {r.get('tag','')}")
        self.detail_text.setPlainText("\n".join(lines))

    def delete_selected_batch(self):
        idx = self.list_widget.currentRow()
        if idx < 0:
            QMessageBox.information(self, "Select", "Choose a batch to delete.")
            return
        b = self.db[idx]
        if QMessageBox.question(self, "Confirm Delete", f"Delete batch '{b['title']}'? This cannot be undone.") == QMessageBox.Yes:
            del self.db[idx]
            save_db(self.db)
            self.list_widget.takeItem(idx)
            self.detail_text.clear()
            QMessageBox.information(self, "Deleted", "Batch removed.")

# ----------------- run -----------------
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
