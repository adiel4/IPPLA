import asyncio
import subprocess
from PyQt6.QtWidgets import (
    QFileDialog, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import sys
import os


class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.app = QApplication(sys.argv)
        self.show()

    def init_ui(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - 800) // 2
        y = (screen.height() - 400) // 2
        self.setGeometry(x, y, 800, 400)
        self.username_label = QLabel("Введите пользователя:")
        self.username_input = QLineEdit(self)
        self.username_input.setText('vgophap')
        self.password_label = QLabel("Введите пароль:")
        self.password_input = QLineEdit(self)
        self.password_input.setText('adiletI1')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.download_button = QPushButton("Скачать")
        self.download_button.clicked.connect(self.download_using_wget)
        self.log_output = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.download_button)
        layout.addWidget(self.log_output)
        self.setLayout(layout)

    @staticmethod
    def show_success_message():
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText("Download completed successfully.")
        msg_box.exec()

    async def run_wget_command(self, wget_command):
        process = await asyncio.create_subprocess_shell(
            wget_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        async for line in process.stdout:
            self.log_output.append(line.decode())

        async for line in process.stderr:
            self.log_output.append(line.decode())

        await process.wait()
        print(process.returncode)
        if process.returncode in (0, 4):
            self.log_output.append("Download completed successfully.")
            self.show_success_message()
        else:
            self.log_output.append("Error occurred during download.")

    def download_using_wget(self):
        username = self.username_input.text()
        password = self.password_input.text()

        target_dir = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if not target_dir:
            self.log_output.append("Не выбрана папка.")
            return

        file_paths = QFileDialog.getOpenFileNames(self, "Choose Text File", "", "Text files (*.txt)")
        if not file_paths[0]:
            self.log_output.append("Не выбран файл.")
            return

        text_file_path = file_paths[0][0]
        self.log_output.append("Selected text file: " + text_file_path)

        wget_command = f'wget --no-check-certificate --keep-session-cookies --http-user={username} ' \
                       f'--http-password={password} --content-disposition --directory-prefix={target_dir} ' \
                       f'-i {text_file_path}'

        self.download_button.setDisabled(True)
        asyncio.run(self.run_wget_command(wget_command))
        self.download_button.setDisabled(False)


if __name__ == '__main__':
    downloader = Downloader()
    sys.exit(downloader.app.exec())
