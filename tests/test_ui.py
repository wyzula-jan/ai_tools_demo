import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ui import App, MainAppWindow
from utils import load_user_database, get_usage_summary


def _create_app_with_qtbot(qtbot):
    stack = App()
    qtbot.addWidget(stack)
    return stack


def test_login_rejects_invalid_email(qtbot):
    stack = _create_app_with_qtbot(qtbot)
    login = stack.login_screen

    login.email.setText("not-an-email")
    login.password.setText("Admin123!")
    login.handle_login()

    assert "Invalid email" in login.error_label.text()


def test_successful_login_switches_to_main_screen(qtbot):
    stack = _create_app_with_qtbot(qtbot)
    login = stack.login_screen

    login.email.setText("admin@example.com")
    login.password.setText("Admin123!")
    login.handle_login()

    assert stack.currentIndex() == 1
    assert "admin@example.com" in stack.main_screen.welcome_label.text()
    assert stack.main_screen.tabs.currentWidget() == stack.main_screen.welcome_tab


def test_database_table_populates_from_mock_data(qtbot):
    main = MainAppWindow()
    qtbot.addWidget(main)

    expected_rows = len(load_user_database())
    assert main.table_widget.rowCount() == expected_rows


def test_dashboard_stats_reflect_usage_summary(qtbot):
    main = MainAppWindow()
    qtbot.addWidget(main)

    summary = get_usage_summary(load_user_database())
    for key, label in main.dashboard_labels.items():
        assert str(summary[key]) == label.text()

    roles_text = main.roles_label.text()
    for role in summary["roles"].keys():
        assert role in roles_text
