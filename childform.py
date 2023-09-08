from PyQt6.QtWidgets import QWidget

class ChildForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Child Form")
        self.setGeometry(100, 100, 300, 200)

    def closeEvent(self, event):
        self.parent().enable_buttons()  # Call the parent's method to enable buttons
        event.accept()
