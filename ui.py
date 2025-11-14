from qtpy.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QDialog, QCheckBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QGridLayout, QHeaderView
)
from qtpy.QtGui import QFont
from qtpy.QtCore import Qt

# Import your validation utilities
from utils import (
    is_email_valid,
    is_strong_password,
    load_user_database,
    get_usage_summary,
)


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
    """
    Container for the authenticated experience.
    """
    TABLE_COLUMNS = [
        ("id", "ID"),
        ("name", "Name"),
        ("email", "Email"),
        ("role", "Role"),
        ("active", "Active"),
        ("login_count", "Logins"),
    ]

    def __init__(self, data_loader=load_user_database, summary_builder=get_usage_summary):
        super().__init__()
        self.setWindowTitle("User Workspace")
        self.data_loader = data_loader
        self.summary_builder = summary_builder
        self.user_data = []
        self.usage_summary = {}
        self.dashboard_labels = {}

        layout = QVBoxLayout(self)
        header = QLabel("User Workspace")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 20))
        layout.addWidget(header)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.welcome_tab = self._build_welcome_tab()
        self.database_tab = self._build_database_tab()
        self.dashboard_tab = self._build_dashboard_tab()

        self.tabs.addTab(self.welcome_tab, "Welcome")
        self.tabs.addTab(self.database_tab, "Database")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        self.refresh_data()

    def _build_welcome_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.welcome_label = QLabel("Welcome! Select a section to get started.")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setFont(QFont("Arial", 16))

        helper = QLabel(
            "Use the tabs above to review the user database or see usage analytics."
        )
        helper.setWordWrap(True)
        helper.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(self.welcome_label)
        layout.addWidget(helper)
        layout.addStretch()
        return widget

    def _build_database_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        description = QLabel("User database snapshot")
        description.setAlignment(Qt.AlignLeft)
        description.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(description)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.TABLE_COLUMNS))
        self.table_widget.setHorizontalHeaderLabels([col[1] for col in self.TABLE_COLUMNS])
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_widget)
        return widget

    def _build_dashboard_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        intro = QLabel("Usage overview")
        intro.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(intro)

        grid = QGridLayout()
        stats = [
            ("total_users", "Total users"),
            ("active_users", "Active users"),
            ("inactive_users", "Inactive users"),
            ("total_logins", "Total logins"),
            ("average_logins", "Avg. logins / user"),
        ]
        for row, (key, label) in enumerate(stats):
            name_label = QLabel(label + ":")
            value_label = QLabel("-")
            value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            value_label.setObjectName(f"stat_{key}")
            grid.addWidget(name_label, row, 0)
            grid.addWidget(value_label, row, 1)
            self.dashboard_labels[key] = value_label

        layout.addLayout(grid)

        roles_title = QLabel("Top roles")
        roles_title.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(roles_title)

        self.roles_label = QLabel("No data")
        self.roles_label.setWordWrap(True)
        layout.addWidget(self.roles_label)
        layout.addStretch()
        return widget

    def refresh_data(self):
        """
        Reloads data from disk and refreshes UI components.
        """
        self.user_data = self.data_loader()
        self.usage_summary = self.summary_builder(self.user_data)
        self.populate_table()
        self.update_dashboard()

    def populate_table(self):
        self.table_widget.setRowCount(len(self.user_data))
        for row_idx, record in enumerate(self.user_data):
            for col_idx, (key, _) in enumerate(self.TABLE_COLUMNS):
                value = record.get(key, "")
                if isinstance(value, bool):
                    display_value = "Yes" if value else "No"
                else:
                    display_value = str(value)
                item = QTableWidgetItem(display_value)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_widget.setItem(row_idx, col_idx, item)

    def update_dashboard(self):
        summary = self.usage_summary
        if not summary:
            return
        for key, label in self.dashboard_labels.items():
            value = summary.get(key, "-")
            label.setText(str(value))

        if summary.get("roles"):
            role_lines = [
                f"{role}: {count}"
                for role, count in summary["roles"].items()
            ]
            self.roles_label.setText(", ".join(role_lines))
        else:
            self.roles_label.setText("No role data available.")

    def set_logged_in_user(self, email: str):
        self.welcome_label.setText(f"Welcome back, {email}!")
        self.tabs.setCurrentWidget(self.welcome_tab)
        self.refresh_data()


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
            if hasattr(self.stack, "main_screen"):
                self.stack.main_screen.set_logged_in_user(email_value)
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
