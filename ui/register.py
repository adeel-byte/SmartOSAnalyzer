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


class RegisterWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Register")
        self.setGeometry(500, 200, 400, 500)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel(" ")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        register_btn = QPushButton("Register")

        register_btn.clicked.connect(self.register_user)

        widgets = [
            self.username_input,
            self.email_input,
            self.password_input,
            register_btn
        ]

        for widget in widgets:
            widget.setMinimumHeight(45)
            layout.addWidget(widget)

        layout.addWidget(title)

        self.setLayout(layout)

    def register_user(self):

        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Fill all fields")
            return

        try:

            conn, cursor = connect_db()

            cursor.execute("""
                INSERT INTO users(username, email, password)
                VALUES (?, ?, ?)
            """, (username, email, password))

            conn.commit()

            QMessageBox.information(
                self,
                "Success",
                "Registration Successful"
            )

            conn.close()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))