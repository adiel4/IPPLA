import functools

from PyQt6.QtWidgets import QMessageBox


# Define a custom decorator
def require_file_path(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.file_path:
            message_box = QMessageBox(self)
            message_box.setWindowTitle("Dataset не выбран")
            message_box.setText("Dataset не выбран, загрузите или выберите нужный Dataset.")
            message_box.exec()
            return None
        return func(self)

    return wrapper
