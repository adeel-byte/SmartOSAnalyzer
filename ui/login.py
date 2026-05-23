from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

from PyQt6.QtGui import QFont

from core.database import connect_db

from ui.dashboard import DashboardWindow
from ui.register import RegisterWindow


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(500, 200, 400, 500)

        self.register_window = None
        self.dashboard = None

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel(" ")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Login")

        register_btn = QPushButton("Create New Account")

        login_btn.clicked.connect(self.login_user)

        register_btn.clicked.connect(self.open_register)

        widgets = [
            self.email_input,
            self.password_input,
            login_btn,
            register_btn
        ]

        for widget in widgets:
            widget.setMinimumHeight(45)
            layout.addWidget(widget)

        layout.addWidget(title)

        self.setLayout(layout)

    def login_user(self):

        email = self.email_input.text()
        password = self.password_input.text()

        conn, cursor = connect_db()

        cursor.execute("""
            SELECT * FROM users
            WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        conn.close()

        if user:

            QMessageBox.information(
                self,
                "Success",
                "Login Successful"
            )

            self.dashboard = DashboardWindow()
            self.dashboard.show()

            self.close()

        else:
            QMessageBox.warning(
                self,
                "Error",
                "Invalid Email or Password"
            )

    def open_register(self):

        self.register_window = RegisterWindow()
        self.register_window.show()