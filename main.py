import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from tempform import TempForm
from windform import WindForm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.temp_button = QPushButton("Open Temp Form", self)
        self.temp_button.clicked.connect(self.open_temp_form)
        self.layout.addWidget(self.temp_button)

        self.wind_button = QPushButton("Open Wind Form", self)
        self.wind_button.clicked.connect(self.open_wind_form)
        self.layout.addWidget(self.wind_button)

        self.temp_form = None
        self.wind_form = None

    def open_temp_form(self):
        if not self.temp_form:
            self.temp_form = TempForm()
            self.temp_form.closed.connect(self.enable_buttons)
            self.temp_button.setDisabled(True)
            self.temp_form.show()

    def open_wind_form(self):
        if not self.wind_form:
            self.wind_form = WindForm()
            self.wind_form.closed.connect(self.enable_buttons)
            self.wind_button.setDisabled(True)
            self.wind_form.show()

    def enable_buttons(self):
        if self.temp_form:
            self.temp_form = None
            self.temp_button.setDisabled(False)
        if self.wind_form:
            self.wind_form = None
            self.wind_button.setDisabled(False)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
