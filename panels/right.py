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
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project

        layout = QVBoxLayout(self)

        #buttons
        self.btn_load = QPushButton("Load Project")
        self.btn_save = QPushButton("Save Project")
        self.btn_limage = QPushButton("Load Image")

        project_row = QHBoxLayout()
        project_row.addWidget(self.btn_load)
        project_row.addWidget(self.btn_save)

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

        layout.addLayout(project_row)
        layout.addWidget(QLabel("Project name: " + self.project.name))
        layout.addLayout(row)
        layout.addWidget(self.btn_limage)
        layout.addStretch()

        self.btn_start = QPushButton("Start")
        layout.addWidget(self.btn_start)
