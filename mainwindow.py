from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QApplication
from PyQt6.QtCore import Qt
from childform import ChildForm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setFixedSize(500, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button1 = QPushButton("Open Child Form 1", self)
        self.layout.addWidget(self.button1)
        self.button1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.button1.clicked.connect(self.on_button1_click)

        self.button2 = QPushButton("Open Child Form 2", self)
        self.layout.addWidget(self.button2)
        self.button2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.button2.clicked.connect(self.on_button2_click)

        self.child_form1 = None
        self.child_form2 = None

    def on_button1_click(self):
        if not self.child_form1:
            self.child_form1 = ChildForm(self)
            self.child_form1.show()
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)

    def on_button2_click(self):
        if not self.child_form2:
            self.child_form2 = ChildForm(self)
            self.child_form2.show()
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)

    def enable_buttons(self):
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.child_form1 = None
        self.child_form2 = None
