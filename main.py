import sys

from PyQt6.QtWidgets import QApplication

from qt_material import apply_stylesheet

from ui.login import LoginWindow


app = QApplication(sys.argv)

apply_stylesheet(app, theme='dark_cyan.xml')

window = LoginWindow()
window.show()

sys.exit(app.exec())