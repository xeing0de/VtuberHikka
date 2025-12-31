from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class RightPanel(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    layout = QVBoxLayout(self)

    self.btn_load = QPushButton("Load")
    layout.addWidget(self.btn_load)
    layout.addStretch()

