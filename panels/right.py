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
  outputSizeChanged = Signal(int, int)

  def __init__(self, parent=None):
    super().__init__(parent)

    layout = QVBoxLayout(self)

    self.btn_load = QPushButton("Load")
    layout.addWidget(self.btn_load)

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
