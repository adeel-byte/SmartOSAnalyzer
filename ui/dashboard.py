from ui.scheduler_page import SchedulerPage
from ui.memory_page import MemoryPage

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QFrame
)

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

import psutil
import pyqtgraph as pg

from ui.process_page import ProcessPage


class DashboardWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SmartOS Analyzer")
        self.setGeometry(100, 100, 1400, 800)

        self.cpu_data = []
        self.ram_data = []

        self.process_window = None

        self.init_ui()

        # Real-time update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graphs)
        self.timer.start(1000)

    def init_ui(self):

        main_layout = QHBoxLayout()

        # ================= SIDEBAR =================

        sidebar = QFrame()
        sidebar.setFixedWidth(250)

        sidebar.setStyleSheet("""
            background-color: #1E1E1E;
            border-radius: 15px;
        """)

        sidebar_layout = QVBoxLayout()

        title = QLabel("SmartOS")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))

        title.setStyleSheet("""
            color: cyan;
            padding: 20px;
        """)

        sidebar_layout.addWidget(title)

        # ================= BUTTONS =================

        dashboard_btn = QPushButton("Dashboard")
        process_btn = QPushButton("Processes")
        scheduler_btn = QPushButton("Scheduler")
        memory_btn = QPushButton("Memory")
        memory_btn.clicked.connect(self.open_memory_page)

        buttons = [
            dashboard_btn,
            process_btn,
            scheduler_btn,
            memory_btn
        ]

        for btn in buttons:

            btn.setFixedHeight(55)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2D2D2D;
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                }

                QPushButton:hover {
                    background-color: cyan;
                    color: black;
                }
            """)

            sidebar_layout.addWidget(btn)

        # Open Process Manager
        process_btn.clicked.connect(self.open_process_page)

        scheduler_btn.clicked.connect(self.open_scheduler_page)

        sidebar_layout.addStretch()

        sidebar.setLayout(sidebar_layout)

        # ================= MAIN CONTENT =================

        content = QFrame()

        content_layout = QVBoxLayout()

        heading = QLabel("System Monitoring Dashboard")

        heading.setFont(QFont("Arial", 28, QFont.Weight.Bold))

        heading.setStyleSheet("""
            color: white;
            padding: 10px;
        """)

        # ================= CPU GRAPH =================

        self.cpu_plot = pg.PlotWidget()

        self.cpu_plot.setBackground("#121212")

        self.cpu_plot.setTitle("CPU Usage (%)")

        self.cpu_curve = self.cpu_plot.plot(
            pen=pg.mkPen('c', width=3)
        )

        # ================= RAM GRAPH =================

        self.ram_plot = pg.PlotWidget()

        self.ram_plot.setBackground("#121212")

        self.ram_plot.setTitle("RAM Usage (%)")

        self.ram_curve = self.ram_plot.plot(
            pen=pg.mkPen('m', width=3)
        )

        # ================= ADD TO LAYOUT =================

        content_layout.addWidget(heading)
        content_layout.addWidget(self.cpu_plot)
        content_layout.addWidget(self.ram_plot)

        content.setLayout(content_layout)

        # ================= MAIN LAYOUT =================

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        self.setLayout(main_layout)

    def update_graphs(self):

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        self.cpu_data.append(cpu)
        self.ram_data.append(ram)

        # Keep latest 30 values
        self.cpu_data = self.cpu_data[-30:]
        self.ram_data = self.ram_data[-30:]

        self.cpu_curve.setData(self.cpu_data)
        self.ram_curve.setData(self.ram_data)

    def open_process_page(self):

        self.process_window = ProcessPage()
        self.process_window.show()

    def open_scheduler_page(self):

        self.scheduler_window = SchedulerPage()
        self.scheduler_window.show()

    def open_memory_page(self):
        self.memory_window = MemoryPage()
        self.memory_window.show()