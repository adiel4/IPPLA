import os
import re
import aiohttp
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (
    QFileDialog, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
import sys
import asyncio


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
        self.username_label = QLabel("Enter username:")
        self.username_input = QLineEdit(self)
        self.username_input.setText('vgophap')
        self.password_label = QLabel("Enter password:")
        self.password_input = QLineEdit(self)
        self.password_input.setText('adiletI1')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download)
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

    @pyqtSlot()
    def download(self):
        username = self.username_input.text()
        password = self.password_input.text()
        target_dir = QFileDialog.getExistingDirectory(self, "Choose a directory")
        if not target_dir:
            self.log_output.append("No directory selected.")
            return
        file_paths = QFileDialog.getOpenFileNames(self, "Choose a text file", "", "Text files (*.txt)")
        if not file_paths[0]:
            self.log_output.append("No file selected.")
            return

        for file_path in file_paths[0]:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    asyncio.run(self.download_file(username, password, line, target_dir))

    async def download_file(self, username, password, url, target_dir):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, auth=aiohttp.BasicAuth(username, password), ssl=False) as response:
                if response.status == 200:
                    date_match = re.search(r'\d{8}', url)
                    if date_match:
                        date = date_match.group()
                        extension = os.path.splitext(url)[-1]
                        filename = f"{date}{extension}"
                        save_path = os.path.join(target_dir, filename)
                        with open(save_path, 'wb') as f:
                            f.write(await response.read())
                            self.log_output.append(f"Downloaded: {url}")
                else:
                    self.log_output.append(f"Failed to download: {url}")


if __name__ == '__main__':
    downloader = Downloader()
    sys.exit(downloader.app.exec())
