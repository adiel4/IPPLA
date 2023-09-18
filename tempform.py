from PyQt6.QtWidgets import QDialog, QPushButton, QApplication
from PyQt6.QtCore import pyqtSignal
import dataset


class TempForm(QDialog):
    closed = pyqtSignal()

    def __init__(self, file_path, parent=None):
        super().__init__(parent)

        self.dataset = dataset.Dataset()
        self.dataset.load_from_directory(file_path)

        self.setWindowTitle("Температура")
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - 1000) // 2
        y = (screen.height() - 500) // 2
        self.setGeometry(x, y, 1000, 500)

        self.close_button = QPushButton("Закрыть", self)
        self.close_button.clicked.connect(self.close)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
