# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_main import Ui_MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_MainWindow()   # Already inherits QMainWindow and sets up UI
    window.show()
    sys.exit(app.exec_())
