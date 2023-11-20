import asyncio
from PyQt6.QtWidgets import (
    QFileDialog, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
from PyQt6.QtGui import QTextCursor
import sys


class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.app = QApplication(sys.argv)
        self.show()

    def init_ui(self):
        self.username_label = QLabel("Enter your username:")
        self.username_input = QLineEdit(self)
        self.username_input.setText('vgophap')
        self.password_label = QLabel("Enter your password:")
        self.password_input = QLineEdit(self)
        self.password_input.setText('adiletI1')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_using_wget)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.download_button)
        layout.addWidget(self.log_output)
        self.setLayout(layout)

    async def run_wget_command(self, wget_command):
        process = await asyncio.create_subprocess_shell(
            wget_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        async for line in process.stdout:
            self.append_log(line.decode(), "green")

        async for line in process.stderr:
            self.append_log(line.decode(), "red")

        await process.wait()

        if process.returncode == 0:
            self.append_log("Download completed successfully.", "green")
        else:
            self.append_log("Error occurred during download.", "red")

    def append_log(self, text, color):
        cursor = self.log_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        formatted_text = f'<span style="color: {color};">{text}</span>'
        cursor.insertHtml(formatted_text)
        self.log_output.setTextCursor(cursor)
        self.log_output.ensureCursorVisible()

    def download_using_wget(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Get the target directory for downloads
        target_dir = QFileDialog.getExistingDirectory(self, "Choose Target Directory")
        if not target_dir:
            self.append_log("No target directory selected. Exiting.", "red")
            return

        file_paths = QFileDialog.getOpenFileNames(self, "Choose Text File", "", "Text files (*.txt)")
        if not file_paths[0]:
            self.append_log("No file selected. Exiting.", "red")
            return

        text_file_path = file_paths[0][0]
        self.append_log("Selected text file: " + text_file_path, "green")

        # Prepare the wget command without SSL certificate verification
        wget_command = f'wget --no-check-certificate --keep-session-cookies --http-user={username} ' \
                       f'--http-password={password} --content-disposition --directory-prefix={target_dir} ' \
                       f'-i {text_file_path}'

        # Run the wget command asynchronously
        asyncio.run(self.run_wget_command(wget_command))


if __name__ == '__main__':
    downloader = Downloader()
    sys.exit(downloader.app.exec_())
