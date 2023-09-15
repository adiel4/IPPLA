import os
import sys
from turtledemo.chaos import h

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListView, QGridLayout, \
    QLabel, QFileDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal, QStringListModel

import decorators
from tempform import TempForm
from windform import WindForm


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.list_model = None
        self.files_caption = None
        self.load_button = None
        self.files_list = None
        self.dataset = None
        self.wind_button = None
        self.layout = None
        self.central_widget = None
        self.temp_button = None
        self.init_ui()
        self.temp_form = None
        self.wind_form = None

    def init_ui(self):
        self.setWindowTitle("Главное окно")

        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - 400) // 2
        y = (screen.height() - 200) // 2
        self.setGeometry(x, y, 400, 200)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        grid_layout = QGridLayout()

        self.files_list = QListView(self)
        grid_layout.addWidget(self.files_list, 0, 1, 1, 2)
        self.files_list.clicked.connect(self.update_file_path)

        self.files_caption = QLabel('Список файлов', self)
        self.files_caption.alignment()
        grid_layout.addWidget(self.files_list, 0, 0)

        self.load_button = QPushButton("Загрузка", self)
        self.load_button.clicked.connect(self.load_files_from_folder)
        grid_layout.addWidget(self.load_button, 1, 0)

        self.temp_button = QPushButton("Открыть форму Температуры", self)
        self.temp_button.clicked.connect(self.open_temp_form)
        grid_layout.addWidget(self.temp_button, 1, 2)

        self.wind_button = QPushButton("Открыть форму Ветра", self)
        self.wind_button.clicked.connect(self.open_wind_form)
        grid_layout.addWidget(self.wind_button, 1, 1)

        self.list_model = QStringListModel()
        self.files_list.setModel(self.list_model)

        self.temp_form = None
        self.wind_form = None
        self.layout.addLayout(grid_layout)

    def load_files_from_folder(self):
        directory_path = QFileDialog.getExistingDirectory(self, "Choose Directory")
        existing_items = self.list_model.stringList()

        if directory_path:
            if directory_path in existing_items:
                message_box = QMessageBox(self)
                message_box.setWindowTitle("Dataset уже в списке")
                message_box.setText("Этот Dataset уже в списке.")
                message_box.exec()
                return
            file_list = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            if all(not f.lower().endswith('.nc') for f in file_list):
                message_box = QMessageBox(self)
                message_box.setWindowTitle("No Dataset Found")
                message_box.setText("Не все файлы в папке имеют формат .nc или .nc4")
                message_box.exec()
                return

            updated_items = existing_items + [directory_path]
            self.list_model.setStringList(updated_items)
            self.file_path = directory_path
            index = self.list_model.index(len(updated_items) - 1)
            self.files_list.setCurrentIndex(index)

            message_box = QMessageBox(self)
            message_box.setWindowTitle("Dataset загружен")
            message_box.setText("Новый Dataset загружен.")
            message_box.exec()

    @decorators.require_file_path
    def open_temp_form(self):
        if not self.temp_form:
            self.temp_form = TempForm(self)
            self.temp_form.closed.connect(self.enable_buttons)
            self.temp_button.setDisabled(True)
            self.temp_form.show()

    @decorators.require_file_path
    def open_wind_form(self):
        if not self.wind_form:
            self.wind_form = WindForm(self)
            self.wind_form.closed.connect(self.enable_buttons)
            self.wind_button.setDisabled(True)
            self.wind_form.show()

    def update_file_path(self, index):
        selected_item = self.list_model.data(index)
        self.file_path = selected_item
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Dataset изменен")
        message_box.setText("Dataset выбран, можете продолжить работу.")
        message_box.exec()

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
