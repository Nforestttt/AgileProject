from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Signal


class LoginWindow(QWidget):

    login_success = Signal()

    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("ui/login.ui")
        ui_file.open(QFile.ReadOnly)

        self.ui = loader.load(ui_file)
        ui_file.close()

        layout = QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)

        self.ui.pushButton.clicked.connect(self.login)

    def login(self):
        print("login success")
        self.login_success.emit()