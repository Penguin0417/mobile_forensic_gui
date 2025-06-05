# ui_main.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox
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
import subprocess

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mobile Forensic Triage")
        self.setGeometry(1200, 100, 365, 700)
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

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.navigate_back)

        self.download_btn = QPushButton("Download Selected File")
        # self.extract_btn.clicked.connect(self.extract_device_data)

        self.checklist = QListWidget()
        self.checklist.itemDoubleClicked.connect(self.navigate_forward)
        self.checklist.itemClicked.connect(self.select_folder)

        self.filter_box = QLineEdit()
        self.filter_box.setPlaceholderText("Filter content by keyword...")
        # self.filter_box.textChanged.connect(self.apply_filter)

        self.preview = QTableWidget(0, 2)
        self.preview.setColumnWidth(1, 240)
        self.preview.setHorizontalHeaderLabels(["Item Type", "Data"])

        self.export_pdf = QPushButton("Export to PDF")
        self.export_csv = QPushButton("Export to CSV")

        self.export_pdf.clicked.connect(lambda: export_data(self.preview, "pdf"))
        self.export_csv.clicked.connect(lambda: export_data(self.preview, "csv"))

        layout.addWidget(self.toggle_mode_btn)
        layout.addWidget(self.detect_btn)
        layout.addWidget(self.device_label)
        layout.addWidget(self.checklist)
        layout.addWidget(self.filter_box)
        layout.addWidget(self.download_btn)
        layout.addWidget(self.back_btn)
        layout.addWidget(self.preview)
        layout.addWidget(self.export_pdf)
        layout.addWidget(self.export_csv)
        self.central.setLayout(layout)

    def toggle_dark_mode(self):
        qss_path = os.path.join(os.path.dirname(__file__), "assets", "style.qss")
        try:
            with open(qss_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            self.device_label.setText("style.qss not found!")

    # def extract_device_data(self):
    #     if self.selected_file_path:
    #         extract_files([], specific_file=self.selected_file_path)
    #         self.device_label.setText(f"Extracted: {os.path.basename(self.selected_file_path)}")
    #     elif self.current_path:
    #         extract_files([], specific_folder=self.current_path)
    #         self.device_label.setText(f"Extracted folder: {self.current_path}")
    #     else:
    #         self.device_label.setText("Nothing to extract.")

    # def preview_content(self):
    #     self.preview.setRowCount(0)
    #     self.selected_file_path = None
    #     contents = get_device_folder(self.current_path)
    #     all_records = [(item, "", self.current_path) for item in contents]
    #     self.load_preview(all_records)

    # def apply_filter(self):
    #     text = self.filter_box.text().lower()
    #     for row in range(self.preview.rowCount()):
    #         visible = False
    #         for col in range(self.preview.columnCount()):
    #             item = self.preview.item(row, col)
    #             if item and text in item.text().lower():
    #                 visible = True
    #                 break
    #         self.preview.setRowHidden(row, not visible)

    # def handle_preview_double_click(self, row, column=0):
    #     name = self.preview.item(row, 0).text().strip()
    #     full_path = f"{self.current_path.rstrip('/')}/{name}"

    #     # Use 'ls -d path/' to check if it's a directory
    #     try:
    #         result = subprocess.check_output(["adb", "shell", "ls", "-d", f"{full_path}/"], stderr=subprocess.STDOUT, text=True, encoding='utf-8')
    #         # It's a folder
    #         self.current_path = full_path.strip()
    #         self.selected_file_path = None
    #         contents = get_device_folder(self.current_path)
    #         self.checklist.clear()
    #         self.checklist.addItems(contents)
    #         self.device_label.setText(f"Navigated into: {self.current_path}")
    #     except subprocess.CalledProcessError:
    #         # It's a file
    #         self.selected_file_path = full_path
    #         self.device_label.setText(f"Selected file: {name}")

    def navigate_forward(self, item):
        new_path = f"{self.current_path.rstrip('/')}/{item.text().strip('/')}"
        try:
            result = subprocess.check_output(["adb", "shell", "ls", "-d", f"{new_path}/"], stderr=subprocess.STDOUT, text=True, encoding='utf-8')
            # It's a folder
            self.current_path = new_path.strip()
            self.selected_file_path = None
            contents = get_device_folder(self.current_path)
            self.checklist.clear()
            self.checklist.addItems(contents)
            self.device_label.setText(f"Navigated into: {self.current_path}")
        except subprocess.CalledProcessError:
            # It's a file
            self.selected_file_path = new_path
            self.device_label.setText(f"Selected file: {item.text().strip('/')}")

    def navigate_back(self):
        if self.current_path and self.current_path != "/sdcard":
            self.current_path = '/'.join(self.current_path.strip('/').split('/')[:-1])
            self.current_path = f"/{self.current_path}" if self.current_path else "/sdcard"
            contents = get_device_folder(self.current_path)
            self.checklist.clear()
            self.checklist.addItems(contents)
            self.device_label.setText(f"Current path: {self.current_path}")

    def detect_device(self):
        if (get_device_info()):
            device_info = get_device_info()
            self.device_label.setText(f"Device: {device_info}")
            self.current_path = "/sdcard"
            folders = get_device_folder(self.current_path)
            self.checklist.clear()
            self.checklist.addItems(folders)
        else:
            self.device_label.setText(f"Device: No Devices/Emulators Found")

    def show_file_info(self):
        try:
            result = subprocess.check_output(
                ["adb", "shell", "stat", self.selected_file_path],
                stderr=subprocess.STDOUT,
                text=True, 
                encoding='utf-8'
            )

            # Split into lines
            lines = [line.strip() for line in result.strip().split('\n')]
            
            # Initialize dictionary
            info_dict = {}

            # Parse lines
            info_dict['File'] = lines[0].split(": ", 1)[1]

            # Parse size line
            size_parts = lines[1].split()
            info_dict['Size'] = size_parts[1]
            info_dict['Blocks'] = size_parts[3]
            info_dict['IO Blocks'] = size_parts[6]
            info_dict['Type'] = size_parts[7]

            # Parse device line
            device_parts = lines[2].split('\t ')
            info_dict['Device'] = device_parts[0].split(': ', 1)[1]
            info_dict['Inode'] = device_parts[1].split(': ', 1)[1]
            info_dict['Links'] = device_parts[2].split(': ', 1)[1]
            info_dict['Device type'] = device_parts[3].split(': ', 1)[1]

            # Parse Access line (permissions and UID/GID)
            access_perm = lines[3].split('\t')
            info_dict['Permissions'] = access_perm[0].split(': ')[1]
            info_dict['Uid'] = access_perm[1].split(': ')[1]
            info_dict['Gid'] = access_perm[2].split(': ')[1]

            # Timestamps
            info_dict['Access Time'] = lines[4].split(": ", 1)[1]
            info_dict['Modify Time'] = lines[5].split(": ", 1)[1]
            info_dict['Change Time'] = lines[6].split(": ", 1)[1]

            
            self.load_preview(info_dict)
            # msg = QMessageBox(self)
            # msg.setWindowTitle("File/Folder Info")
            # msg.setText(f"<pre>{result}</pre>")
            # msg.setStandardButtons(QMessageBox.Ok)
            # msg.exec_()
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Could not fetch info:\n{e.output}")

    def load_preview(self, records):
        self.preview.setRowCount(len(records))
        for i, (col1, col2) in enumerate(records.items()):
            self.preview.setItem(i, 0, QTableWidgetItem(col1))
            self.preview.setItem(i, 1, QTableWidgetItem(col2))

    def select_folder(self):
        current_file = self.checklist.currentItem().text().strip()
        self.selected_file_path = f"{self.current_path.rstrip('/')}/{current_file}"
        self.device_label.setText(f"Selected File: {self.selected_file_path}")
        self.show_file_info()
