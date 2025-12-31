from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class LeftPanel(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    layout = QVBoxLayout(self)

    self.image = QLabel()
    self.image.setAlignment(Qt.AlignCenter)
    self.image.setPixmap(QPixmap("71.jpg"))

    layout.addWidget(self.image)

