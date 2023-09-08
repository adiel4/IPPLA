from PyQt6.QtWidgets import QDialog, QPushButton
from PyQt6.QtCore import pyqtSignal

class WindForm(QDialog):
    closed = pyqtSignal()  # Define a custom signal

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Wind Form")
        self.setGeometry(200, 200, 300, 150)

        self.button = QPushButton("Close Wind Form", self)
        self.button.clicked.connect(self.close)

    def closeEvent(self, event):
        self.closed.emit()  # Emit the custom signal when the form is closed
        event.accept()
