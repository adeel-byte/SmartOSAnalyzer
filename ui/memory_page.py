from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QMessageBox
)

from PyQt6.QtGui import QFont


class MemoryPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memory Management Simulator")
        self.setGeometry(300, 100, 900, 600)

        self.frames = []
        self.frame_size = 3

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Page Replacement Simulator (FIFO / LRU)")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # INPUT
        input_layout = QHBoxLayout()

        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("Enter pages (e.g. 1 2 3 4 1 2 5)")

        self.algo_input = QLineEdit()
        self.algo_input.setPlaceholderText("FIFO or LRU")

        btn = QPushButton("Run Simulation")
        btn.clicked.connect(self.run_simulation)

        input_layout.addWidget(self.page_input)
        input_layout.addWidget(self.algo_input)
        input_layout.addWidget(btn)

        # OUTPUT
        self.output = QLabel("")
        self.output.setFont(QFont("Arial", 14))

        layout.addWidget(title)
        layout.addLayout(input_layout)
        layout.addWidget(self.output)

        self.setLayout(layout)

    # ================= MAIN LOGIC =================
    def run_simulation(self):

        pages_text = self.page_input.text()
        algo = self.algo_input.text().upper()

        if not pages_text:
            QMessageBox.warning(self, "Error", "Enter page sequence")
            return

        pages = list(map(int, pages_text.split()))

        if algo == "FIFO":
            self.fifo(pages)

        elif algo == "LRU":
            self.lru(pages)

        else:
            QMessageBox.warning(self, "Error", "Enter FIFO or LRU")

    # ================= FIFO =================
    def fifo(self, pages):

        memory = []
        hits = 0
        faults = 0

        for p in pages:

            if p in memory:
                hits += 1
            else:
                faults += 1

                if len(memory) < self.frame_size:
                    memory.append(p)
                else:
                    memory.pop(0)
                    memory.append(p)

        self.output.setText(
            f"""
FIFO RESULT

Page Hits: {hits}
Page Faults: {faults}
Final Memory: {memory}
"""
        )

    # ================= LRU =================
    def lru(self, pages):

        memory = []
        recent = []
        hits = 0
        faults = 0

        for p in pages:

            if p in memory:
                hits += 1
                recent.remove(p)
                recent.append(p)

            else:
                faults += 1

                if len(memory) < self.frame_size:
                    memory.append(p)
                    recent.append(p)
                else:
                    lru_page = recent.pop(0)
                    memory[memory.index(lru_page)] = p
                    recent.append(p)

        self.output.setText(
            f"""
LRU RESULT

Page Hits: {hits}
Page Faults: {faults}
Final Memory: {memory}
"""
        )