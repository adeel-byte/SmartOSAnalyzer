from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QMessageBox
)

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

import psutil


class ProcessPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Process Manager")

        self.init_ui()

        # Timer for live updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_processes)
        self.timer.start(2000)

    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Process Manager")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Process...")

        self.search_input.textChanged.connect(self.load_processes)

        # Table
        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "PID",
            "Process Name",
            "CPU %",
            "RAM %"
        ])

        self.table.horizontalHeader().setStretchLastSection(True)

        # Kill Button
        kill_btn = QPushButton("Kill Selected Process")

        kill_btn.clicked.connect(self.kill_process)

        layout.addWidget(title)
        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.addWidget(kill_btn)

        self.setLayout(layout)

        self.load_processes()

    def load_processes(self):

        search_text = self.search_input.text().lower()

        processes = []

        for proc in psutil.process_iter([
            'pid',
            'name',
            'cpu_percent',
            'memory_percent'
        ]):

            try:

                process_name = proc.info['name']

                if search_text in process_name.lower():

                    processes.append(proc.info)

            except:
                pass

        self.table.setRowCount(len(processes))

        for row, proc in enumerate(processes):

            self.table.setItem(
                row, 0,
                QTableWidgetItem(str(proc['pid']))
            )

            self.table.setItem(
                row, 1,
                QTableWidgetItem(proc['name'])
            )

            self.table.setItem(
                row, 2,
                QTableWidgetItem(str(proc['cpu_percent']))
            )

            self.table.setItem(
                row, 3,
                QTableWidgetItem(
                    f"{proc['memory_percent']:.2f}"
                )
            )

    def kill_process(self):

        selected_row = self.table.currentRow()

        if selected_row == -1:

            QMessageBox.warning(
                self,
                "Error",
                "Select a process first"
            )

            return

        pid_item = self.table.item(selected_row, 0)

        pid = int(pid_item.text())

        try:

            process = psutil.Process(pid)

            process.terminate()

            QMessageBox.information(
                self,
                "Success",
                f"Process {pid} terminated"
            )

            self.load_processes()

        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )