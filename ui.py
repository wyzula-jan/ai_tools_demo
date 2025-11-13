from qtpy.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QDialog, QCheckBox
)
from qtpy.QtGui import QFont
from qtpy.QtCore import Qt

# Import your validation utilities
from utils import is_email_valid, is_strong_password


class RegistrationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Account")

        layout = QVBoxLayout(self)

        title = QLabel("Create New Account")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16))

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")

        create_btn = QPushButton("Create Account")
        create_btn.clicked.connect(self.handle_create)

        layout.addWidget(title)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.error_label)
        layout.addWidget(create_btn)

    def handle_create(self):
        email_val = self.email.text().strip()
        pwd_val = self.password.text()

        if not email_val or not pwd_val:
            self.error_label.setText("Please fill in all fields.")
            return

        if not is_email_valid(email_val):
            self.error_label.setText("Invalid email format.")
            return

        if not is_strong_password(pwd_val):
            self.error_label.setText(
                "Password must include uppercase, lowercase, digit, "
                "special character and be at least 8 characters long."
            )
            return

        self.error_label.setStyleSheet("color: green;")
        self.error_label.setText("Account created.")
        self.accept()


class MainAppWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("You are now logged in.")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20))
        layout.addWidget(title)


class LoginWindow(QWidget):
    def __init__(self, stack_widget: QStackedWidget):
        super().__init__()
        self.stack = stack_widget
        self.setWindowTitle("Login")

        layout = QVBoxLayout(self)

        title = QLabel("Welcome")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18))

        layout.addWidget(title)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.toggle_show_pwd = QCheckBox("Show password")
        self.toggle_show_pwd.stateChanged.connect(self.toggle_password_visibility)

        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.toggle_show_pwd)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        btn_box = QHBoxLayout()
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        btn_box.addStretch()
        btn_box.addWidget(login_btn)

        layout.addLayout(btn_box)

        link_box = QHBoxLayout()
        forgot_btn = QPushButton("Forgot Password")
        create_btn = QPushButton("Create Account")

        forgot_btn.clicked.connect(self.on_forgot_password)
        create_btn.clicked.connect(self.on_create_account)

        link_box.addWidget(forgot_btn)
        link_box.addWidget(create_btn)

        layout.addLayout(link_box)

    def toggle_password_visibility(self):
        if self.toggle_show_pwd.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def handle_login(self):
        email_value = self.email.text().strip()
        pwd_value = self.password.text()

        if not email_value:
            self.error_label.setText("Please enter your email address.")
            return

        if not is_email_valid(email_value):
            self.error_label.setText("Invalid email address format.")
            return

        if not pwd_value:
            self.error_label.setText("Please enter your password.")
            return

        if not is_strong_password(pwd_value):
            self.error_label.setText(
                "Password must include uppercase, lowercase, digit, "
                "special character and be at least 8 characters long."
            )
            return

        # Dummy authentication
        if email_value == "admin@example.com" and pwd_value == "Admin123!":
            self.error_label.setStyleSheet("color: green;")
            self.error_label.setText("Login successful.")
            self.stack.setCurrentIndex(1)
        else:
            self.error_label.setStyleSheet("color: red;")
            self.error_label.setText("Email or password is incorrect.")

    def on_forgot_password(self):
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setText("Password recovery is not implemented yet.")

    def on_create_account(self):
        dlg = RegistrationDialog()
        dlg.exec()


class App(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.login_screen = LoginWindow(self)
        self.main_screen = MainAppWindow()

        self.addWidget(self.login_screen)
        self.addWidget(self.main_screen)


if __name__ == "__main__":
    app = QApplication([])
    stack = App()
    stack.resize(400, 260)
    stack.show()
    app.exec()