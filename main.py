# main.py
import sys
from PySide6.QtWidgets import QApplication
from gui.main_gui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
