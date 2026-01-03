from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
        QWidget, 
        QHBoxLayout, 
        QVBoxLayout, 
        QPushButton, 
        QLabel, 
        QSpinBox, 
        QFormLayout,
        )


class RightPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None

        layout = QVBoxLayout(self)

        self.btn_load = QPushButton("Load Project")
        layout.addWidget(self.btn_load)

        self.btn_save = QPushButton("Save Project")
        layout.addWidget(self.btn_save)

        form = QFormLayout()
        layout.addLayout(form)

        self.sp_w = QSpinBox()
        self.sp_w.setRange(1, 20000)
        self.sp_w.setValue(500)

        self.sp_h = QSpinBox()
        self.sp_h.setRange(1, 20000)
        self.sp_h.setValue(500)

        row = QHBoxLayout()
        row.addWidget(QLabel("Width"))
        row.addWidget(self.sp_w)
        row.addWidget(QLabel("Height"))
        row.addWidget(self.sp_h)

        form.addRow(row)
        layout.addStretch()

        self.btn_start = QPushButton("Start")
        layout.addWidget(self.btn_start)
