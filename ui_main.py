# ui_main.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QTableWidget, QTableWidgetItem,
    QFileDialog
)
from PyQt5.QtCore import Qt
import os
from utils.device_handler import (
    get_device_info,
    extract_files,
    get_call_logs,
    get_sms_messages,
    list_directory_contents,
    get_device_folder  # Added to fetch device folders via ADB
)
from utils.data_exporter import export_data

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mobile Forensic Triage")
        self.current_path = "/sdcard"
        self.selected_file_path = None
        self.setupUi()

    def setupUi(self):
        self.central = QWidget()
        self.setCentralWidget(self.central)

        layout = QVBoxLayout()
        self.toggle_mode_btn = QPushButton("Toggle Mode")
        self.toggle_mode_btn.clicked.connect(self.toggle_dark_mode)

        self.detect_btn = QPushButton("Detect Device")
        self.detect_btn.clicked.connect(self.detect_device)
        self.device_label = QLabel("Device: Not Connected")

        self.preview_btn = QPushButton("Preview Content")
        self.preview_btn.clicked.connect(self.preview_content)

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.navigate_back)

        self.extract_btn = QPushButton("Extract Device Data")
        self.extract_btn.clicked.connect(self.extract_device_data)

        self.checklist = QListWidget()
        self.checklist.itemClicked.connect(self.navigate_forward)

        self.filter_box = QLineEdit()
        self.filter_box.setPlaceholderText("Filter content by keyword...")
        self.filter_box.textChanged.connect(self.apply_filter)

        self.preview = QTableWidget(0, 3)
        self.preview.setHorizontalHeaderLabels(["Name/Time", "Content/Size", "Source"])
        self.preview.cellDoubleClicked.connect(self.handle_preview_double_click)

        self.export_pdf = QPushButton("Export to PDF")
        self.export_csv = QPushButton("Export to CSV")

        self.export_pdf.clicked.connect(lambda: export_data(self.preview, "pdf"))
        self.export_csv.clicked.connect(lambda: export_data(self.preview, "csv"))

        layout.addWidget(self.toggle_mode_btn)
        layout.addWidget(self.detect_btn)
        layout.addWidget(self.preview_btn)
        layout.addWidget(self.extract_btn)
        layout.addWidget(self.device_label)
        layout.addWidget(self.back_btn)
        layout.addWidget(self.checklist)
        layout.addWidget(self.filter_box)
        layout.addWidget(self.preview)
        layout.addWidget(self.export_pdf)
        layout.addWidget(self.export_csv)
        self.central.setLayout(layout)

    def adb_detect_device(self):
        device_info = get_device_info()
        self.device_label.setText(f"Device: {device_info}")

    def toggle_dark_mode(self):
        qss_path = os.path.join(os.path.dirname(__file__), "assets", "style.qss")
        try:
            with open(qss_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            self.device_label.setText("style.qss not found!")

    def extract_device_data(self):
        if self.selected_file_path:
            extract_files([], specific_file=self.selected_file_path)
            self.device_label.setText(f"Extracted: {os.path.basename(self.selected_file_path)}")
        elif self.current_path:
            extract_files([], specific_folder=self.current_path)
            self.device_label.setText(f"Extracted folder: {self.current_path}")
        else:
            self.device_label.setText("Nothing to extract.")

    def preview_content(self):
        self.preview.setRowCount(0)
        self.selected_file_path = None
        contents = get_device_folder(self.current_path)
        all_records = [(item, "", self.current_path) for item in contents]
        self.load_preview(all_records)

    def load_preview(self, records):
        self.preview.setRowCount(len(records))
        for i, (col1, col2, col3) in enumerate(records):
            self.preview.setItem(i, 0, QTableWidgetItem(col1))
            self.preview.setItem(i, 1, QTableWidgetItem(col2))
            self.preview.setItem(i, 2, QTableWidgetItem(col3))

    def apply_filter(self):
        text = self.filter_box.text().lower()
        for row in range(self.preview.rowCount()):
            visible = False
            for col in range(self.preview.columnCount()):
                item = self.preview.item(row, col)
                if item and text in item.text().lower():
                    visible = True
                    break
            self.preview.setRowHidden(row, not visible)

    def handle_preview_double_click(self, row, column):
        name = self.preview.item(row, 0).text()
        full_path = os.path.join(self.current_path, name)
        self.selected_file_path = full_path
        self.device_label.setText(f"Selected file: {name}")

    def navigate_forward(self, item):
        new_path = os.path.join(self.current_path, item.text())
        self.current_path = new_path
        self.selected_file_path = None
        contents = get_device_folder(self.current_path)
        self.checklist.clear()
        self.checklist.addItems(contents)
        self.device_label.setText(f"Current path: {self.current_path}")

    def navigate_back(self):
        if self.current_path and self.current_path != "/sdcard":
            self.current_path = os.path.dirname(self.current_path)
            contents = get_device_folder(self.current_path)
            self.checklist.clear()
            self.checklist.addItems(contents)
            self.device_label.setText(f"Current path: {self.current_path}")

    def detect_device(self):
        device_info = get_device_info()
        self.device_label.setText(f"Device: {device_info}")
        self.current_path = "/sdcard"
        folders = get_device_folder(self.current_path)
        self.checklist.clear()
        self.checklist.addItems(folders)
