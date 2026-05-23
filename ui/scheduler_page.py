from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QComboBox,
    QFrame
)

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class SchedulerPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CPU Scheduling Simulator")
        self.setGeometry(300, 100, 1100, 750)

        self.processes = []

        self.init_ui()

    # ================= UI =================
    def init_ui(self):

        main_layout = QVBoxLayout()

        # Title
        title = QLabel("CPU Scheduling Simulator")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Input row
        input_layout = QHBoxLayout()

        self.process_input = QLineEdit()
        self.process_input.setPlaceholderText("Process Name")

        self.burst_input = QLineEdit()
        self.burst_input.setPlaceholderText("Burst Time")

        self.priority_input = QLineEdit()
        self.priority_input.setPlaceholderText("Priority")

        self.quantum_input = QLineEdit()
        self.quantum_input.setPlaceholderText("Quantum (RR)")

        add_btn = QPushButton("Add Process")
        add_btn.clicked.connect(self.add_process)

        input_layout.addWidget(self.process_input)
        input_layout.addWidget(self.burst_input)
        input_layout.addWidget(self.priority_input)
        input_layout.addWidget(self.quantum_input)
        input_layout.addWidget(add_btn)

        main_layout.addLayout(input_layout)

        # Algorithm selector
        self.algorithm_box = QComboBox()
        self.algorithm_box.addItems(["FCFS", "SJF", "Priority", "Round Robin"])
        main_layout.addWidget(self.algorithm_box)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Process", "Burst", "Priority", "Waiting", "Turnaround"
        ])

        main_layout.addWidget(self.table)

        # Run button
        run_btn = QPushButton("Run Scheduling")
        run_btn.clicked.connect(self.run_algorithm)
        main_layout.addWidget(run_btn)

        # Output label
        self.output_label = QLabel("Execution Order:")
        self.output_label.setFont(QFont("Arial", 14))
        main_layout.addWidget(self.output_label)

        # Gantt title
        gantt_title = QLabel("Gantt Chart")
        gantt_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(gantt_title)

        # Gantt container
        self.gantt_layout = QHBoxLayout()

        self.gantt_frame = QFrame()
        self.gantt_frame.setLayout(self.gantt_layout)
        self.gantt_frame.setStyleSheet("""
            background-color: #1E1E1E;
            border-radius: 10px;
            padding: 10px;
        """)

        main_layout.addWidget(self.gantt_frame)

        self.setLayout(main_layout)

    # ================= ADD PROCESS =================
    def add_process(self):

        name = self.process_input.text()
        burst = self.burst_input.text()
        priority = self.priority_input.text()

        if not name or not burst:
            QMessageBox.warning(self, "Error", "Enter required fields")
            return

        try:
            burst = int(burst)
            priority = int(priority) if priority else 0
        except:
            QMessageBox.warning(self, "Error", "Burst/Priority must be numbers")
            return

        self.processes.append({
            "name": name,
            "burst": burst,
            "priority": priority
        })

        self.load_table()

        self.process_input.clear()
        self.burst_input.clear()
        self.priority_input.clear()

    # ================= LOAD TABLE =================
    def load_table(self):

        self.table.setRowCount(len(self.processes))

        for i, p in enumerate(self.processes):

            self.table.setItem(i, 0, QTableWidgetItem(p["name"]))
            self.table.setItem(i, 1, QTableWidgetItem(str(p["burst"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(p["priority"])))

    # ================= RUN =================
    def run_algorithm(self):

        if not self.processes:
            QMessageBox.warning(self, "Error", "No processes added")
            return

        algo = self.algorithm_box.currentText()

        if algo == "FCFS":
            self.run_fcfs()

        elif algo == "SJF":
            self.run_sjf()

        elif algo == "Priority":
            self.run_priority()

        elif algo == "Round Robin":
            self.run_rr()

    # ================= FCFS =================
    def run_fcfs(self):
        self.calculate(self.processes, "FCFS")

    # ================= SJF =================
    def run_sjf(self):
        sorted_p = sorted(self.processes, key=lambda x: x["burst"])
        self.calculate(sorted_p, "SJF")

    # ================= PRIORITY =================
    def run_priority(self):
        sorted_p = sorted(self.processes, key=lambda x: x["priority"])
        self.calculate(sorted_p, "Priority")

    # ================= ROUND ROBIN =================
    def run_rr(self):

        try:
            q = int(self.quantum_input.text())
        except:
            QMessageBox.warning(self, "Error", "Enter valid quantum")
            return

        remaining = []
        for p in self.processes:
            remaining.append({
                "name": p["name"],
                "remaining": p["burst"]
            })

        execution = []
        gantt = []

        while True:
            done = True

            for p in remaining:

                if p["remaining"] > 0:
                    done = False

                    time_slice = min(q, p["remaining"])

                    execution.append(p["name"])

                    gantt.append({
                        "name": p["name"],
                        "burst": time_slice
                    })

                    p["remaining"] -= time_slice

            if done:
                break

        self.output_label.setText(
            "Execution Order:\n" + " → ".join(execution)
        )

        self.draw_gantt(gantt)

    # ================= CALCULATE =================
    def calculate(self, plist, algo):

        wt = 0
        total_wt = 0
        total_tat = 0
        exec_order = []

        self.table.setRowCount(len(plist))

        for i, p in enumerate(plist):

            tat = wt + p["burst"]

            self.table.setItem(i, 0, QTableWidgetItem(p["name"]))
            self.table.setItem(i, 1, QTableWidgetItem(str(p["burst"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(p["priority"])))
            self.table.setItem(i, 3, QTableWidgetItem(str(wt)))
            self.table.setItem(i, 4, QTableWidgetItem(str(tat)))

            exec_order.append(p["name"])

            total_wt += wt
            total_tat += tat

            wt += p["burst"]

        avg_wt = total_wt / len(plist)
        avg_tat = total_tat / len(plist)

        self.output_label.setText(
            f"Execution Order:\n{' → '.join(exec_order)}\n\n"
            f"Avg Waiting Time: {avg_wt:.2f}\n"
            f"Avg Turnaround Time: {avg_tat:.2f}"
        )

        self.draw_gantt(plist)

    # ================= GANTT CHART (FIXED) =================
    def draw_gantt(self, plist):

        # clear old blocks
        while self.gantt_layout.count():
            item = self.gantt_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        time = 0

        for p in plist:

            block = QLabel(f"{p['name']}\n{time}-{time + p['burst']}")

            block.setFixedHeight(70)
            block.setFixedWidth(max(60, p["burst"] * 40))

            block.setAlignment(Qt.AlignmentFlag.AlignCenter)

            block.setStyleSheet("""
                background-color: cyan;
                color: black;
                border-radius: 8px;
                font-weight: bold;
            """)

            self.gantt_layout.addWidget(block)

            time += p["burst"]